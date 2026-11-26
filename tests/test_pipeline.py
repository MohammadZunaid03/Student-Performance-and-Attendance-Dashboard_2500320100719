"""Automated validation tests for the cleaned student analytics pipeline."""
import os
from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"


def load(name):
    path = CLEAN / name
    if not path.exists():
        pytest.skip(f"{path} missing; run python src/02_clean_data.py first")
    return pd.read_csv(path)


def test_student_primary_keys_unique():
    students = load("students.csv")
    assert students["Student_ID"].notna().all()
    assert students["Student_ID"].is_unique


def test_subject_primary_keys_unique():
    subjects = load("subjects.csv")
    assert subjects["Subject_ID"].notna().all()
    assert subjects["Subject_ID"].is_unique


def test_marks_student_subject_grain_unique():
    marks = load("marks.csv")
    assert marks["Term_ID"].notna().all()
    assert not marks.duplicated(["Student_ID", "Subject_ID", "Term_ID"]).any()


def test_attendance_student_subject_grain_unique():
    attendance = load("attendance.csv")
    assert attendance["Term_ID"].notna().all()
    assert not attendance.duplicated(["Student_ID", "Subject_ID", "Term_ID"]).any()


def test_required_student_references_exist():
    students = set(load("students.csv")["Student_ID"])
    for filename in ["marks.csv", "attendance.csv"]:
        frame = load(filename)
        assert frame["Student_ID"].notna().all()
        assert set(frame["Student_ID"]).issubset(students)


def test_marks_ranges_and_statuses():
    marks = load("marks.csv")
    subjects = load("subjects.csv").set_index("Subject_ID")
    assert marks["Record_Status"].isin(["PRESENT", "ABSENT", "MISSING"]).all()
    present = marks[marks["Record_Status"].eq("PRESENT")]
    import json
    rules = json.loads((ROOT / "config" / "business_rules.json").read_text(encoding="utf-8"))
    assert present["Internal_Marks"].between(0, rules["assessment_components"]["internal_max"]).all()
    assert present["External_Marks"].between(0, rules["assessment_components"]["external_max"]).all()
    assert present["Total_Marks"].between(0, rules["assessment_components"]["total_max"]).all()
    assert (present["Total_Marks"] == present["Internal_Marks"] + present["External_Marks"]).all()
    for row in present.itertuples():
        assert row.Total_Marks <= subjects.loc[row.Subject_ID, "Maximum_Marks"]


def test_absent_and_missing_marks_are_not_zero():
    marks = load("marks.csv")
    special = marks[marks["Record_Status"].isin(["ABSENT", "MISSING"])]
    assert special["Total_Marks"].isna().all()
    assert set(special["Result"]).issubset({"ABSENT", "MISSING"})


def test_attendance_ranges_and_calculations():
    attendance = load("attendance.csv")
    assert (attendance["Total_Classes"] > 0).all()
    assert attendance["Present_Classes"].between(0, attendance["Total_Classes"]).all()
    assert (attendance["Absent_Classes"] == attendance["Total_Classes"] - attendance["Present_Classes"]).all()
    assert attendance["Attendance_Percentage"].between(0, 100).all()


def test_python_totals_match_oracle_when_configured():
    if not all(os.getenv(k) for k in ["ORACLE_USER", "ORACLE_PASSWORD", "ORACLE_DSN"]):
        pytest.skip("Oracle credentials not configured; integration comparison not run")
    import oracledb
    marks = load("marks.csv")
    expected = float(marks.loc[marks["Record_Status"].eq("PRESENT"), "Total_Marks"].sum())
    conn = oracledb.connect(user=os.environ["ORACLE_USER"],
                            password=os.environ["ORACLE_PASSWORD"],
                            dsn=os.environ["ORACLE_DSN"])
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(total_marks) FROM fact_marks WHERE record_status='PRESENT'")
            actual = float(cur.fetchone()[0] or 0)
        assert abs(expected - actual) < 0.01
    finally:
        conn.close()



def test_grade_boundaries_are_consistent_with_demo_policy():
    import runpy
    module = runpy.run_path(str(ROOT / "src" / "02_clean_data.py"))
    grade_for = module["grade_for"]
    import json
    rules = json.loads((ROOT / "config" / "business_rules.json").read_text(encoding="utf-8"))
    for band in rules["grade_bands"]:
        assert grade_for(band["min_score"]) == band["grade"]


def test_pass_fail_matches_configured_subject_passing_marks():
    marks = load("marks.csv")
    present = marks[marks["Record_Status"].eq("PRESENT")]
    expected = present.apply(
        lambda row: "PASS" if row["Total_Marks"] >= row["Passing_Marks"] else "FAIL",
        axis=1
    )
    assert (expected.reset_index(drop=True) == present["Result"].reset_index(drop=True)).all()


def test_dense_rank_preserves_ties():
    scores = pd.Series([95, 95, 90, 80])
    ranks = scores.rank(method="dense", ascending=False).astype(int).tolist()
    assert ranks == [1, 1, 2, 3]



def test_clean_fact_term_keys_reference_valid_term():
    terms = load("academic_terms.csv")
    assert terms["Term_ID"].notna().all()
    assert terms["Term_ID"].is_unique
    valid = set(terms["Term_ID"])
    assert set(load("marks.csv")["Term_ID"]).issubset(valid)
    assert set(load("attendance.csv")["Term_ID"]).issubset(valid)


def test_attendance_threshold_uses_canonical_config():
    import json
    rules = json.loads((ROOT / "config" / "business_rules.json").read_text(encoding="utf-8"))
    threshold = float(rules["attendance_threshold_pct"])
    assert 0 <= threshold <= 100
    attendance = load("attendance.csv")
    expected = attendance.groupby("Student_ID")["Attendance_Percentage"].mean()
    low_ids = set(expected[expected < threshold].index)
    assert all(expected.loc[student_id] < threshold for student_id in low_ids)
