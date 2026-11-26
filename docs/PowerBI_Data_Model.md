# Power BI Data Model and DAX

## Import and relationships
1. In Power BI Desktop select Get Data → Text/CSV and import the cleaned CSV files from data/clean.
2. In Power Query confirm IDs are Text, marks/counts are Whole Number or Decimal Number, dates are Date, and null marks remain null. Select Close & Apply.
3. Create one-to-many, single-direction relationships:
   - Dim_Student[Student_ID] → Fact_Marks[Student_ID] and Fact_Attendance[Student_ID]
   - Dim_Subject[Subject_ID] → both fact tables
   - Dim_Academic_Term[Term_ID] → both fact tables
4. Do not create a direct relationship between Fact_Marks and Fact_Attendance. Both facts share conformed dimensions and have the same student-subject-term grain in this sample.
5. Create a calendar table only if date-level events are added. Current attendance and marks CSVs are term-level aggregates, not daily records.

## Recommended semantic model
Use the Oracle star schema in sql/schema.sql for a production-shaped model. For a CSV prototype, create Power Query dimension queries by referencing distinct student/subject/term tables and merge source IDs into facts, or use source IDs directly as dimension keys. Do not mix surrogate and natural keys.

## DAX measures
Assumptions: pass rate denominator includes PRESENT scored records only; ABSENT and MISSING are excluded from the scored pass-rate denominator and displayed separately. Low attendance is a provisional 75% threshold and must be confirmed.

```dax
Total Students = DISTINCTCOUNT(Dim_Student[Student_ID])

Scored Records =
CALCULATE(COUNTROWS(Fact_Marks), Fact_Marks[Record_Status] = "PRESENT")

Total Marks =
CALCULATE(SUM(Fact_Marks[Total_Marks]), Fact_Marks[Record_Status] = "PRESENT")

Average Marks =
DIVIDE([Total Marks], [Scored Records])

Pass Count =
CALCULATE(COUNTROWS(Fact_Marks), Fact_Marks[Result] = "PASS")

Fail Count =
CALCULATE(COUNTROWS(Fact_Marks), Fact_Marks[Result] = "FAIL")

Pass Percentage =
DIVIDE([Pass Count], [Scored Records], 0) * 100

Average Attendance =
AVERAGE(Fact_Attendance[Attendance_Percentage])

Low Attendance Student Count =
COUNTROWS(
    FILTER(
        VALUES(Dim_Student[Student_ID]),
        CALCULATE(AVERAGE(Fact_Attendance[Attendance_Percentage])) < 75
    )
)

Subject Average Marks =
CALCULATE(AVERAGE(Fact_Marks[Total_Marks]), Fact_Marks[Record_Status] = "PRESENT")

Student Aggregate Marks =
CALCULATE([Total Marks], ALLEXCEPT(Dim_Student, Dim_Student[Student_ID]))

Student Rank =
RANKX(ALLSELECTED(Dim_Student[Student_ID]), [Student Aggregate Marks], , DESC, DENSE)

Topper =
VAR TopScore =
    MAXX(ALLSELECTED(Dim_Student[Student_ID]), [Student Aggregate Marks])
RETURN
    CONCATENATEX(
        FILTER(ALLSELECTED(Dim_Student), [Student Aggregate Marks] = TopScore),
        Dim_Student[Student_Name], ", "
    )

Absent Records =
CALCULATE(COUNTROWS(Fact_Marks), Fact_Marks[Record_Status] = "ABSENT")

Missing Marks Records =
CALCULATE(COUNTROWS(Fact_Marks), Fact_Marks[Record_Status] = "MISSING")
```

## Measure notes
- Total Students counts distinct students in current filter context.
- Scored Records counts present/scored student-subject rows.
- Total Marks sums valid scored totals.
- Average Marks is mean marks per scored subject record, not a student's percentage.
- Pass Count and Fail Count count scored subject outcomes.
- Pass Percentage uses scored records as denominator.
- Average Attendance averages student-subject attendance percentages; for weighted attendance use total present / total classes instead.
- Low Attendance Student Count counts students whose average subject attendance is below 75%.
- Subject Average Marks is affected by the selected subject and cohort filters.
- Student Aggregate Marks sums scored subject marks for the current student.
- Student Rank uses dense ranking and preserves ties.
- Topper returns all names tied at the top score.
- Absent and Missing Marks Records are shown separately and are not treated as zero.

## Validation
Compare every KPI with Python/Oracle for the same cohort, subject and term filters. If the institutional policy uses a different denominator, threshold or grade scheme, update the single business-rule definition and all implementations together.
