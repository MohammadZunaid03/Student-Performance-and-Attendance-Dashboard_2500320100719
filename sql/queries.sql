-- Q1. Top 10 students by total marks; DENSE_RANK preserves ties.
SELECT * FROM (
  SELECT s.student_id, s.student_name, SUM(m.total_marks) total_marks,
         DENSE_RANK() OVER (ORDER BY SUM(m.total_marks) DESC) rank_no
  FROM fact_marks m JOIN dim_student s ON s.student_key = m.student_key
  WHERE m.record_status = 'PRESENT'
  GROUP BY s.student_id, s.student_name
) WHERE rank_no <= 10
ORDER BY rank_no, student_id;

-- Q2. Student-wise percentage across valid scored subject records.
SELECT s.student_id, s.student_name,
       ROUND(SUM(m.total_marks) / NULLIF(SUM(sub.maximum_marks),0) * 100, 2) overall_percentage
FROM fact_marks m
JOIN dim_student s ON s.student_key = m.student_key
JOIN dim_subject sub ON sub.subject_key = m.subject_key
WHERE m.record_status = 'PRESENT'
GROUP BY s.student_id, s.student_name
ORDER BY overall_percentage DESC;

-- Q3. Subject-wise average marks.
SELECT sub.subject_name, ROUND(AVG(m.total_marks),2) average_marks,
       COUNT(m.total_marks) scored_records
FROM fact_marks m JOIN dim_subject sub ON sub.subject_key = m.subject_key
WHERE m.record_status = 'PRESENT'
GROUP BY sub.subject_name ORDER BY average_marks DESC;

-- Q4. Pass rate: PASS divided by scored PRESENT records; absent/missing are reported separately.
SELECT ROUND(100 * SUM(CASE WHEN result='PASS' THEN 1 ELSE 0 END) /
       NULLIF(SUM(CASE WHEN record_status='PRESENT' THEN 1 ELSE 0 END),0),2) pass_percentage,
       SUM(CASE WHEN result='PASS' THEN 1 ELSE 0 END) pass_records,
       SUM(CASE WHEN result='FAIL' THEN 1 ELSE 0 END) fail_records,
       SUM(CASE WHEN result='ABSENT' THEN 1 ELSE 0 END) absent_records,
       SUM(CASE WHEN result='MISSING' THEN 1 ELSE 0 END) missing_records
FROM fact_marks;

-- Q5. Students with one or more failed scored subjects.
SELECT s.student_id, s.student_name, COUNT(*) failed_subjects
FROM fact_marks m JOIN dim_student s ON s.student_key=m.student_key
WHERE m.result='FAIL'
GROUP BY s.student_id, s.student_name ORDER BY failed_subjects DESC;

-- Q6. Students below the provisional 75% attendance threshold.
-- Replace 75 with the institution-approved threshold before official use.
SELECT s.student_id, s.student_name, ROUND(AVG(a.attendance_percentage),2) average_attendance
FROM fact_attendance a JOIN dim_student s ON s.student_key=a.student_key
GROUP BY s.student_id, s.student_name
HAVING AVG(a.attendance_percentage) < (
           SELECT numeric_value FROM dim_business_rule
           WHERE rule_key = 'ATTENDANCE_THRESHOLD_PCT'
         )
ORDER BY average_attendance;

-- Q7. Attendance and marks at the shared student-subject-term grain.
SELECT s.student_id, sub.subject_name, a.attendance_percentage, m.total_marks, m.result
FROM fact_attendance a
JOIN fact_marks m ON m.student_key=a.student_key
 AND m.subject_key=a.subject_key AND m.term_key=a.term_key
JOIN dim_student s ON s.student_key=a.student_key
JOIN dim_subject sub ON sub.subject_key=a.subject_key
WHERE m.record_status='PRESENT'
ORDER BY s.student_id, sub.subject_name;

-- Q8. Subject failure rate among PRESENT scored records only.
SELECT sub.subject_name,
       ROUND(100 * SUM(CASE WHEN m.result='FAIL' THEN 1 ELSE 0 END) /
       NULLIF(COUNT(*),0),2) failure_percentage
FROM fact_marks m JOIN dim_subject sub ON sub.subject_key=m.subject_key
WHERE m.record_status='PRESENT'
GROUP BY sub.subject_name ORDER BY failure_percentage DESC;

-- Q9. Department-wise average marks and pass percentage.
SELECT s.department, ROUND(AVG(m.total_marks),2) average_marks,
       ROUND(100 * SUM(CASE WHEN m.result='PASS' THEN 1 ELSE 0 END) /
       NULLIF(COUNT(*),0),2) pass_percentage
FROM fact_marks m JOIN dim_student s ON s.student_key=m.student_key
WHERE m.record_status='PRESENT'
GROUP BY s.department ORDER BY average_marks DESC;

-- Q10. Show all students tied at the highest aggregate marks.
WITH totals AS (
  SELECT s.student_id, s.student_name, SUM(m.total_marks) total_marks
  FROM fact_marks m JOIN dim_student s ON s.student_key=m.student_key
  WHERE m.record_status='PRESENT'
  GROUP BY s.student_id, s.student_name
), ranked AS (
  SELECT totals.*, DENSE_RANK() OVER (ORDER BY total_marks DESC) rank_no FROM totals
)
SELECT student_id, student_name, total_marks, rank_no
FROM ranked WHERE rank_no=1 ORDER BY student_id;
