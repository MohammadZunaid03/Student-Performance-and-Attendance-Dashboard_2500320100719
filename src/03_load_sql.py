"""Load cleaned project CSVs into Oracle and export business-query results.

Environment variables required: ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN.
Run: python src/03_load_sql.py
This script performs a controlled full reload (DELETE + INSERT + COMMIT).
"""
import os
from pathlib import Path
import pandas as pd
import oracledb

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
SQL_FILE = ROOT / "sql" / "queries.sql"
RESULTS = ROOT / "reports" / "sql_results"


def require_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def rows(frame, columns):
    return [tuple(None if pd.isna(v) else v for v in row)
            for row in frame[columns].itertuples(index=False, name=None)]


def main():
    user, password, dsn = require_env("ORACLE_USER"), require_env("ORACLE_PASSWORD"), require_env("ORACLE_DSN")
    required = ["students.csv", "subjects.csv", "academic_terms.csv", "marks.csv", "attendance.csv"]
    for name in required:
        if not (CLEAN / name).exists():
            raise FileNotFoundError(f"Missing cleaned input {CLEAN / name}; run src/02_clean_data.py first")

    students = pd.read_csv(CLEAN / "students.csv")
    subjects = pd.read_csv(CLEAN / "subjects.csv")
    terms = pd.read_csv(CLEAN / "academic_terms.csv")
    marks = pd.read_csv(CLEAN / "marks.csv")
    attendance = pd.read_csv(CLEAN / "attendance.csv")

    connection = oracledb.connect(user=user, password=password, dsn=dsn)
    try:
        with connection.cursor() as cur:
            # Controlled reload: delete facts before dimensions to respect foreign keys.
            for table in ["fact_marks", "fact_attendance", "dim_date",
                          "dim_student", "dim_subject", "dim_academic_term"]:
                cur.execute(f"DELETE FROM {table}")

            cur.executemany(
                "INSERT INTO dim_student (student_id, student_name, department, semester, section) VALUES (:1,:2,:3,:4,:5)",
                rows(students, ["Student_ID", "Student_Name", "Department", "Semester", "Section"]),
            )
            cur.executemany(
                "INSERT INTO dim_subject (subject_id, subject_name, subject_code, maximum_marks, passing_marks) VALUES (:1,:2,:3,:4,:5)",
                rows(subjects, ["Subject_ID", "Subject_Name", "Subject_Code", "Maximum_Marks", "Passing_Marks"]),
            )
            cur.executemany(
                "INSERT INTO dim_academic_term (term_id, academic_year, semester_label, start_date, end_date) VALUES (:1,:2,:3,TO_DATE(:4,'YYYY-MM-DD'),TO_DATE(:5,'YYYY-MM-DD'))",
                rows(terms, ["Term_ID", "Academic_Year", "Semester", "Start_Date", "End_Date"]),
            )
            cur.execute("SELECT student_id, student_key FROM dim_student")
            student_keys = dict(cur.fetchall())
            cur.execute("SELECT subject_id, subject_key FROM dim_subject")
            subject_keys = dict(cur.fetchall())
            cur.execute("SELECT term_id, term_key FROM dim_academic_term")
            term_key = dict(cur.fetchall())[str(terms.iloc[0]["Term_ID"])]

            mark_rows = []
            for r in marks.itertuples(index=False):
                mark_rows.append((
                    str(r.Marks_ID), student_keys[str(r.Student_ID)], subject_keys[str(r.Subject_ID)], term_key,
                    None if pd.isna(r.Internal_Marks) else float(r.Internal_Marks),
                    None if pd.isna(r.External_Marks) else float(r.External_Marks),
                    None if pd.isna(r.Total_Marks) else float(r.Total_Marks),
                    None if pd.isna(r.Grade) else str(r.Grade), str(r.Result), str(r.Record_Status)
                ))
            cur.executemany(
                """INSERT INTO fact_marks
                (source_marks_id, student_key, subject_key, term_key, internal_marks,
                 external_marks, total_marks, grade, result, record_status)
                VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)""", mark_rows
            )

            attendance_rows = []
            for r in attendance.itertuples(index=False):
                attendance_rows.append((
                    str(r.Attendance_ID), student_keys[str(r.Student_ID)], subject_keys[str(r.Subject_ID)], term_key,
                    int(r.Total_Classes), int(r.Present_Classes), int(r.Absent_Classes),
                    float(r.Attendance_Percentage)
                ))
            cur.executemany(
                """INSERT INTO fact_attendance
                (source_attendance_id, student_key, subject_key, term_key, total_classes,
                 present_classes, absent_classes, attendance_percentage)
                VALUES (:1,:2,:3,:4,:5,:6,:7,:8)""", attendance_rows
            )
        connection.commit()
        print(f"Loaded students={len(students)}, subjects={len(subjects)}, terms={len(terms)}, "
              f"marks={len(marks)}, attendance={len(attendance)}")

        RESULTS.mkdir(parents=True, exist_ok=True)
        sql_text = SQL_FILE.read_text(encoding="utf-8")
        statements = [s.strip() for s in sql_text.split(";") if s.strip()]
        with connection.cursor() as cur:
            for statement in statements:
                if not statement or statement.startswith("--"):
                    continue
                cur.execute(statement)
                if cur.description:
                    columns = [d[0] for d in cur.description]
                    output = pd.DataFrame(cur.fetchall(), columns=columns)
                    name = f"query_{len(list(RESULTS.glob('query_*.csv'))) + 1:02d}.csv"
                    output.to_csv(RESULTS / name, index=False)
                    print(f"Exported {name}: {len(output)} rows")
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
