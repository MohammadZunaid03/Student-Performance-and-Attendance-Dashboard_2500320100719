"""Create a 20-record independent calculation check.

Run after cleaning: python src/06_manual_validation.py
This is a deterministic sample-based arithmetic check, not a substitute for
institutional approval of the grade policy.
"""
from pathlib import Path
import pandas as pd
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from business_rules import RULES

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
REPORTS = ROOT / "reports"
GRADE_BANDS = [(int(item["min_score"]), item["grade"]) for item in RULES["grade_bands"]]


def grade(total):
    for boundary, label in GRADE_BANDS:
        if total >= boundary:
            return label
    return "F"


def main():
    marks = pd.read_csv(CLEAN / "marks.csv")
    students = pd.read_csv(CLEAN / "students.csv")
    sample = (marks[marks["Record_Status"].eq("PRESENT")]
              .sort_values(["Student_ID", "Subject_ID"])
              .drop_duplicates("Student_ID").head(20).copy())
    sample["Calculated_Total"] = sample["Internal_Marks"] + sample["External_Marks"]
    sample["Expected_Grade"] = sample["Calculated_Total"].map(grade)
    sample["Grade_Match"] = sample["Expected_Grade"].eq(sample["Grade"])
    sample["Expected_Result"] = sample.apply(
        lambda r: "PASS" if r["Calculated_Total"] >= r["Passing_Marks"] else "FAIL", axis=1)
    sample["Result_Match"] = sample["Expected_Result"].eq(sample["Result"])
    sample = sample.merge(students[["Student_ID", "Student_Name"]], on="Student_ID", how="left")
    columns = ["Student_ID", "Student_Name", "Subject_ID", "Internal_Marks",
               "External_Marks", "Total_Marks", "Calculated_Total", "Expected_Grade",
               "Grade", "Grade_Match", "Expected_Result", "Result", "Result_Match"]
    REPORTS.mkdir(parents=True, exist_ok=True)
    sample[columns].to_csv(REPORTS / "manual_validation_20.csv", index=False)
    if len(sample) < 20:
        raise RuntimeError(f"Only {len(sample)} eligible students available; expected at least 20")
    if not sample["Grade_Match"].all() or not sample["Result_Match"].all():
        raise AssertionError("Manual validation sample contains mismatched grade/result calculations")
    print(f"PASS: {len(sample)} student records matched grade and result arithmetic.")


if __name__ == "__main__":
    main()
