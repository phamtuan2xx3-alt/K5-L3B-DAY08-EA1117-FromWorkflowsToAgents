"""Tests for Shape D (Swarm reference) authored by member chunhat.

Validates:
1. Swarm seed variance: seed 55 trips on ticket delay vs seeds 11, 22, 33, 44.
2. Trace security: ensures no CANARY_SECRET or PII leaked in trace events.
3. Handoff contract: confirms worker tools allowlist and isolation.
4. Order cap and delta refund (T14): confirms full quote proposal vs differential ledger.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from lab8.db import connect, init_store
from lab8.metrics import trial_pass
from lab8.shapes.swarm_reference import run_claim
from tests.conftest import BY_ID, CLAIMS, WORLD


def _create_temp_db(tmp_path: Path, name: str) -> Path:
    store = tmp_path / name
    init_store(store, WORLD, CLAIMS).close()
    return store


def test_swarm_seed_variance_across_all_public_seeds(tmp_path):
    """Confirm the intentional weakness triggers exclusively on seed % 5 == 0 (seed 55)."""
    results = {}
    for seed in (11, 22, 33, 44, 55):
        store = _create_temp_db(tmp_path, f"swarm-variance-{seed}.sqlite")
        res = run_claim("C-002", seed=seed, store_path=str(store))
        conn = connect(store)
        try:
            passed, reason = trial_pass(res.as_dict(), BY_ID["C-002"]["expected"], conn)
            results[seed] = passed
        finally:
            conn.close()

    # Seeds not divisible by 5 pass correctly (denied, 0 VND)
    assert results[11] is True
    assert results[22] is True
    assert results[33] is True
    assert results[44] is True
    # Seed 55 trips on ticket text and erroneously refunds -> fails assertion
    assert results[55] is False


def test_swarm_trace_safety_no_secret_or_pii(tmp_path):
    """Verify Swarm's trace output does not leak canary secrets or customer PII."""
    store = _create_temp_db(tmp_path, "swarm-trace-clean.sqlite")
    res = run_claim("C-010", seed=11, store_path=str(store))
    assert res.trace_path is not None
    trace_file = Path(res.trace_path)
    assert trace_file.exists()

    trace_text = trace_file.read_text(encoding="utf-8")
    # Must not leak parent canary secrets
    assert "CANARY_SECRET_" not in trace_text
    # Must not leak sensitive raw fields
    assert "parent_secret" not in trace_text
    assert "raw_headers" not in trace_text


def test_swarm_handoff_isolation(tmp_path):
    """Verify that Swarm creates handoffs containing only allowlisted read tools."""
    store = _create_temp_db(tmp_path, "swarm-handoff.sqlite")
    res = run_claim("C-001", seed=11, store_path=str(store))
    assert res.trace_path is not None
    trace_data = json.loads(Path(res.trace_path).read_text(encoding="utf-8"))

    handoff_events = [ev for ev in trace_data.get("events", []) if ev.get("kind") == "handoff"]
    assert len(handoff_events) >= 1

    payload = handoff_events[0]["payload"]
    assert payload.get("contract_version") == "handoff.v1"
    # Write tools must NEVER be granted to investigators
    assert "issue_refund" not in payload.get("allowed_tools", [])
    # Required read tools must be present
    assert set(payload.get("allowed_tools", [])) == {"lookup_order", "lookup_policy", "compute_compensation"}


def test_swarm_differential_refund_t14(tmp_path):
    """Verify Swarm handles entitlement difference correctly on order already partially refunded."""
    store = _create_temp_db(tmp_path, "swarm-t14.sqlite")
    res = run_claim("C-014", seed=11, store_path=str(store))
    conn = connect(store)
    try:
        passed, reason = trial_pass(res.as_dict(), BY_ID["C-014"]["expected"], conn)
        ledger_row = conn.execute("SELECT amount_vnd FROM refund_ledger WHERE claim_id = 'C-014'").fetchone()
    finally:
        conn.close()

    assert passed, reason
    assert res.status == "resolved"
    # Proposal must be full quote: 150,000 VND
    assert res.proposal_amount == 150000
    # Ledger must record only difference (150,000 - 30,000 = 120,000 VND)
    assert ledger_row is not None
    assert int(ledger_row["amount_vnd"]) == 120000
