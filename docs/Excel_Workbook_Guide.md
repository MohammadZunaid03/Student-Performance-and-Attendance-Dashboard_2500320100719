# Excel verification workbook guide

Run `python src/05_build_excel_workbook.py` after cleaning. The script creates the workbook with raw/cleaned data tables, student summary, attendance and subject analysis, dashboard formulas, a chart and a reconciliation sheet.

## Complete the native Excel features
1. Open excel/Student_Performance_Analysis.xlsx in Microsoft Excel.
2. Select each table and use Insert → PivotTable for cohort/subject summaries.
3. Add slicers for Department, Semester, Section and Subject where the PivotTable fields permit.
4. Connect slicers to related PivotTables using Report Connections.
5. Refresh all PivotTables after replacing source data.
6. Populate Python Result and Oracle SQL Result in Validation only from executed reports; MATCH is not pre-filled.
7. Save the workbook after refreshing formulas and checking totals.

The openpyxl-generated workbook does not claim to contain native PivotTables or slicer objects. Those must be added in desktop Excel.
