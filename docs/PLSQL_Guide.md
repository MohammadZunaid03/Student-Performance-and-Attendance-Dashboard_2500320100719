# PL/SQL implementation guide

## Prerequisites
1. Run `sql/schema.sql` in Oracle Database 12c or later.
2. Run the Python cleaning and Oracle loader. The loader populates DIM_BUSINESS_RULE and DIM_GRADE_BAND from the single source `config/business_rules.json`.
3. Compile the package:
```sql
@sql/plsql/academic_analytics_pkg.sql
SHOW ERRORS PACKAGE academic_analytics_pkg;
SHOW ERRORS PACKAGE BODY academic_analytics_pkg;
```

## Package routines
- **FN_GRADE(total):** reads the applicable grade band from DIM_GRADE_BAND; no grade thresholds are duplicated in PL/SQL.
- **FN_STUDENT_PERCENTAGE(student_id):** scored marks divided by maximum possible marks for PRESENT records; ABSENT and MISSING are excluded.
- **PR_CLASSIFY_RESULTS(cursor):** returns calculated PASS/FAIL/ABSENT/MISSING and grade values without updating any fact rows.
- **PR_RANK_STUDENTS(cursor):** sums scored marks by student and uses DENSE_RANK, preserving ties.
- **PR_LOW_ATTENDANCE(cursor, threshold):** uses the supplied threshold if provided; otherwise reads ATTENDANCE_THRESHOLD_PCT from DIM_BUSINESS_RULE.
- **PR_STUDENT_SUMMARY(student_id, cursor):** returns subject results, attendance and term context for one student.

## Example test calls
```sql
SET SERVEROUTPUT ON;
DECLARE
  v_pct NUMBER;
  v_rows SYS_REFCURSOR;
  v_id VARCHAR2(20);
  v_name VARCHAR2(120);
  v_avg NUMBER;
BEGIN
  v_pct := academic_analytics_pkg.fn_student_percentage('STU001');
  DBMS_OUTPUT.PUT_LINE('STU001 percentage=' || NVL(TO_CHAR(v_pct), 'N/A'));

  academic_analytics_pkg.pr_low_attendance(v_rows);
  LOOP
    FETCH v_rows INTO v_id, v_name, v_avg;
    EXIT WHEN v_rows%NOTFOUND;
    DBMS_OUTPUT.PUT_LINE(v_id || ' ' || v_name || ' ' || v_avg);
  END LOOP;
  CLOSE v_rows;
END;
/
```

For grade function checks:
```sql
SELECT academic_analytics_pkg.fn_grade(95) grade_95,
       academic_analytics_pkg.fn_grade(40) grade_40,
       academic_analytics_pkg.fn_grade(39) grade_39
FROM dual;
```

## Business-rule source
Edit only `config/business_rules.json` to change attendance threshold, assessment maxima, passing mark default or grade bands. Re-run the data generator/cleaner as appropriate and reload Oracle to refresh its DIM_BUSINESS_RULE and DIM_GRADE_BAND rows. Power BI should import the matching exported configuration table.

## Safety and limitations
The package performs read-only classification and reporting. It does not update marks or student records. The package has not been claimed as executed until compiled and tested against the target Oracle instance. Do not use provisional demo rules for official academic decisions.
