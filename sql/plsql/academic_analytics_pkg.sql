-- Oracle PL/SQL package for Student Performance and Attendance Dashboard.
-- Grade bands are provisional synthetic demonstration rules. Confirm policy first.

CREATE OR REPLACE PACKAGE academic_analytics_pkg AS
  FUNCTION fn_grade(p_total_marks NUMBER) RETURN VARCHAR2;
  FUNCTION fn_student_percentage(p_student_id VARCHAR2) RETURN NUMBER;
  PROCEDURE pr_refresh_results;
  PROCEDURE pr_low_attendance(
    p_threshold IN NUMBER,
    p_rows OUT SYS_REFCURSOR
  );
  PROCEDURE pr_rank_students(p_rows OUT SYS_REFCURSOR);
  PROCEDURE pr_student_summary(
    p_student_id IN VARCHAR2,
    p_rows OUT SYS_REFCURSOR
  );
END academic_analytics_pkg;
/

CREATE OR REPLACE PACKAGE BODY academic_analytics_pkg AS

  FUNCTION fn_grade(p_total_marks NUMBER) RETURN VARCHAR2 IS
  BEGIN
    IF p_total_marks IS NULL THEN RETURN 'NA';
    ELSIF p_total_marks >= 90 THEN RETURN 'A+';
    ELSIF p_total_marks >= 80 THEN RETURN 'A';
    ELSIF p_total_marks >= 70 THEN RETURN 'B';
    ELSIF p_total_marks >= 60 THEN RETURN 'C';
    ELSIF p_total_marks >= 50 THEN RETURN 'D';
    ELSIF p_total_marks >= 40 THEN RETURN 'E';
    ELSE RETURN 'F';
    END IF;
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

  PROCEDURE pr_refresh_results IS
  BEGIN
    UPDATE fact_marks
       SET result = CASE
                      WHEN record_status = 'ABSENT' THEN 'ABSENT'
                      WHEN record_status = 'MISSING' THEN 'MISSING'
                      WHEN total_marks >= (SELECT ds.passing_marks
                                             FROM dim_subject ds
                                            WHERE ds.subject_key = fact_marks.subject_key) THEN 'PASS'
                      ELSE 'FAIL'
                    END,
           grade = CASE
                     WHEN record_status = 'ABSENT' THEN 'AB'
                     WHEN record_status = 'MISSING' THEN 'NA'
                     ELSE academic_analytics_pkg.fn_grade(total_marks)
                   END;
    COMMIT;
  EXCEPTION
    WHEN OTHERS THEN
      ROLLBACK;
      RAISE;
  END pr_refresh_results;

  PROCEDURE pr_low_attendance(p_threshold IN NUMBER, p_rows OUT SYS_REFCURSOR) IS
  BEGIN
    IF p_threshold < 0 OR p_threshold > 100 THEN
      RAISE_APPLICATION_ERROR(-20001, 'Attendance threshold must be between 0 and 100');
    END IF;
    OPEN p_rows FOR
      SELECT st.student_id, st.student_name,
             ROUND(AVG(a.attendance_percentage), 2) average_attendance
        FROM fact_attendance a
        JOIN dim_student st ON st.student_key = a.student_key
       GROUP BY st.student_id, st.student_name
      HAVING AVG(a.attendance_percentage) < p_threshold
       ORDER BY average_attendance;
  END pr_low_attendance;

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

  PROCEDURE pr_student_summary(p_student_id IN VARCHAR2, p_rows OUT SYS_REFCURSOR) IS
  BEGIN
    OPEN p_rows FOR
      SELECT st.student_id, st.student_name, sub.subject_name,
             m.total_marks, m.grade, m.result, a.attendance_percentage
        FROM dim_student st
        JOIN fact_marks m ON m.student_key = st.student_key
        JOIN dim_subject sub ON sub.subject_key = m.subject_key
        LEFT JOIN fact_attendance a
          ON a.student_key = m.student_key
         AND a.subject_key = m.subject_key
         AND a.term_key = m.term_key
       WHERE st.student_id = p_student_id
       ORDER BY sub.subject_name;
  END pr_student_summary;

END academic_analytics_pkg;
/
