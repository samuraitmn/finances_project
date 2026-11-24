"""Validate the generated report before CI uploads it."""

import json
import sys
from pathlib import Path


def main() -> int:
    report_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("artifacts/evaluation.json")
    markdown_path = report_path.with_name("evaluation.md")
    if not report_path.is_file() or not markdown_path.is_file():
        raise SystemExit("ERROR: evaluation.json or evaluation.md is missing")

    report = json.loads(report_path.read_text(encoding="utf-8"))
    summary = report.get("summary", {})
    results = report.get("results", [])
    if summary.get("total") != len(results) or not results:
        raise SystemExit("ERROR: report summary does not match scenario results")
    if summary.get("failed") != sum(not row.get("passed", False) for row in results):
        raise SystemExit("ERROR: failed counter does not match scenario results")
    if summary.get("failed") != 0:
        raise SystemExit(f"ERROR: evaluation contains {summary['failed']} failed scenarios")
    print(
        f"REPORT VALID: {summary['passed']}/{summary['total']} scenarios passed; "
        f"{summary['pass_rate_percent']}% pass rate"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
