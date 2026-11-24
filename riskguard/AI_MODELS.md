# AI models and assistance declaration

This project uses a deterministic, explicitly specified risk-scoring policy. No generative model or trained machine-learning model is called by the application at runtime.

## AI assistance

| Activity | Model | Use |
|---|---|---|
| Project idea and architecture | OpenAI GPT-6 | Brainstorming and structuring the Human-in-the-Loop simulator |
| Source code and tests | OpenAI GPT-6 | Assistance with implementation, test design, and debugging |
| CI/CD configuration | OpenAI GPT-6 | Assistance drafting the two GitVerse workflow files |
| Documentation | OpenAI GPT-6 | Assistance drafting README, submission navigation, and this declaration |

The student is responsible for reviewing the generated code, running the workflows, inspecting their logs, and making any required corrections before submission.

## Runtime models

- Generative AI model: none.
- Trained ML model: none.
- Decision mechanism: deterministic Python risk-scoring rules in `src/riskguard/core.py`.
