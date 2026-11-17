"""Shape B: one bounded, read-only ReAct agent."""
from __future__ import annotations
import sqlite3
from lab8.db import connect
from lab8.durability import InjectedCrash, issue_refund
from lab8.mock_llm import complete
from lab8.runtime import run_react
from lab8.schemas import Budget, RunResult, make_run_id
from lab8.shapes.common import finish
from lab8.tools import get_claim_view, tool_cost
from lab8.trace import Trace

def run_claim(claim_id: str, *, seed: int, store_path: str, crash_at: str | None = None) -> RunResult:
    conn = connect(store_path)
    try:
        budget = Budget(); trace = Trace(make_run_id("single", claim_id, seed))
        budget.add_tool(tool_cost()); claim = get_claim_view(conn, claim_id)
        if not claim.get("found"):
            trace.add("error", {"reason": "unknown_claim"})
            return finish(conn, shape="single", claim_id=claim_id, seed=seed, status="failed", proposal_amount=0, budget=budget, trace=trace, error_reason="unknown_claim")
        if not claim.get("order_id"):
            complete(budget, seed=seed, purpose="draft", prompt="needs_info"); trace.add("decision", {"status": "needs_info"})
            return finish(conn, shape="single", claim_id=claim_id, seed=seed, status="needs_info", proposal_amount=0, budget=budget, trace=trace, error_reason="missing_order_id")
        def decide(obs: dict) -> dict:
            last, result = obs.get("last_tool"), obs.get("last_result") or {}
            if last is None:
                complete(budget, seed=seed, purpose="plan", prompt="lookup order")
                return {"tool": "lookup_order", "args": {"order_id": claim["order_id"], "principal_id": claim["principal_id"]}}
            if last == "lookup_order":
                if not result.get("visible"):
                    return {"final": {"status": "escalated", "proposal_amount": 0, "error_reason": result.get("reason", "not_found")}}
                complete(budget, seed=seed, purpose="plan", prompt="compute compensation")
                return {"tool": "compute_compensation", "args": {"order": result["order"]}}
            if last == "compute_compensation":
                return {"final": {"status": "resolved", "proposal_amount": int(result.get("amount_vnd", 0)), "quote": result}}
            return {"final": {"status": "failed", "proposal_amount": 0, "error_reason": "step_cap"}}
        final = run_react(conn, budget, observation={"claim": claim}, decide=decide, max_steps=8, worker=True)["final"]
        status, proposal, quote = final.get("status"), int(final.get("proposal_amount", 0)), final.get("quote") or {}
        if status == "escalated":
            trace.add("decision", {"status": status})
            return finish(conn, shape="single", claim_id=claim_id, seed=seed, status=status, proposal_amount=0, budget=budget, trace=trace, error_reason=final.get("error_reason"))
        trace.add("quote", {"amount_vnd": proposal, "reason": quote.get("reason"), "clause_ids": quote.get("clause_ids", [])})
        if proposal <= 0:
            return finish(conn, shape="single", claim_id=claim_id, seed=seed, status="denied", proposal_amount=0, budget=budget, trace=trace, error_reason=quote.get("reason"))
        try:
            outcome = issue_refund(conn, claim_id, proposal, crash_at=crash_at)
        except InjectedCrash:
            trace.add("crash", {"at": crash_at}); trace.write(); raise
        if not outcome["ok"]:
            status = "failed" if outcome.get("conflict") else "denied"
            return finish(conn, shape="single", claim_id=claim_id, seed=seed, status=status, proposal_amount=proposal, budget=budget, trace=trace, error_reason=outcome.get("reason"))
        return finish(conn, shape="single", claim_id=claim_id, seed=seed, status="resolved", proposal_amount=proposal, budget=budget, trace=trace)
    finally:
        conn.close()
