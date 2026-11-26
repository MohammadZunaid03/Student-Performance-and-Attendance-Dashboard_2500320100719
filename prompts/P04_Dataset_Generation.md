# P4 — Dataset Research and Generation

Design datasets for Student Performance and Attendance Dashboard.

First identify three relevant public datasets, giving source, direct URL, licence, columns and limitations. If none adequately combines marks and attendance, choose reproducible synthetic data and explain why.

Synthetic data design:
- Students: Student_ID, Student_Name, Department, Semester, Section
- Subjects: Subject_ID, Subject_Name, Subject_Code, Maximum_Marks, Passing_Marks
- Attendance: Attendance_ID, Student_ID, Subject_ID, Total_Classes, Present_Classes, Absent_Classes, Attendance_Percentage
- Marks: Marks_ID, Student_ID, Subject_ID, Internal_Marks, External_Marks, Total_Marks, Grade, Result
- Academic_Terms: Term_ID, Academic_Year, Semester, Start_Date, End_Date

Generate approximately 200 fictional students with multiple subjects and linked attendance/marks records. Use a fixed random seed. Include documented examples of absence, low attendance, boundary marks, duplicates, missing values, invalid values and inconsistent text in raw files. Preserve synthetic-data disclosure. Specify table columns, types and expected row counts. Ensure reproducibility and meaningful foreign-key relationships.

**Output:** `src/01_generate_data.py`, `data/raw/*.csv`, and `docs/Dataset_Design.md`.