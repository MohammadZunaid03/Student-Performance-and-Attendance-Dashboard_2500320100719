# Power BI Three-Page Interactive Report Guide

## Before building
Complete the imports and relationships in `docs/PowerBI_Data_Model.md`. Import Business_Rules and Grade_Bands from the generated config CSVs. Keep the synthetic-data caption and refresh timestamp visible.

## Global layout and slicers
Use a 16:9 page, aligned visuals and readable labels. Add slicers for Academic Year, Semester, Department, Section and Subject. Use View → Sync slicers to sync across pages. Use Format → Edit interactions to verify filtering. Keep ABSENT and MISSING separate; never plot them as zero.

## Page 1 — Academic Performance Overview
**Question:** How is the selected cohort performing?

| Visual | Type | Fields / measures | Filters |
|---|---|---|---|
| Total Students | Card | [Total Students] | All cohort slicers |
| Average Marks | Card | [Average Marks] | PRESENT records only |
| Pass Percentage | Card | [Pass Percentage] | PASS / PRESENT scored records |
| Average Attendance | Card | [Average Attendance] | Mean student-subject percentage |
| Pass/fail by department | Clustered column | Department, [Pass Count], [Fail Count] | Cohort slicers |
| Subject average | Bar chart | Subject_Name, [Subject Average Marks] | Subject/cohort slicers |
| Result distribution | Donut | Result, scored-record count | Record_Status = PRESENT |

Format percentages with % units, sort subject averages descending, use legible data labels and avoid truncated axes.

## Page 2 — Student and Subject Analysis
**Question:** Which students and subjects need review?

| Visual | Type | Fields / measures | Filters |
|---|---|---|---|
| Top 10 students | Table | Student_ID, Student_Name, [Student Aggregate Marks], [Student Ranking] | Top 10 by aggregate; dense rank preserves ties |
| Subject performance | Bar chart | Subject_Name, [Subject Average Marks] | Department/semester/section |
| Subject pass/fail | Matrix | Department rows, Subject_Name columns, [Pass Percentage], [Fail Count] | Cohort and subject |
| Student subject detail | Table | Subject_Name, Total_Marks, Grade, Result, Attendance_Percentage | Drill-through by Student_ID |

**Drill-through:** create a Student Detail page; add Dim_Student[Student_ID] to the Drill-through well; show student name, subject results and attendance; enable Keep all filters; add Insert → Buttons → Back.

## Page 3 — Attendance and Academic Risk
**Question:** Who is below the configured threshold, and how do attendance and marks vary together?

| Visual | Type | Fields / measures | Filters |
|---|---|---|---|
| Average attendance | Card | [Average Attendance] | Cohort filters |
| Low attendance count | Card | [Low Attendance Count] | Configured Business_Rules threshold |
| Low attendance list | Table | Student_ID, Student_Name, average attendance | Below [Attendance Threshold] |
| Attendance vs marks | Scatter | X Attendance_Percentage; Y Total_Marks; Details Student_ID; Legend Department | PRESENT marks; matching student-subject-term rows |
| Attendance by subject | Bar chart | Subject_Name, average Attendance_Percentage | Cohort and term |
| Attendance distribution | Histogram/column | Attendance_Percentage bins, student count | Cohort and subject |

Do not interpret correlation as causation. These are synthetic observational records.

## Slicers and refresh
1. Insert slicers for Academic_Year, Semester, Department, Section and Subject.
2. Sync the cohort slicers across pages.
3. Check Edit interactions for every slicer and visual.
4. Test a department, semester, section and subject selection.
5. Clear all filters and compare headline KPIs to `reports/analysis_summary.md`.
6. Refresh after replacing CSVs and confirm data types/relationships.

## Acceptance checks
- Headline measures reconcile with Python for identical filters.
- Dense ranking preserves ties and Topper returns all tied names.
- Low Attendance Count reads the imported threshold.
- ABSENT/MISSING are not zero.
- No direct fact-to-fact relationship or accidental row multiplication exists.
- Every page identifies the data as synthetic.
- Save as `powerbi/Student_Performance_Dashboard.pbix` and export genuine screenshots to `powerbi/screenshots/`.

## Completion status
This guide is implementation-ready, but it is not a PBIX. Power BI Desktop must create, save, refresh and inspect the actual report.
