import pytest

from riskguard.core import Action, ActionType, Decision, calculate_risk, evaluate_action


def test_low_risk_email_is_allowed_automatically():
    result = evaluate_action(Action(ActionType.EMAIL))
    assert result.risk_score == 10
    assert result.decision is Decision.ALLOW


def test_medium_risk_action_requires_human_review():
    action = Action(ActionType.EMAIL, external_recipient=True, attachments=True)
    result = evaluate_action(action)
    assert result.risk_score == 40
    assert result.decision is Decision.REVIEW_REQUIRED


def test_human_rejection_blocks_action():
    action = Action(ActionType.EMAIL, external_recipient=True, attachments=True)
    result = evaluate_action(action, human_approval=False)
    assert result.decision is Decision.BLOCKED_BY_HUMAN


def test_human_approval_allows_review_level_action():
    action = Action(ActionType.EMAIL, external_recipient=True, attachments=True)
    result = evaluate_action(action, human_approval=True)
    assert result.decision is Decision.ALLOW_WITH_APPROVAL


def test_high_risk_action_cannot_be_overridden_by_human_approval():
    action = Action(
        ActionType.TRANSFER,
        amount=15_000,
        external_recipient=True,
        irreversible=True,
    )
    result = evaluate_action(action, human_approval=True)
    assert result.risk_score >= 70
    assert result.decision is Decision.BLOCKED


def test_non_transfer_cannot_have_money_amount():
    with pytest.raises(ValueError, match="only valid for transfer"):
        calculate_risk(Action(ActionType.EMAIL, amount=100))


def test_negative_transfer_amount_is_rejected():
    with pytest.raises(ValueError, match="must not be negative"):
        calculate_risk(Action(ActionType.TRANSFER, amount=-1))


@pytest.mark.parametrize(
    ("action", "expected"),
    [
        (Action(ActionType.TRANSFER, amount=100), 20),
        (Action(ActionType.TRANSFER, amount=1_000), 40),
        (Action(ActionType.TRANSFER, amount=10_000), 60),
    ],
)
def test_transfer_amount_thresholds(action, expected):
    score, _ = calculate_risk(action)
    assert score == expected
