"""Generate deterministic synthetic student marks and attendance data.

Run from repository root: python src/01_generate_data.py
Raw files intentionally contain documented quality defects and fictional records.
"""
import csv
from datetime import date
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from business_rules import RULES

SEED = 20261126
STUDENT_COUNT = 200
SUBJECTS = [
    ("SUB01", "Programming in C++", RULES["assessment_components"]["total_max"], RULES["passing_marks_default"]),
    ("SUB02", "Database Management Systems", RULES["assessment_components"]["total_max"], RULES["passing_marks_default"]),
    ("SUB03", "Data Structures", RULES["assessment_components"]["total_max"], RULES["passing_marks_default"]),
    ("SUB04", "Computer Networks", RULES["assessment_components"]["total_max"], RULES["passing_marks_default"]),
    ("SUB05", "Mathematics for Computing", RULES["assessment_components"]["total_max"], RULES["passing_marks_default"]),
]
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


class DeterministicRng:
    """Small cross-language LCG so generated CSVs can be reproduced exactly."""
    def __init__(self, seed):
        self.state = seed

    def randbelow(self, upper):
        self.state = (1664525 * self.state + 1013904223) % (2 ** 32)
        return self.state % upper

    def randint(self, lower, upper):
        return lower + self.randbelow(upper - lower + 1)

    def choice(self, values):
        return values[self.randbelow(len(values))]


def write_csv(path, rows, columns):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main():
    rng = DeterministicRng(SEED)
    students = []
    departments = ["CSE", "IT", "ECE"]
    for n in range(1, STUDENT_COUNT + 1):
        students.append({
            "Student_ID": f"STU{n:03d}", "Student_Name": f"Student {n:03d}",
            "Department": departments[(n - 1) % 3],
            "Semester": 3 if n <= 100 else 4, "Section": "A" if n % 2 else "B",
        })

    subjects = [
        {"Subject_ID": sid, "Subject_Name": name, "Subject_Code": sid,
         "Maximum_Marks": maximum, "Passing_Marks": passing}
        for sid, name, maximum, passing in SUBJECTS
    ]

    marks, attendance = [], []
    marks_id = attendance_id = 1
    for student in students:
        ability = rng.randint(32, 92)
        for subject_id, subject_name, maximum, passing in SUBJECTS:
            internal_max = int(RULES["assessment_components"]["internal_max"])
            external_max = int(RULES["assessment_components"]["external_max"])
            total_max = int(RULES["assessment_components"]["total_max"])
            internal = max(0, min(internal_max, int(ability * internal_max / total_max + rng.randint(-7, 7) + 0.5)))
            external = max(0, min(external_max, int(ability * external_max / total_max + rng.randint(-10, 10) + 0.5)))
            status = "PRESENT"
            if student["Student_ID"] == "STU016" and subject_id == "SUB02":
                status, internal, external = "ABSENT", "", ""
            elif student["Student_ID"] == "STU015" and subject_id == "SUB03":
                status, internal, external = "MISSING", "", ""
            total = "" if status != "PRESENT" else internal + external
            marks.append({
                "Marks_ID": f"M{marks_id:05d}", "Student_ID": student["Student_ID"],
                "Subject_ID": subject_id, "Internal_Marks": internal,
                "External_Marks": external, "Total_Marks": total,
                "Grade": "", "Result": "", "Record_Status": status,
            })
            marks_id += 1
            total_classes = rng.choice([36, 40, 42, 45])
            present = rng.randint(max(0, total_classes - 12), total_classes)
            attendance.append({
                "Attendance_ID": f"A{attendance_id:05d}",
                "Student_ID": student["Student_ID"], "Subject_ID": subject_id,
                "Total_Classes": total_classes, "Present_Classes": present,
                "Absent_Classes": total_classes - present,
                "Attendance_Percentage": round(present / total_classes * 100, 2),
            })
            attendance_id += 1

    # Intentional defects: duplicate masters/facts, missing values, inconsistent text,
    # out-of-range marks and impossible attendance counts.
    students[10]["Department"] = ""
    students[11]["Student_Name"] = "  sTuDeNt 012 "
    students.append(dict(students[9]))
    internal_max = int(RULES["assessment_components"]["internal_max"])
    external_max = int(RULES["assessment_components"]["external_max"])
    total_max = int(RULES["assessment_components"]["total_max"])
    passing_boundary = int(RULES["passing_marks_default"])
    # Explicit boundary cases for minimum, pass threshold and maximum marks.
    marks[10]["Internal_Marks"], marks[10]["External_Marks"], marks[10]["Total_Marks"] = 0, passing_boundary, passing_boundary
    marks[11]["Internal_Marks"], marks[11]["External_Marks"], marks[11]["Total_Marks"] = internal_max, external_max, total_max
    marks[12]["Internal_Marks"], marks[12]["External_Marks"], marks[12]["Total_Marks"] = 0, 0, 0
    marks[0]["Internal_Marks"] = internal_max + 80
    marks[1]["External_Marks"] = -5
    marks.append(dict(marks[4]))
    attendance[0]["Present_Classes"] = attendance[0]["Total_Classes"] + 3
    attendance[1]["Student_ID"] = ""
    attendance.append(dict(attendance[2]))

    terms = [{
        "Term_ID": "TERM2026S1", "Academic_Year": "2026-27",
        "Semester": "3/4", "Start_Date": date(2026, 7, 1).isoformat(),
        "End_Date": date(2026, 12, 15).isoformat(),
    }]

    write_csv(RAW / "students.csv", students,
              ["Student_ID", "Student_Name", "Department", "Semester", "Section"])
    write_csv(RAW / "subjects.csv", subjects,
              ["Subject_ID", "Subject_Name", "Subject_Code", "Maximum_Marks", "Passing_Marks"])
    write_csv(RAW / "marks.csv", marks,
              ["Marks_ID", "Student_ID", "Subject_ID", "Internal_Marks",
               "External_Marks", "Total_Marks", "Grade", "Result", "Record_Status"])
    write_csv(RAW / "attendance.csv", attendance,
              ["Attendance_ID", "Student_ID", "Subject_ID", "Total_Classes",
               "Present_Classes", "Absent_Classes", "Attendance_Percentage"])
    write_csv(RAW / "academic_terms.csv", terms,
              ["Term_ID", "Academic_Year", "Semester", "Start_Date", "End_Date"])

    print(f"Generated synthetic raw datasets in {RAW}")
    print(f"Students={len(students)} Subjects={len(subjects)} "
          f"Marks={len(marks)} Attendance={len(attendance)} Terms={len(terms)}")


if __name__ == "__main__":
    main()
