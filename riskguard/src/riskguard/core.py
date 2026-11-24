"""Risk scoring and human-approval policy.

The policy is intentionally deterministic and explainable. It is a teaching
simulator, not a production security control or a calibrated ML model.
"""

from dataclasses import asdict, dataclass
from enum import Enum


class ActionType(str, Enum):
    EMAIL = "email"
    TRANSFER = "transfer"
    DELETE = "delete"


class Decision(str, Enum):
    ALLOW = "ALLOW"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    ALLOW_WITH_APPROVAL = "ALLOW_WITH_APPROVAL"
    BLOCKED = "BLOCKED"
    BLOCKED_BY_HUMAN = "BLOCKED_BY_HUMAN"


@dataclass(frozen=True)
class Action:
    """A proposed action from an AI agent."""

    action_type: ActionType
    amount: float = 0.0
    external_recipient: bool = False
    irreversible: bool = False
    attachments: bool = False
    broad_scope: bool = False
    recoverable: bool = True

    def validate(self) -> None:
        if self.amount < 0:
            raise ValueError("amount must not be negative")
        if self.action_type is not ActionType.TRANSFER and self.amount != 0:
            raise ValueError("amount is only valid for transfer actions")


@dataclass(frozen=True)
class Evaluation:
    risk_score: int
    decision: Decision
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["decision"] = self.decision.value
        result["reasons"] = list(self.reasons)
        return result


def calculate_risk(action: Action) -> tuple[int, tuple[str, ...]]:
    """Return an explainable risk score from 0 to 100 and its reasons."""
    action.validate()
    score = 0
    reasons: list[str] = []

    if action.action_type is ActionType.EMAIL:
        score += 10
        reasons.append("Base risk for sending an email: +10")
        if action.external_recipient:
            score += 15
            reasons.append("External recipient: +15")
        if action.attachments:
            score += 15
            reasons.append("Email contains attachments: +15")
        if action.irreversible:
            score += 10
            reasons.append("Action is marked irreversible: +10")

    elif action.action_type is ActionType.TRANSFER:
        score += 20
        reasons.append("Base risk for a money transfer: +20")
        if action.amount >= 1_000:
            score += 20
            reasons.append("Transfer is at least 1,000 units: +20")
        if action.amount >= 10_000:
            score += 20
            reasons.append("Transfer is at least 10,000 units: +20")
        if action.external_recipient:
            score += 20
            reasons.append("Recipient is external: +20")
        if action.irreversible:
            score += 10
            reasons.append("Transfer is marked irreversible: +10")

    elif action.action_type is ActionType.DELETE:
        score += 20
        reasons.append("Base risk for deleting data: +20")
        if action.broad_scope:
            score += 35
            reasons.append("Deletion affects a broad scope: +35")
        if not action.recoverable:
            score += 30
            reasons.append("Deleted data cannot be recovered: +30")
        if action.irreversible:
            score += 15
            reasons.append("Deletion is marked irreversible: +15")

    return min(score, 100), tuple(reasons)


def evaluate_action(action: Action, human_approval: bool | None = None) -> Evaluation:
    """Apply the risk policy and, where required, a human decision.

    Risk below 30 is allowed automatically. Risk from 30 through 69 requires
    human approval. Risk of 70 or higher is blocked and cannot be overridden.
    An explicit human rejection always blocks a review-level action.
    """
    score, reasons = calculate_risk(action)

    if score >= 70:
        return Evaluation(score, Decision.BLOCKED, reasons + ("Risk >= 70: automatic block",))

    if score < 30:
        return Evaluation(score, Decision.ALLOW, reasons + ("Risk < 30: automatic allow",))

    if human_approval is None:
        return Evaluation(
            score,
            Decision.REVIEW_REQUIRED,
            reasons + ("Risk is 30-69: waiting for human approval",),
        )

    if human_approval is False:
        return Evaluation(
            score,
            Decision.BLOCKED_BY_HUMAN,
            reasons + ("Human rejected the action: blocked",),
        )

    return Evaluation(
        score,
        Decision.ALLOW_WITH_APPROVAL,
        reasons + ("Human approved the action",),
    )
