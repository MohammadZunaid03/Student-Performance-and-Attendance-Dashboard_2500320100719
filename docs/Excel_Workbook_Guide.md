# Excel verification workbook guide

## Generate the workbook
Run the cleaning pipeline first, then:
```bash
python src/05_build_excel_workbook.py
```
Outputs:
- `excel/Student_Performance_Analysis.xlsx`
- `docs/Data_Dictionary.xlsx`

The workbook contains the required Raw_Data, Cleaned_Data, Student_Summary, Attendance_Analysis, Subject_Analysis, Dashboard and Validation sheets, plus separate raw source tabs, Business_Rules, Grade_Bands and Data_Quality_Checks.

## Formula checks already included
- Student ranking uses Excel RANK.EQ; equal aggregate marks receive equal rank.
- Topper status uses IF on rank.
- Dashboard KPIs use COUNTA, AVERAGEIF and COUNTIF/COUNTIFS.
- Attendance analysis includes recalculated absent classes and attendance percentage for independent comparison.
- Validation compares Python results with Excel formula outputs and leaves Oracle SQL Result blank until actual Oracle query values are supplied. Match Status remains PENDING until Oracle values are entered.
- Business_Rules and Grade_Bands sheets are exported from the canonical config/business_rules.json assumptions.

## Add native PivotTables and slicers in Excel Desktop
1. Open `excel/Student_Performance_Analysis.xlsx`.
2. Select the CleanedMarks table → Insert → PivotTable → New Worksheet.
3. Build a subject summary with Subject_Name in Rows, Average of Total_Marks in Values, and Result in Columns. Filter Record_Status to PRESENT.
4. Build a department summary with Department in Rows and Average of Total_Marks / Count of Result in Values.
5. Build an attendance summary with Student_Name or Student_ID in Rows and Average of Attendance_Percentage in Values.
6. Select each PivotTable → PivotTable Analyze → Insert Slicer.
7. Add Department, Semester, Section and Subject slicers where the source fields are available.
8. For related PivotTables, select a slicer → Slicer → Report Connections and tick the relevant PivotTables.
9. Use Data → Refresh All after replacing source data.
10. Check the Validation sheet against the Python report and actual Oracle SQL exports; never type guessed Oracle values.

## Review checklist
- Raw and cleaned tables are distinct and preserved.
- Duplicate/missing checks agree with reports/data_quality_log.csv and quarantine CSVs.
- Absent and missing marks remain null and separate.
- Attendance recalculations match the accepted clean data.
- Pass/fail and grade values match the canonical configuration and subject Passing_Marks.
- RANK.EQ and topper flags preserve ties.
- No MATCH status is claimed while Oracle SQL values are blank.

## Limitation
The generator creates structured Excel tables, formulas and charts. Native PivotTables and slicer objects must be added and saved in Excel Desktop; the generated workbook does not claim those desktop objects already exist.
