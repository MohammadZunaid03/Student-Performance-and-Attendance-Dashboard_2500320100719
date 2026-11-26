"""Run pytest and export a compact CSV report."""
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
xml_path = REPORTS / "pytest_results.xml"
REPORTS.mkdir(parents=True, exist_ok=True)
completed = subprocess.run(
    [sys.executable, "-m", "pytest", str(ROOT / "tests" / "test_pipeline.py"),
     "-q", f"--junitxml={xml_path}"],
    cwd=ROOT, check=False
)
rows = []
if xml_path.exists():
    root = ET.parse(xml_path).getroot()
    for case in root.iter("testcase"):
        failure = case.find("failure")
        error = case.find("error")
        skipped = case.find("skipped")
        status = "SKIP" if skipped is not None else ("FAIL" if failure is not None or error is not None else "PASS")
        rows.append({
            "test_case_id": case.attrib.get("name", ""),
            "test_description": case.attrib.get("classname", ""),
            "expected_result": "Validation assertion succeeds",
            "actual_result": (failure if failure is not None else error).attrib.get("message", "") if (failure is not None or error is not None) else status,
            "status": status,
        })
pd.DataFrame(rows, columns=["test_case_id","test_description","expected_result","actual_result","status"]).to_csv(
    REPORTS / "test_results.csv", index=False
)
print(f"Test report: {REPORTS / 'test_results.csv'}")
sys.exit(completed.returncode)
