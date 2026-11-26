"""Clean raw synthetic student performance and attendance CSV files.

Run: python src/02_clean_data.py
Invalid records are quarantined, not silently discarded.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
REPORTS = ROOT / "reports"
ATTENDANCE_THRESHOLD = 75.0  # Provisional demo value; confirm institutional policy.
GRADE_BOUNDARIES = [(90, "A+"), (80, "A"), (70, "B"), (60, "C"),
                    (50, "D"), (40, "E"), (0, "F")]


def read_csv(name):
    path = RAW / name
    if not path.exists():
        raise FileNotFoundError(f"Required input not found: {path}")
    return pd.read_csv(path, dtype={"Student_ID": "string", "Subject_ID": "string"},
                       keep_default_na=True)


def add_log(log, issue, rule, count):
    log.append({"issue": issue, "rule_applied": rule, "rows_affected": int(count)})


def grade_for(total):
    for boundary, grade in GRADE_BOUNDARIES:
        if total >= boundary:
            return grade
    return "F"


def main():
    CLEAN.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    log = []

    # Student master: keep first occurrence by stable key; retain missing departments as UNKNOWN.
    students = read_csv("students.csv")
    before = len(students)
    students["Student_ID"] = students["Student_ID"].astype("string").str.strip()
    missing_id = students["Student_ID"].isna() | students["Student_ID"].eq("")
    student_rejects = students.loc[missing_id].copy()
    students = students.loc[~missing_id].copy()
    add_log(log, "students_missing_id", "Quarantine rows without Student_ID", missing_id.sum())
    dup = students.duplicated(subset=["Student_ID"], keep="first")
    add_log(log, "duplicate_students", "Keep first Student_ID; quarantine later duplicate rows", dup.sum())
    student_rejects = pd.concat([student_rejects, students.loc[dup]], ignore_index=True)
    students = students.loc[~dup].copy()
    students["Student_Name"] = students["Student_Name"].astype("string").str.strip().str.title()
    missing_dept = students["Department"].isna() | students["Department"].astype("string").str.strip().eq("")
    add_log(log, "missing_department", "Replace blank department with UNKNOWN; do not infer department", missing_dept.sum())
    students.loc[missing_dept, "Department"] = "UNKNOWN"
    students["Department"] = students["Department"].astype("string").str.strip().str.upper()
    students.to_csv(CLEAN / "students.csv", index=False)
    student_rejects.to_csv(CLEAN / "quarantine_students.csv", index=False)

    # Subject master.
    subjects = read_csv("subjects.csv")
    dup = subjects.duplicated(subset=["Subject_ID"], keep="first")
    add_log(log, "duplicate_subjects", "Keep first Subject_ID", dup.sum())
    subject_rejects = subjects.loc[dup].copy()
    subjects = subjects.loc[~dup].copy()
    subjects["Subject_ID"] = subjects["Subject_ID"].astype("string").str.strip()
    subjects["Subject_Name"] = subjects["Subject_Name"].astype("string").str.strip().str.title()
    subjects.to_csv(CLEAN / "subjects.csv", index=False)
    subject_rejects.to_csv(CLEAN / "quarantine_subjects.csv", index=False)

    valid_students = set(students["Student_ID"].dropna().astype(str))
    valid_subjects = set(subjects["Subject_ID"].dropna().astype(str))

    # Marks: one record per student/subject for this single-term sample.
    marks = read_csv("marks.csv")
    marks["Student_ID"] = marks["Student_ID"].astype("string").str.strip()
    marks["Subject_ID"] = marks["Subject_ID"].astype("string").str.strip()
    dup = marks.duplicated(subset=["Student_ID", "Subject_ID"], keep="first")
    add_log(log, "duplicate_marks", "Keep first student-subject marks record", dup.sum())
    mark_rejects = marks.loc[dup].copy()
    marks = marks.loc[~dup].copy()
    bad_fk = (marks["Student_ID"].isna() | marks["Student_ID"].eq("") |
              ~marks["Student_ID"].isin(valid_students) |
              marks["Subject_ID"].isna() | ~marks["Subject_ID"].isin(valid_subjects))
    add_log(log, "marks_invalid_foreign_key", "Quarantine marks with missing or unknown student/subject key", bad_fk.sum())
    mark_rejects = pd.concat([mark_rejects, marks.loc[bad_fk]], ignore_index=True)
    marks = marks.loc[~bad_fk].copy()
    for col in ["Internal_Marks", "External_Marks"]:
        marks[col] = pd.to_numeric(marks[col], errors="coerce")
    bounds = marks.merge(subjects[["Subject_ID", "Maximum_Marks", "Passing_Marks"]],
                         on="Subject_ID", how="left", validate="many_to_one")
    # Synthetic source split is documented as 40 internal + 60 external.
    invalid = ((bounds["Record_Status"] == "PRESENT") &
               (bounds["Internal_Marks"].isna() | bounds["External_Marks"].isna() |
                (bounds["Internal_Marks"] < 0) | (bounds["Internal_Marks"] > 40) |
                (bounds["External_Marks"] < 0) | (bounds["External_Marks"] > 60)))
    add_log(log, "marks_out_of_range_or_incomplete", "Quarantine PRESENT rows with missing/out-of-range component marks", invalid.sum())
    mark_rejects = pd.concat([mark_rejects, bounds.loc[invalid, marks.columns]], ignore_index=True)
    bounds = bounds.loc[~invalid].copy()
    bounds["Total_Marks"] = pd.NA
    present = bounds["Record_Status"].eq("PRESENT")
    bounds.loc[present, "Total_Marks"] = bounds.loc[present, "Internal_Marks"] + bounds.loc[present, "External_Marks"]
    bounds["Result"] = bounds["Record_Status"].map({"ABSENT": "ABSENT", "MISSING": "MISSING"})
    bounds["Grade"] = bounds["Record_Status"].map({"ABSENT": "AB", "MISSING": "NA"})
    for idx in bounds.index[present]:
        total = float(bounds.at[idx, "Total_Marks"])
        passing = float(bounds.at[idx, "Passing_Marks"])
        bounds.at[idx, "Result"] = "PASS" if total >= passing else "FAIL"
        bounds.at[idx, "Grade"] = grade_for(total)
    bounds[marks.columns.tolist() + ["Maximum_Marks", "Passing_Marks"]].to_csv(CLEAN / "marks.csv", index=False)

    # Attendance: recalculate absent count and percentage; quarantine impossible counts.
    attendance = read_csv("attendance.csv")
    attendance["Student_ID"] = attendance["Student_ID"].astype("string").str.strip()
    attendance["Subject_ID"] = attendance["Subject_ID"].astype("string").str.strip()
    dup = attendance.duplicated(subset=["Student_ID", "Subject_ID"], keep="first")
    add_log(log, "duplicate_attendance", "Keep first student-subject attendance record", dup.sum())
    attendance_rejects = attendance.loc[dup].copy()
    attendance = attendance.loc[~dup].copy()
    bad_fk = (attendance["Student_ID"].isna() | attendance["Student_ID"].eq("") |
              ~attendance["Student_ID"].isin(valid_students) |
              attendance["Subject_ID"].isna() | ~attendance["Subject_ID"].isin(valid_subjects))
    add_log(log, "attendance_invalid_foreign_key", "Quarantine attendance with missing or unknown student/subject key", bad_fk.sum())
    attendance_rejects = pd.concat([attendance_rejects, attendance.loc[bad_fk]], ignore_index=True)
    attendance = attendance.loc[~bad_fk].copy()
    for col in ["Total_Classes", "Present_Classes"]:
        attendance[col] = pd.to_numeric(attendance[col], errors="coerce")
    invalid = (attendance["Total_Classes"].isna() | attendance["Present_Classes"].isna() |
               (attendance["Total_Classes"] <= 0) | (attendance["Present_Classes"] < 0) |
               (attendance["Present_Classes"] > attendance["Total_Classes"]))
    add_log(log, "attendance_invalid_counts", "Quarantine non-positive totals or present counts outside 0..total", invalid.sum())
    attendance_rejects = pd.concat([attendance_rejects, attendance.loc[invalid]], ignore_index=True)
    attendance = attendance.loc[~invalid].copy()
    attendance["Absent_Classes"] = attendance["Total_Classes"] - attendance["Present_Classes"]
    attendance["Attendance_Percentage"] = (
        attendance["Present_Classes"] / attendance["Total_Classes"] * 100
    ).round(2)
    attendance.to_csv(CLEAN / "attendance.csv", index=False)
    attendance_rejects.to_csv(CLEAN / "quarantine_attendance.csv", index=False)

    # Terms are metadata and are copied after basic date validation.
    terms = read_csv("academic_terms.csv")
    terms["Start_Date"] = pd.to_datetime(terms["Start_Date"], errors="coerce")
    terms["End_Date"] = pd.to_datetime(terms["End_Date"], errors="coerce")
    bad_terms = terms["Start_Date"].isna() | terms["End_Date"].isna() | (terms["End_Date"] < terms["Start_Date"])
    add_log(log, "invalid_academic_terms", "Quarantine terms with invalid dates or end before start", bad_terms.sum())
    terms.loc[~bad_terms].to_csv(CLEAN / "academic_terms.csv", index=False)
    terms.loc[bad_terms].to_csv(CLEAN / "quarantine_academic_terms.csv", index=False)

    pd.DataFrame(log, columns=["issue", "rule_applied", "rows_affected"]).to_csv(
        REPORTS / "data_quality_log.csv", index=False
    )
    print("Cleaning complete.")
    print(f"Students accepted: {len(students)}; marks accepted: {len(bounds)}; attendance accepted: {len(attendance)}")
    print(f"Quality log: {REPORTS / 'data_quality_log.csv'}")


if __name__ == "__main__":
    main()
