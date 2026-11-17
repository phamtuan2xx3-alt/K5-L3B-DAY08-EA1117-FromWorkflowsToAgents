"""Shape C — orchestrator plus read-only investigators. Student work.

1. Build a handoff with `lab8.handoff.make_handoff`. Allowed tools are read-only.
   Never put parent_secret, raw headers, or the full claim row into facts.
2. `lab8.runtime.run_readonly_investigators` runs those tools.
3. The orchestrator quotes from the investigator's order view and calls
   `durability.issue_refund`. Investigators have no write registry.
   Pass the full quote; the host subtracts earlier refunds on the same order.
   `lookup_refund_history` is a read-only tool you may hand to an investigator.
4. Trace the sanitized handoff, not the parent context.

An LLM summary of the parent context is not a sanitizer. Use the allowlist.

Trace contract v1 (docs/contracts.md): return a trace_path to a JSON file written in this run,
{"run_id": <same run_id>, "events": [...]}, on every return path including early
ones. `lab8.trace.Trace` does this; your own tracer is fine if it matches.
"""

from __future__ import annotations

import sqlite3

from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.handoff import make_handoff
from lab8.mock_llm import complete
from lab8.runtime import run_readonly_investigators
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish, safe_dump
from lab8.tools import get_claim_view, tool_cost
from lab8.trace import Trace

SHAPE = "orchestrator"

# Read-only tools the investigator may use. No write tool can be listed here:
# make_handoff rejects anything outside READONLY_TOOLS. lookup_refund_history is
# left out on purpose: the host already subtracts earlier refunds, so the result
# would cost a tool call without changing any decision.
INVESTIGATOR_TOOLS = [
    "lookup_order",
    "lookup_policy",
    "compute_compensation",
]


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    conn = connect(store_path)
    try:
        return _run(conn, claim_id, seed=seed, crash_at=crash_at)
    finally:
        conn.close()


def _run(conn: sqlite3.Connection, claim_id: str, *, seed: int, crash_at: str | None) -> RunResult:
    budget = Budget()
    trace = Trace(make_run_id(SHAPE, claim_id, seed))

    def done(status: str, proposal: int, reason: str | None) -> RunResult:
        trace.add("decision", {"status": status, "proposal_amount": int(proposal), "reason": reason})
        return finish(
            conn,
            shape=SHAPE,
            claim_id=claim_id,
            seed=seed,
            status=status,
            proposal_amount=proposal,
            budget=budget,
            trace=trace,
            error_reason=reason,
        )

    # Parent context. Only the orchestrator sees it; it never enters the trace or the handoff.
    claim = get_claim_view(conn, claim_id)
    budget.add_tool(tool_cost())
    if not claim.get("found"):
        return done("failed", 0, "unknown_claim")
    trace.add("claim", {"claim_id": claim_id, "has_order_id": bool(claim.get("order_id"))})

    # Order id comes from the claim column only, never from the ticket text.
    if not claim.get("order_id"):
        return done("needs_info", 0, "missing_order_id")

    # Allowlisted handoff: no ticket, no principal, no claim row. facts stays empty
    # because the investigator reads the order itself through scoped tools.
    handoff = make_handoff(
        request_id=f"REQ-{claim_id}",
        claim_id=claim_id,
        task="investigate_refund_entitlement",
        facts={},
        allowed_tools=INVESTIGATOR_TOOLS,
    )
    trace.add("handoff", safe_dump(handoff))

    investigated = run_readonly_investigators(conn, budget, handoff, principal_id=claim["principal_id"])
    tools = investigated["tools"]

    order_view = tools.get("lookup_order") or {}
    if not order_view.get("visible"):
        # Only the reason goes to the trace. lookup_order already strips phone/address/item/note.
        trace.add("investigator", {"order_visible": False, "reason": order_view.get("reason")})
        return done("escalated", 0, order_view.get("reason") or "order_not_visible")

    quote_payload = tools.get("compute_compensation") or {}
    trace.add(
        "investigator",
        {
            "order_visible": True,
            "order": safe_dump(order_view["order"]),
            "policy_count": len((tools.get("lookup_policy") or {}).get("policies") or []),
        },
    )

    # Money is decided by code (compute_compensation), not by the model.
    proposal = int(quote_payload.get("amount_vnd") or 0)
    trace.add("quote", safe_dump(quote_payload))

    # Model only drafts the customer reply. The prompt carries no ticket text and no PII.
    complete(budget, seed=seed, purpose="draft", prompt=f"claim={claim_id} proposal={proposal}")

    if proposal <= 0:
        return done("denied", 0, quote_payload.get("reason") or "no_entitlement")

    # Full quote goes to the host. The host checks approval, the per-order cap and
    # idempotency, and subtracts earlier refunds itself (T13, T14).
    try:
        outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
    except InjectedCrash:
        trace.add("crash", {"at": crash_at})
        trace.write()
        raise
    trace.add("host", {"ok": outcome["ok"], "reason": outcome["reason"], "conflict": outcome["conflict"]})

    if not outcome["ok"]:
        status = "failed" if outcome["conflict"] else "denied"
        return done(status, proposal, outcome["reason"])
    return done("resolved", proposal, None)
