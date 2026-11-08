"""Choose the Claude model for one team-bot job. A fixed rule, no AI judgement.

Rules live in rules/rules.yml under `models`. An executor starts from its task's
risk and moves up the ladder after failures or rework, never down. Running out of
quota never moves a job down either: the job stops and a person looks.
"""
from __future__ import annotations


def choose(rules: dict, bot: str, meta: dict | None, payload: dict) -> tuple[str, str]:
    """Return (model, reason) for this job."""
    table = rules["models"]
    if bot != "executor":
        return table["default"], f"default for {bot}"
    ladder = table["ladder"]
    meta = meta or {}
    risk = meta.get("risk") or rules.get("merge_policy", {}).get("default_risk", "medium")
    start = table["executor_start_by_risk"].get(risk, table["default"])
    failures = int(meta.get("failures") or 0)
    rework = bool(payload.get("pr"))
    raised = bool(payload.get("raise_model"))
    steps = max(failures, 1 if rework else 0) + (1 if raised else 0)
    model = ladder[min(ladder.index(start) + steps, len(ladder) - 1)]
    return model, f"risk {risk}, failures {failures}, rework {rework}, raised by dev lead {raised}"
