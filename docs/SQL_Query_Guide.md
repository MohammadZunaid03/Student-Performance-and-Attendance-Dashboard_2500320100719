# Oracle SQL business-query guide

All queries are in `sql/queries.sql`. Execute them after schema creation and loading through `python src/03_load_sql.py`. Results are exported as `reports/sql_results/query_01.csv` through `query_10.csv`.

1. **Top 10 students:** sums PRESENT marks by student and uses DENSE_RANK. It includes every student tied within the top ten rank positions.
2. **Student-wise percentage:** divides each student's scored marks by the maximum possible marks for the same PRESENT subject records. ABSENT/MISSING records are excluded from both numerator and denominator.
3. **Subject average:** computes average total marks and scored record count per subject.
4. **Overall pass percentage:** PASS outcomes divided by PRESENT scored rows. It reports ABSENT and MISSING counts separately.
5. **Failed students:** counts failed subject outcomes per student; only scored FAIL records are included.
6. **Low attendance:** compares each student's mean subject attendance to ATTENDANCE_THRESHOLD_PCT from DIM_BUSINESS_RULE. This is the configured provisional threshold, not institutional policy.
7. **Attendance vs marks:** joins facts at student + subject + term grain, avoiding cross-product multiplication. Only PRESENT marks are included.
8. **Subject failure percentage:** failed PRESENT records divided by all PRESENT scored records for each subject.
9. **Department performance:** reports average marks and pass percentage by department for PRESENT scored rows.
10. **Tied toppers:** computes aggregate scored marks and DENSE_RANK, returning every student at rank 1.

## Denominator and grain safeguards
- A marks row and attendance row represent the same student-subject-term in this sample. Fact tables must not be joined only by Student_ID.
- Pass rate denominator is PRESENT scored records, not all students and not all source rows.
- Average attendance is the mean of subject-level attendance percentages. A weighted overall rate would instead use total present classes divided by total conducted classes.
- The synthetic dataset contains one term. The loader resolves each clean fact Term_ID to DIM_ACADEMIC_TERM. Do not load multiple terms until source facts have a reliable term mapping.
- All output files must be generated from an executed Oracle connection. Do not commit guessed SQL results.
