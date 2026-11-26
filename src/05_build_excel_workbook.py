"""Build an Excel verification workbook from the cleaned project CSVs.

Run: python src/05_build_excel_workbook.py
Open the generated workbook in Excel to add native PivotTables and slicers.
"""
from pathlib import Path
import json
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
    raw_students = pd.read_csv(ROOT / "data" / "raw" / "students.csv")
    raw_subjects = pd.read_csv(ROOT / "data" / "raw" / "subjects.csv")
    raw_attendance = pd.read_csv(ROOT / "data" / "raw" / "attendance.csv")
    raw_terms = pd.read_csv(ROOT / "data" / "raw" / "academic_terms.csv")
    rules = json.loads((ROOT / "config" / "business_rules.json").read_text(encoding="utf-8"))
    marks_detail = marks.merge(students, on="Student_ID", how="left").merge(
        subjects[["Subject_ID", "Subject_Name"]], on="Subject_ID", how="left")

    wb = Workbook()
    ws = wb.active
    ws.title = "Raw_Data"
    add_frame(ws, raw_marks, "RawMarks")
    add_frame(wb.create_sheet("Raw_Students"), raw_students, "RawStudents")
    add_frame(wb.create_sheet("Raw_Subjects"), raw_subjects, "RawSubjects")
    add_frame(wb.create_sheet("Raw_Attendance"), raw_attendance, "RawAttendance")
    add_frame(wb.create_sheet("Raw_Academic_Terms"), raw_terms, "RawAcademicTerms")
    ws = wb.create_sheet("Cleaned_Data")
    add_frame(ws, marks_detail, "CleanedMarks")

    student_summary = students[["Student_ID", "Student_Name", "Department", "Semester", "Section"]].copy()
    student_summary["Aggregate_Marks"] = student_summary["Student_ID"].map(
        marks[marks["Record_Status"].eq("PRESENT")].groupby("Student_ID")["Total_Marks"].sum())
    student_summary["Average_Attendance"] = student_summary["Student_ID"].map(
        attendance.groupby("Student_ID")["Attendance_Percentage"].mean())
    student_summary["Rank"] = student_summary["Aggregate_Marks"].rank(method="min", ascending=False).astype("Int64")
    student_summary["Topper_Status"] = student_summary["Rank"].map(lambda value: "TOPPER" if value == 1 else "")
    ws = wb.create_sheet("Student_Summary")
    add_frame(ws, student_summary, "StudentSummary")
    for row in range(2, ws.max_row + 1):
        ws.cell(row, 8, f'=RANK.EQ(F{row},$F$2:$F${ws.max_row},0)')
        ws.cell(row, 9, f'=IF(H{row}=1,"TOPPER","")')

    ws = wb.create_sheet("Attendance_Analysis")
    attendance_detail = attendance.merge(students, on="Student_ID", how="left")
    attendance_detail["Recalculated_Absent_Classes"] = attendance_detail["Total_Classes"] - attendance_detail["Present_Classes"]
    attendance_detail["Recalculated_Attendance_Percentage"] = (
        attendance_detail["Present_Classes"] / attendance_detail["Total_Classes"] * 100
    ).round(2)
    attendance_detail["Validation_Status"] = (
        attendance_detail["Absent_Classes"].eq(attendance_detail["Recalculated_Absent_Classes"])
        & (attendance_detail["Attendance_Percentage"] - attendance_detail["Recalculated_Attendance_Percentage"]).abs().lt(0.01)
    ).map({True: "PASS", False: "CHECK"})
    add_frame(ws, attendance_detail, "AttendanceAnalysis")

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
    ws.append(["Configured Low Attendance Threshold", float(rules["attendance_threshold_pct"])])
    ws.append(["Data Source", "Synthetic fictional demonstration dataset"])
    ws.append(["Note", "Open in Excel; formulas recalculate on open. Create native PivotTables and slicers using the tables."])
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
    scored = marks[marks["Record_Status"].eq("PRESENT")]
    low_count = int((attendance.groupby("Student_ID")["Attendance_Percentage"].mean() < float(rules["attendance_threshold_pct"])).sum())
    python_values = {
        "Total Students": int(students["Student_ID"].nunique()),
        "Average Marks": float(scored["Total_Marks"].mean()),
        "Average Attendance": float(attendance["Attendance_Percentage"].mean()),
        "Pass Percentage": float(scored["Result"].eq("PASS").sum() / len(scored) * 100),
        "Low Attendance Count": low_count,
    }
    excel_formulas = {
        "Total Students": "=COUNTA(StudentSummary[Student_ID])",
        "Average Marks": '=AVERAGEIF(CleanedMarks[Record_Status],"PRESENT",CleanedMarks[Total_Marks])',
        "Average Attendance": "=AVERAGE(AttendanceAnalysis[Attendance_Percentage])",
        "Pass Percentage": '=IFERROR(COUNTIFS(CleanedMarks[Record_Status],"PRESENT",CleanedMarks[Result],"PASS")/COUNTIF(CleanedMarks[Record_Status],"PRESENT")*100,0)',
        "Low Attendance Count": '=COUNTIF(StudentSummary[Average_Attendance],"<"&Dashboard!B6)',
    }
    for i, metric in enumerate(python_values, start=2):
        ws.append([metric, python_values[metric], None, excel_formulas[metric],
                   f'=IF(C{i}="","PENDING",IF(AND(ABS(B{i}-C{i})<0.01,ABS(B{i}-D{i})<0.01),"MATCH","MISMATCH"))'])
    ws.append(["Instructions", "Calculated from cleaned CSVs", "Fill only after Oracle execution", "Formula-based Excel result", "PENDING until Oracle result is entered"])

    rules_rows = [
        ("ATTENDANCE_THRESHOLD_PCT", rules["attendance_threshold_pct"], "Provisional threshold"),
        ("INTERNAL_MARKS_MAX", rules["assessment_components"]["internal_max"], "Synthetic internal maximum"),
        ("EXTERNAL_MARKS_MAX", rules["assessment_components"]["external_max"], "Synthetic external maximum"),
        ("TOTAL_MARKS_MAX", rules["assessment_components"]["total_max"], "Synthetic total maximum"),
        ("PASSING_MARKS_DEFAULT", rules["passing_marks_default"], "Synthetic default passing mark"),
    ]
    rule_ws = wb.create_sheet("Business_Rules")
    add_frame(rule_ws, pd.DataFrame(rules_rows, columns=["Rule_Key", "Numeric_Value", "Description"]), "BusinessRules")
    grade_ws = wb.create_sheet("Grade_Bands")
    add_frame(grade_ws, pd.DataFrame([(x["grade"], x["min_score"]) for x in rules["grade_bands"]],
                                     columns=["Grade", "Minimum_Score"]), "GradeBands")
    for sheet in wb.worksheets:
        style_sheet(sheet)
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)

    # Create the requested data dictionary workbook from the documented source schema.
    dictionary_rows = [
        ("students","Student_ID","Text","Stable student identifier","STU001","Required; unique after cleaning","No"),
        ("students","Student_Name","Text","Fictional display name","Student 001","Trim whitespace; title-case display","No"),
        ("students","Department","Text","Department code","CSE","Trim/uppercase; blank becomes UNKNOWN","Raw yes; clean no"),
        ("students","Semester","Integer","Semester number","3","Positive integer","No"),
        ("students","Section","Text","Class section","A","Non-empty after trim","No"),
        ("subjects","Subject_ID","Text","Subject identifier","SUB01","Required; unique","No"),
        ("subjects","Subject_Name","Text","Subject title","Programming in C++","Required; trim whitespace","No"),
        ("subjects","Subject_Code","Text","Subject code","SUB01","Required; unique","No"),
        ("subjects","Maximum_Marks","Integer","Maximum combined score","100","Positive","No"),
        ("subjects","Passing_Marks","Integer","Subject passing score","40","0 to Maximum_Marks","No"),
        ("marks","Marks_ID","Text","Source marks row identifier","M00001","Required; unique after duplicate handling","No"),
        ("marks","Student_ID","Text","Student reference","STU001","Must exist in students","No"),
        ("marks","Subject_ID","Text","Subject reference","SUB01","Must exist in subjects","No"),
        ("marks","Internal_Marks","Integer","Internal assessment score","28","0 to configured internal maximum; blank for ABSENT/MISSING","Yes"),
        ("marks","External_Marks","Integer","External assessment score","52","0 to configured external maximum; blank for ABSENT/MISSING","Yes"),
        ("marks","Total_Marks","Integer","Combined score","80","Recomputed; not above subject maximum","Yes"),
        ("marks","Grade","Text","Derived grade","A","Generated from config/business_rules.json; blank in raw input","Yes"),
        ("marks","Result","Text","Derived outcome","PASS","PASS/FAIL/ABSENT/MISSING; blank in raw input","Yes"),
        ("marks","Record_Status","Enum","Marks record state","PRESENT","PRESENT, ABSENT or MISSING","No"),
        ("attendance","Attendance_ID","Text","Source attendance row identifier","A00001","Required; unique after duplicate handling","No"),
        ("attendance","Student_ID","Text","Student reference","STU001","Must exist in students","No"),
        ("attendance","Subject_ID","Text","Subject reference","SUB01","Must exist in subjects","No"),
        ("attendance","Total_Classes","Integer","Conducted classes","40","Positive integer","No"),
        ("attendance","Present_Classes","Integer","Attended classes","34","Integer from 0 to Total_Classes","No"),
        ("attendance","Absent_Classes","Integer","Missed classes","6","Recomputed as total minus present","No"),
        ("attendance","Attendance_Percentage","Decimal","Attendance rate","85.00","Recomputed; 0 to 100","No"),
        ("academic_terms","Term_ID","Text","Academic-term identifier","TERM2026S1","Required; unique","No"),
        ("academic_terms","Academic_Year","Text","Academic-year label","2026-27","Required; non-empty","No"),
        ("academic_terms","Semester","Text","Semester grouping label","3/4","Required; non-empty","No"),
        ("academic_terms","Start_Date","Date","Term start date","2026-07-01","Valid ISO date","No"),
        ("academic_terms","End_Date","Date","Term end date","2026-12-15","Valid ISO date; on/after Start_Date","No"),
        ("clean marks","Term_ID","Text","Academic term key attached during cleaning","TERM2026S1","Must match one validated term in single-term prototype","No"),
        ("clean attendance","Term_ID","Text","Academic term key attached during cleaning","TERM2026S1","Must match one validated term in single-term prototype","No"),
    ]
    dict_wb = Workbook()
    dict_ws = dict_wb.active
    dict_ws.title = "Data_Dictionary"
    dict_ws.append(["Table", "Column", "Data Type", "Description", "Example", "Validation Rule", "Nullable"])
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
