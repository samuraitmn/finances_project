# RiskGuard evaluation report

- Generated (UTC): `2026-11-24T07:38:07.737806+00:00`
- Scenarios: **9**
- Passed: **9**
- Failed: **0**
- Pass rate: **100.0%**

## Scenario results

| Scenario | Risk | Expected | Actual | Result |
|---|---:|---|---|---|
| safe_internal_email | 10 | ALLOW | ALLOW | PASS |
| external_email_with_attachment | 40 | REVIEW_REQUIRED | REVIEW_REQUIRED | PASS |
| approved_external_email | 40 | ALLOW_WITH_APPROVAL | ALLOW_WITH_APPROVAL | PASS |
| rejected_external_email | 40 | BLOCKED_BY_HUMAN | BLOCKED_BY_HUMAN | PASS |
| small_transfer | 20 | ALLOW | ALLOW | PASS |
| medium_external_transfer | 60 | REVIEW_REQUIRED | REVIEW_REQUIRED | PASS |
| large_external_transfer | 90 | BLOCKED | BLOCKED | PASS |
| recoverable_single_delete | 20 | ALLOW | ALLOW | PASS |
| permanent_bulk_delete | 100 | BLOCKED | BLOCKED | PASS |

## Decision distribution

- `ALLOW`: 3
- `ALLOW_WITH_APPROVAL`: 1
- `BLOCKED`: 2
- `BLOCKED_BY_HUMAN`: 1
- `REVIEW_REQUIRED`: 2

## Interpretation

The report evaluates a deterministic teaching policy, not a trained or calibrated machine-learning model. A failed scenario means the observed policy decision differs from the scenario's declared expected decision.
