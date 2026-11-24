# Submission Guide

**Project:** RiskGuard — Human-in-the-Loop AI Safety Simulator  
**Platform:** GitHub Actions

## What to review

1. Project implementation: `riskguard/src/riskguard/`
2. Scenario dataset: `riskguard/data/scenarios.json`
3. Quality tests: `riskguard/tests/`
4. Quality CI workflow: [`.github/workflows/quality-ci.yml`](https://github.com/samuraitmn/finances_project/blob/main/.github/workflows/quality-ci.yml)
5. Project CI workflow: [`.github/workflows/project-ci.yml`](https://github.com/samuraitmn/finances_project/blob/main/.github/workflows/project-ci.yml)
6. Model declaration: `riskguard/AI_MODELS.md`

## CI run links

- Quality CI workflow: https://github.com/samuraitmn/finances_project/blob/main/.github/workflows/quality-ci.yml
- Successful Quality CI run on final commit: **REPLACE_WITH_QUALITY_RUN_URL**
- Project CI workflow: https://github.com/samuraitmn/finances_project/blob/main/.github/workflows/project-ci.yml
- Successful Project CI run on final commit: **REPLACE_WITH_PROJECT_RUN_URL**

Both runs must correspond to the final submitted commit and have a successful status.

## Project CI artifact

The successful Project CI run uploads an artifact named `riskguard-evaluation-report`.

The artifact contains:

- `evaluation.json` — scenario inputs, expected and actual outcomes, risk scores, explanations, and summary metrics.
- `evaluation.md` — readable evaluation summary and result table.

The workflow validates the generated report and fails if any scenario fails or if the report is inconsistent.

## Reproduction

Run these commands from the repository root:

```bash
cd riskguard
python -m pip install -e ".[dev]"
python -m ruff check src tests
python -m pytest -v
python -m riskguard.evaluate --scenarios data/scenarios.json --output artifacts
python -m riskguard.verify_report artifacts/evaluation.json
```

