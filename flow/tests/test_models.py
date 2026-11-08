from flow import models

RULES = {
    "merge_policy": {"default_risk": "medium"},
    "models": {
        "ladder": ["sonnet", "opus"],
        "default": "sonnet",
        "executor_start_by_risk": {"low": "sonnet", "medium": "sonnet", "high": "opus"},
    },
}


def pick(bot="executor", meta=None, **payload):
    return models.choose(RULES, bot, meta, payload)[0]


def test_other_bots_use_the_default_whatever_the_task():
    assert pick("reviewer", {"risk": "high", "failures": 2}) == "sonnet"
    assert pick("dev_lead", {"risk": "high"}) == "sonnet"


def test_executor_starts_from_risk():
    assert pick(meta={"risk": "low"}) == "sonnet"
    assert pick(meta={"risk": "high"}) == "opus"


def test_missing_risk_or_task_uses_the_default_risk():
    assert pick(meta={}) == "sonnet"
    assert pick(meta=None) == "sonnet"


def test_a_failure_moves_up():
    assert pick(meta={"risk": "low", "failures": 0}) == "sonnet"
    assert pick(meta={"risk": "low", "failures": 1}) == "opus"


def test_rework_on_an_existing_pr_moves_up_without_a_failure():
    assert pick(meta={"risk": "low"}, pr="https://example/pull/1") == "opus"


def test_the_dev_lead_can_raise_one_step():
    assert pick(meta={"risk": "low"}, raise_model=True) == "opus"


def test_stops_at_the_top_of_the_ladder():
    assert pick(meta={"risk": "high", "failures": 3}, pr="x", raise_model=True) == "opus"


def test_reason_says_why():
    _, reason = models.choose(RULES, "executor", {"risk": "low", "failures": 1}, {})
    assert "failures 1" in reason and "risk low" in reason
