# Power BI Report Build Guide

## Page 1 — Academic Performance Overview
**Business question:** How is the selected cohort performing overall?
- Four KPI cards: Total Students, Average Marks, Pass Percentage and Average Attendance.
- Clustered column: pass/fail records by department.
- Bar chart: subject-wise average marks.
- Donut: PASS vs FAIL for scored records.
- Slicers: academic year/term, semester, department, section.
- Formatting: restrained palette, clear labels, percentage units, no truncated axes.

## Page 2 — Student and Subject Analysis
**Business question:** Which students and subjects need attention?
- Top 10 table: student ID, name, aggregate marks and dense rank.
- Bar chart: subject-wise average marks.
- Matrix: department/section by subject with average marks and pass percentage.
- Drill-through page or detail table by Student_ID showing subject marks, grade, result and attendance.
- Slicers: subject, department, semester and section.

## Page 3 — Attendance and Academic Risk
**Business question:** Which students fall below the attendance policy and how do attendance and marks compare?
- KPI: Average Attendance and Low Attendance Student Count.
- Table: student ID, name, average attendance and threshold status.
- Scatter: attendance percentage vs total marks at student-subject grain.
- Bar chart: average attendance by subject.
- Slicer: threshold (if implemented as a What-if parameter), term, department and semester.
- Keep ABSENT and MISSING marks distinct.

## Build steps
1. Load and model cleaned data using docs/PowerBI_Data_Model.md.
2. Create DAX measures and verify them against Python summary and Oracle query outputs.
3. Add each page and visuals as specified above.
4. Configure slicers to filter all relevant visuals.
5. Add drill-through using Student_ID; include a back button.
6. Add a page-level caption: synthetic demonstration data, last refresh date and threshold assumption.
7. Check interactions, sorting, blank handling and tie display.
8. Save as powerbi/Student_Performance_Dashboard.pbix.
9. Export page screenshots to powerbi/screenshots/ after the PBIX is built.

## Acceptance checks
- Every KPI responds to intended slicers.
- Topper visual includes ties.
- Low-attendance list uses the approved threshold.
- Missing and absent marks are not shown as zero.
- Python, SQL and Power BI values reconcile under identical filters.

**Limitation:** A PBIX is a binary Power BI Desktop artifact and must be created/saved in Power BI Desktop. This guide does not claim that a PBIX has already been built.
