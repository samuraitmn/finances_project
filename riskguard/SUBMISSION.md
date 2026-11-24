# Submission guide

**Project:** RiskGuard — Human-in-the-Loop AI Safety Simulator  
**Platform:** GitVerse

## What to review

1. **Project implementation:** `src/riskguard/`
2. **Scenario dataset:** `data/scenarios.json`
3. **Quality tests:** `tests/`
4. **Quality workflow:** `.gitverse/workflows/quality-ci.yml`
5. **Project workflow:** `.gitverse/workflows/project-ci.yml`
6. **Model declaration:** `AI_MODELS.md`

## CI run links

After the workflows have run on the final commit, replace the placeholders below with links copied from the GitVerse CI/CD run pages:

- Quality CI workflow: `ADD_QUALITY_CI_WORKFLOW_URL`
- Successful Quality CI run on final commit: `ADD_SUCCESSFUL_QUALITY_RUN_URL`
- Project CI workflow: `ADD_PROJECT_CI_WORKFLOW_URL`
- Successful Project CI run on final commit: `ADD_SUCCESSFUL_PROJECT_RUN_URL`

Do not submit this document with placeholders. The links must point to actual runs of the final repository version.

## Project CI result

Open the successful Project CI run and download the artifact named `riskguard-evaluation-report`. It contains:

- `evaluation.json` — all scenario inputs' expected and actual outcomes, risk scores, explanations, and summary metrics.
- `evaluation.md` — a readable evaluation summary and result table.

The workflow also validates the generated report and fails if any scenario fails or if the report is inconsistent.

## Reproduction

Run the following commands from the repository root:

```bash
python -m pip install -e ".[dev]"
python -m pytest -v
python -m riskguard.evaluate --scenarios data/scenarios.json --output artifacts
python -m riskguard.verify_report artifacts/evaluation.json
```
