# RiskGuard — Human-in-the-Loop AI Safety Simulator

RiskGuard is an educational simulator for deciding when an AI agent may execute an action automatically, when it must ask a human for approval, and when it must block the action.

## Problem and user value

Autonomous agents can send messages, transfer money, or delete data. These operations have different consequences. RiskGuard demonstrates an explicit, explainable policy that evaluates an action before execution:

| Risk score | Policy |
|---:|---|
| 0–29 | Allow automatically |
| 30–69 | Require human review |
| 70–100 | Block automatically |

A human rejection always blocks a review-level action. Human approval cannot override the automatic block for high-risk actions.

The current implementation is a deterministic teaching simulator. It is not a trained ML model, a production authorization system, or a substitute for security review.

## Features

- Risk scoring for email, money-transfer, and data-deletion actions.
- Human approval, rejection, and automatic blocking.
- Explainable reasons for each decision.
- Nine reproducible evaluation scenarios.
- JSON and Markdown evaluation reports.
- Unit and integration tests.

## Run locally

Requirements: Python 3.10 or newer.

```bash
python -m pip install -e ".[dev]"
ruff check src tests
python -m pytest -v
python -m riskguard.evaluate --scenarios data/scenarios.json --output artifacts
python -m riskguard.verify_report artifacts/evaluation.json
```

Generated files:
- `artifacts/evaluation.json` — machine-readable results.
- `artifacts/evaluation.md` — human-readable summary and scenario table.

## CI/CD

The repository contains two independent GitVerse workflows in `.gitverse/workflows/`.

### Quality CI

`quality-ci.yml` runs on pushes, pull requests, and manual dispatch. It installs the project, runs Ruff (`ruff check src tests`), and executes the unit/integration suite (`python -m pytest -v`). The tests check policy thresholds, invalid input handling, the human-rejection invariant, resistance to approval overrides for high-risk actions, and the complete scenario suite. A failed check produces a failed workflow status.

### Project CI

`project-ci.yml` runs on pushes and manual dispatch. It executes the actual scenario evaluation, generates JSON and Markdown reports, validates the report consistency and zero-failure condition, and uploads both reports as the `riskguard-evaluation-report` artifact. Open the successful Project CI run in GitVerse and download the artifact from its Artifacts section.

## New contribution

This project adds an end-to-end Human-in-the-Loop risk policy simulator, a scenario dataset, automated policy and integration tests, a reproducible evaluation command, report validation, and two separate CI workflows. The work is not merely a copy of a previous coursework submission.

## Repository layout

```text
.gitverse/workflows/
  quality-ci.yml
  project-ci.yml
data/
  scenarios.json
src/riskguard/
  __init__.py
  core.py
  evaluate.py
  verify_report.py
tests/
  test_policy.py
  test_evaluation.py
artifacts/                 # generated locally or by Project CI
README.md
SUBMISSION.md
AI_MODELS.md
pyproject.toml
```
