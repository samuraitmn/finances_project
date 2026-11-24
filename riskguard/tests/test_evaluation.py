import json
from pathlib import Path

from riskguard.evaluate import load_scenarios, run_scenarios, write_reports

ROOT = Path(__file__).resolve().parents[1]


def test_full_scenario_suite_passes():
    scenarios = load_scenarios(ROOT / "data" / "scenarios.json")
    report = run_scenarios(scenarios)
    assert report["summary"]["total"] == 9
    assert report["summary"]["failed"] == 0
    assert report["summary"]["pass_rate_percent"] == 100.0


def test_report_writer_creates_machine_and_human_readable_files(tmp_path):
    scenarios = load_scenarios(ROOT / "data" / "scenarios.json")
    report = run_scenarios(scenarios)
    write_reports(report, tmp_path)

    json_report = json.loads((tmp_path / "evaluation.json").read_text(encoding="utf-8"))
    markdown_report = (tmp_path / "evaluation.md").read_text(encoding="utf-8")
    assert json_report["summary"]["passed"] == 9
    assert "# RiskGuard evaluation report" in markdown_report
    assert "permanent_bulk_delete" in markdown_report
