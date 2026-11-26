-- PL/SQL package smoke and boundary tests.
-- Run after schema, loader and package compilation:
-- @sql/plsql/test_academic_analytics_pkg.sql

SET SERVEROUTPUT ON;

DECLARE
    v_grade VARCHAR2(5);
    v_pct NUMBER;
    v_rows SYS_REFCURSOR;
    v_student_id VARCHAR2(20);
    v_student_name VARCHAR2(120);
    v_subject_name VARCHAR2(120);
    v_total NUMBER;
    v_passing NUMBER;
    v_result VARCHAR2(10);
    v_classified_grade VARCHAR2(5);
    v_status VARCHAR2(10);
    v_rank NUMBER;
    v_count NUMBER := 0;
BEGIN
    -- Validate every configured grade-band boundary from the database.
    FOR band IN (SELECT grade_code, minimum_score FROM dim_grade_band) LOOP
        v_grade := academic_analytics_pkg.fn_grade(band.minimum_score);
        IF v_grade <> band.grade_code THEN
            RAISE_APPLICATION_ERROR(-20101, 'Grade boundary mismatch: ' || band.grade_code);
        END IF;
    END LOOP;

    v_pct := academic_analytics_pkg.fn_student_percentage('STU001');
    IF v_pct IS NULL OR v_pct < 0 OR v_pct > 100 THEN
        RAISE_APPLICATION_ERROR(-20102, 'Student percentage outside 0..100');
    END IF;

    academic_analytics_pkg.pr_classify_results(v_rows);
    LOOP
        FETCH v_rows INTO v_student_id, v_student_name, v_subject_name,
                          v_total, v_passing, v_result, v_classified_grade, v_status;
        EXIT WHEN v_rows%NOTFOUND;
        v_count := v_count + 1;
        IF v_status = 'ABSENT' AND (v_result <> 'ABSENT' OR v_total IS NOT NULL) THEN
            RAISE_APPLICATION_ERROR(-20103, 'ABSENT handling failed');
        ELSIF v_status = 'MISSING' AND (v_result <> 'MISSING' OR v_total IS NOT NULL) THEN
            RAISE_APPLICATION_ERROR(-20104, 'MISSING handling failed');
        ELSIF v_status = 'PRESENT' AND v_result <> CASE WHEN v_total >= v_passing THEN 'PASS' ELSE 'FAIL' END THEN
            RAISE_APPLICATION_ERROR(-20105, 'PASS/FAIL classification failed');
        END IF;
    END LOOP;
    CLOSE v_rows;

    academic_analytics_pkg.pr_rank_students(v_rows);
    FETCH v_rows INTO v_student_id, v_student_name, v_total, v_rank;
    IF v_rows%NOTFOUND OR v_rank <> 1 THEN
        RAISE_APPLICATION_ERROR(-20106, 'Ranking procedure did not return rank 1');
    END IF;
    CLOSE v_rows;

    academic_analytics_pkg.pr_low_attendance(v_rows);
    CLOSE v_rows;

    academic_analytics_pkg.pr_student_summary('STU001', v_rows);
    CLOSE v_rows;

    DBMS_OUTPUT.PUT_LINE('PASS: PL/SQL package smoke checks completed; classified rows=' || v_count);
EXCEPTION
    WHEN OTHERS THEN
        IF v_rows%ISOPEN THEN CLOSE v_rows; END IF;
        RAISE;
END;
/
