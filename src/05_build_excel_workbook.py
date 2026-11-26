"""Build an Excel verification workbook from the cleaned project CSVs.

Run: python src/05_build_excel_workbook.py
Open the generated workbook in Excel to add native PivotTables and slicers.
"""
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.chart import BarChart, Reference

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
OUT = ROOT / "excel" / "Student_Performance_Analysis.xlsx"


def add_frame(ws, frame, table_name):
    ws.append(list(frame.columns))
    for row in frame.itertuples(index=False, name=None):
        ws.append([None if pd.isna(v) else v for v in row])
    if ws.max_row >= 2 and ws.max_column:
        ref = f"A1:{ws.cell(ws.max_row, ws.max_column).coordinate}"
        table = Table(displayName=table_name, ref=ref)
        table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True,
                                               showColumnStripes=False)
        ws.add_table(table)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


def style_sheet(ws):
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
        cell.alignment = Alignment(wrap_text=True)
    for col in ws.columns:
        letter = col[0].column_letter
        width = min(max(max(len(str(c.value or "")) for c in col) + 2, 12), 32)
        ws.column_dimensions[letter].width = width


def main():
    required = ["students.csv", "subjects.csv", "marks.csv", "attendance.csv"]
    for name in required:
        if not (CLEAN / name).exists():
            raise FileNotFoundError(f"Missing {CLEAN / name}; run the cleaning pipeline first.")
    students = pd.read_csv(CLEAN / "students.csv")
    subjects = pd.read_csv(CLEAN / "subjects.csv")
    marks = pd.read_csv(CLEAN / "marks.csv")
    attendance = pd.read_csv(CLEAN / "attendance.csv")
    raw_marks = pd.read_csv(ROOT / "data" / "raw" / "marks.csv")
    marks_detail = marks.merge(students, on="Student_ID", how="left").merge(
        subjects[["Subject_ID", "Subject_Name"]], on="Subject_ID", how="left")

    wb = Workbook()
    ws = wb.active
    ws.title = "Raw_Data"
    add_frame(ws, raw_marks, "RawMarks")
    ws = wb.create_sheet("Cleaned_Data")
    add_frame(ws, marks_detail, "CleanedMarks")

    student_summary = students[["Student_ID", "Student_Name", "Department", "Semester", "Section"]].copy()
    student_summary["Aggregate_Marks"] = student_summary["Student_ID"].map(
        marks[marks["Record_Status"].eq("PRESENT")].groupby("Student_ID")["Total_Marks"].sum())
    student_summary["Average_Attendance"] = student_summary["Student_ID"].map(
        attendance.groupby("Student_ID")["Attendance_Percentage"].mean())
    ws = wb.create_sheet("Student_Summary")
    add_frame(ws, student_summary, "StudentSummary")

    ws = wb.create_sheet("Attendance_Analysis")
    add_frame(ws, attendance.merge(students, on="Student_ID", how="left"), "AttendanceAnalysis")

    subject_summary = marks[marks["Record_Status"].eq("PRESENT")].merge(
        subjects[["Subject_ID", "Subject_Name"]], on="Subject_ID")
    subject_summary = subject_summary.groupby("Subject_Name", as_index=False).agg(
        Average_Marks=("Total_Marks", "mean"),
        Scored_Records=("Total_Marks", "count"),
        Pass_Records=("Result", lambda s: int((s == "PASS").sum())),
        Fail_Records=("Result", lambda s: int((s == "FAIL").sum())))
    subject_summary["Pass_Percentage"] = subject_summary["Pass_Records"] / subject_summary["Scored_Records"] * 100
    ws = wb.create_sheet("Subject_Analysis")
    add_frame(ws, subject_summary, "SubjectAnalysis")

    ws = wb.create_sheet("Dashboard")
    ws.append(["Student Performance and Attendance Dashboard", "Value"])
    ws.append(["Total Students", "=COUNTA(StudentSummary[Student_ID])"])
    ws.append(["Average Marks (scored records)", '=AVERAGEIF(CleanedMarks[Record_Status],"PRESENT",CleanedMarks[Total_Marks])'])
    ws.append(["Pass Percentage (scored records)", '=IFERROR(COUNTIF(CleanedMarks[Result],"PASS")/COUNTIF(CleanedMarks[Record_Status],"PRESENT")*100,0)'])
    ws.append(["Average Attendance", "=AVERAGE(AttendanceAnalysis[Attendance_Percentage])"])
    ws.append(["Provisional Low Attendance Threshold", 75])
    ws.append(["Data Source", "Synthetic fictional demonstration dataset"])
    ws.append(["Note", "Open in Excel; formulas recalculate on open. Create PivotTables and slicers using the tables."])
    chart = BarChart()
    chart.title = "Subject-wise Average Marks"
    chart.y_axis.title = "Average Marks"
    chart.x_axis.title = "Subject"
    data = Reference(wb["Subject_Analysis"], min_col=2, min_row=1, max_row=wb["Subject_Analysis"].max_row)
    cats = Reference(wb["Subject_Analysis"], min_col=1, min_row=2, max_row=wb["Subject_Analysis"].max_row)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    ws.add_chart(chart, "D2")

    ws = wb.create_sheet("Validation")
    ws.append(["Metric", "Python Result", "Oracle SQL Result", "Excel Result", "Match Status"])
    metrics = ["Total Students", "Average Marks", "Average Attendance", "Pass Percentage", "Low Attendance Count"]
    for i, metric in enumerate(metrics, start=2):
        ws.append([metric, None, None, None,
                   f'=IF(AND(B{i}<>"",C{i}<>""),IF(AND(ABS(B{i}-C{i})<0.01,ABS(B{i}-D{i})<0.01),"MATCH","MISMATCH"),"PENDING")'])
    ws.append(["Instructions", "Populate from executed Python summary", "Populate from Oracle query", "Link to dashboard/verified calculation", "Do not claim MATCH until values are supplied"])

    for sheet in wb.worksheets:
        style_sheet(sheet)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)

    # Create the requested data dictionary workbook from the documented source schema.
    dictionary_rows = [
        ("students", "Student_ID", "Text", "Stable student identifier", "STU001", "No"),
        ("students", "Student_Name", "Text", "Fictional student display name", "Student 001", "No"),
        ("students", "Department", "Text", "Department code", "CSE / UNKNOWN", "Raw yes; clean no"),
        ("students", "Semester", "Integer", "Semester number", "3 or 4", "No"),
        ("students", "Section", "Text", "Class section", "A or B", "No"),
        ("subjects", "Subject_ID", "Text", "Subject identifier", "SUB01", "No"),
        ("subjects", "Subject_Name", "Text", "Subject title", "Programming in C++", "No"),
        ("subjects", "Subject_Code", "Text", "Subject code", "SUB01", "No"),
        ("subjects", "Maximum_Marks", "Integer", "Maximum combined marks", "100", "No"),
        ("subjects", "Passing_Marks", "Integer", "Synthetic passing mark", "40", "No"),
        ("marks", "Marks_ID", "Text", "Source marks row identifier", "M00001", "No"),
        ("marks", "Student_ID", "Text", "Student foreign key", "STU001", "No"),
        ("marks", "Subject_ID", "Text", "Subject foreign key", "SUB01", "No"),
        ("marks", "Internal_Marks", "Integer", "Internal score; synthetic max 40", "28", "Yes for ABSENT/MISSING"),
        ("marks", "External_Marks", "Integer", "External score; synthetic max 60", "52", "Yes for ABSENT/MISSING"),
        ("marks", "Total_Marks", "Integer", "Recomputed total score", "80", "Yes for ABSENT/MISSING"),
        ("marks", "Grade", "Text", "Derived grade", "A", "Yes"),
        ("marks", "Result", "Text", "Derived result/status", "PASS / FAIL / ABSENT / MISSING", "Yes in raw"),
        ("marks", "Record_Status", "Text", "Source marks status", "PRESENT / ABSENT / MISSING", "No"),
        ("attendance", "Attendance_ID", "Text", "Source attendance row identifier", "A00001", "No"),
        ("attendance", "Student_ID", "Text", "Student foreign key", "STU001", "No"),
        ("attendance", "Subject_ID", "Text", "Subject foreign key", "SUB01", "No"),
        ("attendance", "Total_Classes", "Integer", "Conducted classes", "40", "No; must be > 0"),
        ("attendance", "Present_Classes", "Integer", "Attended classes", "34", "No; 0..Total_Classes"),
        ("attendance", "Absent_Classes", "Integer", "Missed classes", "6", "Recomputed as total-present"),
        ("attendance", "Attendance_Percentage", "Decimal", "Present / total × 100", "85.00", "No; 0..100"),
        ("academic_terms", "Term_ID", "Text", "Academic term identifier", "TERM2026S1", "No"),
        ("academic_terms", "Academic_Year", "Text", "Academic-year label", "2026-27", "No"),
        ("academic_terms", "Semester", "Text", "Semester grouping", "3/4", "No"),
        ("academic_terms", "Start_Date", "Date", "Term start date", "2026-07-01", "No"),
        ("academic_terms", "End_Date", "Date", "Term end date", "2026-12-15", "No"),
    ]
    dict_wb = Workbook()
    dict_ws = dict_wb.active
    dict_ws.title = "Data_Dictionary"
    dict_ws.append(["Table", "Column", "Type", "Description", "Example / Rule", "Nullable"])
    for row in dictionary_rows:
        dict_ws.append(list(row))
    style_sheet(dict_ws)
    dictionary_path = ROOT / "docs" / "Data_Dictionary.xlsx"
    dictionary_path.parent.mkdir(parents=True, exist_ok=True)
    dict_wb.save(dictionary_path)
    print(f"Workbook created: {OUT}")
    print(f"Data dictionary created: {dictionary_path}")


if __name__ == "__main__":
    main()
