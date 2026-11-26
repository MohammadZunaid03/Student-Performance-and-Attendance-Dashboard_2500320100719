# PL/SQL implementation guide

Run the script after loading the schema and data:
`sqlplus user/password@service @sql/plsql/academic_analytics_pkg.sql`

## Package contents
- FN_GRADE: returns a grade using the provisional synthetic bands (A+ 90+, A 80–89, B 70–79, C 60–69, D 50–59, E 40–49, F below 40).
- FN_STUDENT_PERCENTAGE: computes scored marks divided by maximum marks for a student; absent and missing records are excluded.
- PR_REFRESH_RESULTS: refreshes PASS/FAIL/ABSENT/MISSING and grade labels in FACT_MARKS. It commits on success and rolls back/re-raises on error.
- PR_LOW_ATTENDANCE: opens a reference cursor of students whose average subject attendance is below the supplied threshold.
- PR_RANK_STUDENTS: returns dense ranks so equal aggregate marks receive the same rank.
- PR_STUDENT_SUMMARY: returns subject marks, result, grade and attendance for one student.

## Example calls
```sql
SET SERVEROUTPUT ON;
DECLARE
  v_pct NUMBER;
  v_rows SYS_REFCURSOR;
  v_id VARCHAR2(20);
  v_name VARCHAR2(120);
  v_avg NUMBER;
BEGIN
  academic_analytics_pkg.pr_refresh_results;
  v_pct := academic_analytics_pkg.fn_student_percentage('STU001');
  DBMS_OUTPUT.PUT_LINE('STU001 percentage=' || NVL(TO_CHAR(v_pct), 'N/A'));

  academic_analytics_pkg.pr_low_attendance(75, v_rows);
  LOOP
    FETCH v_rows INTO v_id, v_name, v_avg;
    EXIT WHEN v_rows%NOTFOUND;
    DBMS_OUTPUT.PUT_LINE(v_id || ' ' || v_name || ' ' || v_avg);
  END LOOP;
  CLOSE v_rows;
END;
/
```

## Important policy caveat
The 40/60 component split, passing score 40 and grade bands are synthetic demonstration settings. The attendance threshold of 75% is also provisional. Confirm institutional regulations before using this package for real academic decisions. Missing marks are not treated as zero. The package has not been represented as executed against a live Oracle instance; compile and test it in the target Oracle environment.
