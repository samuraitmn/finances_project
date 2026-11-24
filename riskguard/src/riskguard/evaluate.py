"""Run a reproducible scenario suite and generate JSON/Markdown reports."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from riskguard.core import Action, ActionType, Decision, evaluate_action

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCENARIOS = ROOT / "data" / "scenarios.json"


def load_scenarios(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("Scenario file must contain a non-empty JSON array")
    return data


def run_scenarios(scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for scenario in scenarios:
        action_data = dict(scenario["action"])
        action_data["action_type"] = ActionType(action_data["action_type"])
        action = Action(**action_data)
        approval = scenario.get("human_approval")
        evaluation = evaluate_action(action, approval)
        expected = scenario["expected_decision"]
        actual = evaluation.decision.value
        results.append(
            {
                "id": scenario["id"],
                "description": scenario["description"],
                "risk_score": evaluation.risk_score,
                "expected_decision": expected,
                "actual_decision": actual,
                "passed": expected == actual,
                "reasons": list(evaluation.reasons),
            }
        )

    passed = sum(item["passed"] for item in results)
    decisions = Counter(item["actual_decision"] for item in results)
    return {
        "project": "RiskGuard",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
            "pass_rate_percent": round(100 * passed / len(results), 2),
            "decisions": dict(sorted(decisions.items())),
        },
        "results": results,
    }


def write_reports(report: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "evaluation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = report["summary"]
    lines = [
        "# RiskGuard evaluation report",
        "",
        f"- Generated (UTC): `{report['generated_at_utc']}`",
        f"- Scenarios: **{summary['total']}**",
        f"- Passed: **{summary['passed']}**",
        f"- Failed: **{summary['failed']}**",
        f"- Pass rate: **{summary['pass_rate_percent']}%**",
        "",
        "## Scenario results",
        "",
        "| Scenario | Risk | Expected | Actual | Result |",
        "|---|---:|---|---|---|",
    ]
    for item in report["results"]:
        status = "PASS" if item["passed"] else "FAIL"
        lines.append(
            f"| {item['id']} | {item['risk_score']} | "
            f"{item['expected_decision']} | {item['actual_decision']} | {status} |"
        )
    lines.extend(["", "## Decision distribution", ""])
    for decision, count in summary["decisions"].items():
        lines.append(f"- `{decision}`: {count}")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The report evaluates a deterministic teaching policy, not a trained or "
            "calibrated machine-learning model. A failed scenario means the observed "
            "policy decision differs from the scenario's declared expected decision.",
            "",
        ]
    )
    (output_dir / "evaluation.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate RiskGuard safety scenarios.")
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts")
    args = parser.parse_args()

    report = run_scenarios(load_scenarios(args.scenarios))
    write_reports(report, args.output)
    summary = report["summary"]
    print(
        f"RiskGuard evaluation: {summary['passed']}/{summary['total']} passed; "
        f"{summary['failed']} failed"
    )
    print(f"Reports written to: {args.output.resolve()}")
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
