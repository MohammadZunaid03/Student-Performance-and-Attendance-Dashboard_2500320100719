-- Oracle PL/SQL package for Student Performance and Attendance Dashboard.
-- Business thresholds and grade bands are loaded from config/business_rules.json
-- by src/03_load_sql.py into DIM_BUSINESS_RULE and DIM_GRADE_BAND.

CREATE OR REPLACE PACKAGE academic_analytics_pkg AS
  FUNCTION fn_grade(p_total_marks NUMBER) RETURN VARCHAR2;
  FUNCTION fn_student_percentage(p_student_id VARCHAR2) RETURN NUMBER;
  PROCEDURE pr_classify_results(p_rows OUT SYS_REFCURSOR);
  PROCEDURE pr_rank_students(p_rows OUT SYS_REFCURSOR);
  PROCEDURE pr_low_attendance(
    p_rows OUT SYS_REFCURSOR,
    p_threshold IN NUMBER DEFAULT NULL
  );
  PROCEDURE pr_student_summary(
    p_student_id IN VARCHAR2,
    p_rows OUT SYS_REFCURSOR
  );
END academic_analytics_pkg;
/

CREATE OR REPLACE PACKAGE BODY academic_analytics_pkg AS

  FUNCTION fn_grade(p_total_marks NUMBER) RETURN VARCHAR2 IS
    v_grade VARCHAR2(5);
  BEGIN
    IF p_total_marks IS NULL THEN
      RETURN 'NA';
    END IF;
    SELECT grade_code
      INTO v_grade
      FROM dim_grade_band
     WHERE minimum_score = (
       SELECT MAX(minimum_score)
         FROM dim_grade_band
        WHERE minimum_score <= p_total_marks
     );
    RETURN v_grade;
  EXCEPTION
    WHEN NO_DATA_FOUND THEN
      RETURN 'NA';
  END fn_grade;

  FUNCTION fn_student_percentage(p_student_id VARCHAR2) RETURN NUMBER IS
    v_percentage NUMBER;
  BEGIN
    SELECT ROUND(SUM(m.total_marks) / NULLIF(SUM(s.maximum_marks), 0) * 100, 2)
      INTO v_percentage
      FROM fact_marks m
      JOIN dim_student st ON st.student_key = m.student_key
      JOIN dim_subject s ON s.subject_key = m.subject_key
     WHERE st.student_id = p_student_id
       AND m.record_status = 'PRESENT';
    RETURN v_percentage;
  END fn_student_percentage;

  -- Read-only classification: does not update source or warehouse facts.
  PROCEDURE pr_classify_results(p_rows OUT SYS_REFCURSOR) IS
  BEGIN
    OPEN p_rows FOR
      SELECT st.student_id, st.student_name, sub.subject_name,
             m.total_marks, sub.passing_marks,
             CASE
               WHEN m.record_status = 'ABSENT' THEN 'ABSENT'
               WHEN m.record_status = 'MISSING' THEN 'MISSING'
               WHEN m.total_marks >= sub.passing_marks THEN 'PASS'
               ELSE 'FAIL'
             END calculated_result,
             CASE
               WHEN m.record_status = 'ABSENT' THEN 'AB'
               WHEN m.record_status = 'MISSING' THEN 'NA'
               ELSE academic_analytics_pkg.fn_grade(m.total_marks)
             END calculated_grade,
             m.record_status
        FROM fact_marks m
        JOIN dim_student st ON st.student_key = m.student_key
        JOIN dim_subject sub ON sub.subject_key = m.subject_key
       ORDER BY st.student_id, sub.subject_name;
  END pr_classify_results;

  PROCEDURE pr_rank_students(p_rows OUT SYS_REFCURSOR) IS
  BEGIN
    OPEN p_rows FOR
      SELECT student_id, student_name, total_marks,
             DENSE_RANK() OVER (ORDER BY total_marks DESC) rank_no
        FROM (
          SELECT st.student_id, st.student_name, SUM(m.total_marks) total_marks
            FROM fact_marks m
            JOIN dim_student st ON st.student_key = m.student_key
           WHERE m.record_status = 'PRESENT'
           GROUP BY st.student_id, st.student_name
        )
       ORDER BY rank_no, student_id;
  END pr_rank_students;

  PROCEDURE pr_low_attendance(p_rows OUT SYS_REFCURSOR, p_threshold IN NUMBER DEFAULT NULL) IS
    v_threshold NUMBER;
  BEGIN
    IF p_threshold IS NULL THEN
      SELECT numeric_value
        INTO v_threshold
        FROM dim_business_rule
       WHERE rule_key = 'ATTENDANCE_THRESHOLD_PCT';
    ELSE
      v_threshold := p_threshold;
    END IF;
    IF v_threshold < 0 OR v_threshold > 100 THEN
      RAISE_APPLICATION_ERROR(-20001, 'Attendance threshold must be between 0 and 100');
    END IF;
    OPEN p_rows FOR
      SELECT st.student_id, st.student_name,
             ROUND(AVG(a.attendance_percentage), 2) average_attendance
        FROM fact_attendance a
        JOIN dim_student st ON st.student_key = a.student_key
       GROUP BY st.student_id, st.student_name
      HAVING AVG(a.attendance_percentage) < v_threshold
       ORDER BY average_attendance;
  END pr_low_attendance;

  PROCEDURE pr_student_summary(p_student_id IN VARCHAR2, p_rows OUT SYS_REFCURSOR) IS
  BEGIN
    OPEN p_rows FOR
      SELECT st.student_id, st.student_name, sub.subject_name,
             m.total_marks, m.grade, m.result, a.attendance_percentage,
             t.academic_year, t.semester_label
        FROM dim_student st
        JOIN fact_marks m ON m.student_key = st.student_key
        JOIN dim_subject sub ON sub.subject_key = m.subject_key
        JOIN dim_academic_term t ON t.term_key = m.term_key
        LEFT JOIN fact_attendance a
          ON a.student_key = m.student_key
         AND a.subject_key = m.subject_key
         AND a.term_key = m.term_key
       WHERE st.student_id = p_student_id
       ORDER BY t.academic_year, sub.subject_name;
  END pr_student_summary;

END academic_analytics_pkg;
/
