"""Interactive Streamlit dashboard for synthetic student analytics.

Run from repository root: streamlit run app/streamlit_app.py
Run src/02_clean_data.py first.
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
st.set_page_config(page_title="Student Performance & Attendance", page_icon="📊", layout="wide")
st.title("Student Performance and Attendance Dashboard")
st.caption("Data source: project synthetic dataset (fictional demonstration records). Refresh by rerunning the data pipeline.")

@st.cache_data
def load_data():
    required = ["students.csv", "subjects.csv", "marks.csv", "attendance.csv"]
    missing = [name for name in required if not (CLEAN / name).exists()]
    if missing:
        raise FileNotFoundError("Missing cleaned files: " + ", ".join(missing) + ". Run python src/02_clean_data.py first.")
    return (
        pd.read_csv(CLEAN / "students.csv"),
        pd.read_csv(CLEAN / "subjects.csv"),
        pd.read_csv(CLEAN / "marks.csv"),
        pd.read_csv(CLEAN / "attendance.csv"),
    )

try:
    students, subjects, marks, attendance = load_data()
except Exception as exc:
    st.error(str(exc))
    st.stop()

st.sidebar.header("Filters")
departments = sorted(students["Department"].dropna().unique().tolist())
semesters = sorted(students["Semester"].dropna().unique().tolist())
sections = sorted(students["Section"].dropna().unique().tolist())
subject_names = sorted(subjects["Subject_Name"].dropna().unique().tolist())
selected_departments = st.sidebar.multiselect("Department", departments, default=departments)
selected_semesters = st.sidebar.multiselect("Semester", semesters, default=semesters)
selected_sections = st.sidebar.multiselect("Section", sections, default=sections)
selected_subject_names = st.sidebar.multiselect("Subject", subject_names, default=subject_names)

subject_ids = subjects.loc[subjects["Subject_Name"].isin(selected_subject_names), "Subject_ID"]
filtered_students = students[
    students["Department"].isin(selected_departments)
    & students["Semester"].isin(selected_semesters)
    & students["Section"].isin(selected_sections)
]
student_ids = filtered_students["Student_ID"]
filtered_marks = marks[marks["Student_ID"].isin(student_ids) & marks["Subject_ID"].isin(subject_ids)].copy()
filtered_attendance = attendance[attendance["Student_ID"].isin(student_ids) & attendance["Subject_ID"].isin(subject_ids)].copy()
scored = filtered_marks[filtered_marks["Record_Status"].eq("PRESENT")].copy()
scored["Total_Marks"] = pd.to_numeric(scored["Total_Marks"], errors="coerce")
pass_count = int(scored["Result"].eq("PASS").sum())
pass_rate = pass_count / len(scored) * 100 if len(scored) else 0.0
avg_marks = scored["Total_Marks"].mean()
avg_attendance = filtered_attendance["Attendance_Percentage"].mean()
low_threshold = 75.0  # Provisional demonstration threshold; confirm policy.

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Students", f"{filtered_students['Student_ID'].nunique():,}")
k2.metric("Average Marks", "—" if pd.isna(avg_marks) else f"{avg_marks:.2f}")
k3.metric("Pass Percentage", f"{pass_rate:.2f}%")
k4.metric("Average Attendance", "—" if pd.isna(avg_attendance) else f"{avg_attendance:.2f}%")

left, right = st.columns(2)
with left:
    result_counts = scored["Result"].value_counts().rename_axis("Result").reset_index(name="Records")
    st.plotly_chart(px.pie(result_counts, names="Result", values="Records", title="Pass / Fail Distribution"), use_container_width=True)
with right:
    subject_summary = scored.merge(subjects[["Subject_ID", "Subject_Name"]], on="Subject_ID")
    subject_summary = subject_summary.groupby("Subject_Name", as_index=False)["Total_Marks"].mean()
    st.plotly_chart(px.bar(subject_summary, x="Subject_Name", y="Total_Marks", title="Subject-wise Average Marks"), use_container_width=True)

attendance_by_student = filtered_attendance.groupby("Student_ID", as_index=False)["Attendance_Percentage"].mean()
attendance_by_student = attendance_by_student.merge(filtered_students[["Student_ID", "Student_Name"]], on="Student_ID")
attendance_by_student["Attendance_Status"] = attendance_by_student["Attendance_Percentage"].apply(
    lambda value: "Below threshold" if value < low_threshold else "At/above threshold"
)
st.plotly_chart(px.histogram(attendance_by_student, x="Attendance_Percentage", color="Attendance_Status",
                             title="Student Average Attendance"), use_container_width=True)

student_totals = scored.groupby("Student_ID", as_index=False)["Total_Marks"].sum()
student_totals = student_totals.merge(filtered_students[["Student_ID", "Student_Name"]], on="Student_ID")
student_totals["Rank"] = student_totals["Total_Marks"].rank(method="dense", ascending=False).astype("Int64")
st.subheader("Top 10 students")
st.dataframe(student_totals.sort_values(["Rank", "Student_ID"]).head(10), use_container_width=True, hide_index=True)

st.subheader("Students below provisional attendance threshold")
low = attendance_by_student[attendance_by_student["Attendance_Percentage"] < low_threshold].sort_values("Attendance_Percentage")
st.dataframe(low, use_container_width=True, hide_index=True)
st.download_button("Download filtered marks CSV", filtered_marks.to_csv(index=False), "filtered_marks.csv", "text/csv")
st.download_button("Download filtered attendance CSV", filtered_attendance.to_csv(index=False), "filtered_attendance.csv", "text/csv")
