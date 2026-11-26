"""Interactive five-section dashboard for the synthetic student analytics project.

Run from the repository root:
    python src/01_generate_data.py
    python src/02_clean_data.py
    streamlit run app/streamlit_app.py
"""
from datetime import datetime
from pathlib import Path
import json

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
RULES = json.loads((ROOT / "config" / "business_rules.json").read_text(encoding="utf-8"))

st.set_page_config(page_title="Student Performance & Attendance", page_icon="📊", layout="wide")
st.title("Student Performance and Attendance Dashboard")
st.caption(
    "Synthetic fictional demonstration data • "
    f"Last refreshed: {datetime.now().astimezone().strftime('%d %b %Y, %H:%M %Z')} • "
    "Not an official institutional result"
)


@st.cache_data
def load_data():
    required = ["students.csv", "subjects.csv", "academic_terms.csv", "marks.csv", "attendance.csv"]
    missing = [name for name in required if not (CLEAN / name).exists()]
    if missing:
        raise FileNotFoundError(
            "Missing cleaned files: " + ", ".join(missing) +
            ". Run python src/02_clean_data.py first."
        )
    return (
        pd.read_csv(CLEAN / "students.csv"),
        pd.read_csv(CLEAN / "subjects.csv"),
        pd.read_csv(CLEAN / "academic_terms.csv"),
        pd.read_csv(CLEAN / "marks.csv"),
        pd.read_csv(CLEAN / "attendance.csv"),
    )


try:
    students, subjects, terms, marks, attendance = load_data()
except Exception as exc:
    st.error(str(exc))
    st.stop()

st.sidebar.header("Cohort filters")
departments = sorted(students["Department"].dropna().unique().tolist())
semesters = sorted(students["Semester"].dropna().unique().tolist())
sections = sorted(students["Section"].dropna().unique().tolist())
subject_names = sorted(subjects["Subject_Name"].dropna().unique().tolist())
academic_years = sorted(terms["Academic_Year"].dropna().astype(str).unique().tolist())

selected_departments = st.sidebar.multiselect("Department", departments, default=departments)
selected_semesters = st.sidebar.multiselect("Semester", semesters, default=semesters)
selected_sections = st.sidebar.multiselect("Section", sections, default=sections)
selected_subject_names = st.sidebar.multiselect("Subject", subject_names, default=subject_names)
selected_years = st.sidebar.multiselect("Academic Year", academic_years, default=academic_years)

selected_term_ids = terms.loc[
    terms["Academic_Year"].astype(str).isin(selected_years), "Term_ID"
]
selected_subject_ids = subjects.loc[
    subjects["Subject_Name"].isin(selected_subject_names), "Subject_ID"
]
filtered_students = students[
    students["Department"].isin(selected_departments)
    & students["Semester"].isin(selected_semesters)
    & students["Section"].isin(selected_sections)
]
student_ids = filtered_students["Student_ID"]
filtered_marks = marks[
    marks["Student_ID"].isin(student_ids)
    & marks["Subject_ID"].isin(selected_subject_ids)
    & marks["Term_ID"].isin(selected_term_ids)
].copy()
filtered_attendance = attendance[
    attendance["Student_ID"].isin(student_ids)
    & attendance["Subject_ID"].isin(selected_subject_ids)
    & attendance["Term_ID"].isin(selected_term_ids)
].copy()

if filtered_students.empty or filtered_marks.empty or filtered_attendance.empty:
    st.warning("No records match the current filters. Select at least one department, semester, section, subject and academic year.")
    st.stop()

scored = filtered_marks[filtered_marks["Record_Status"].eq("PRESENT")].copy()
scored["Total_Marks"] = pd.to_numeric(scored["Total_Marks"], errors="coerce")
threshold = float(RULES["attendance_threshold_pct"])
pass_count = int(scored["Result"].eq("PASS").sum())
fail_count = int(scored["Result"].eq("FAIL").sum())
pass_rate = pass_count / len(scored) * 100 if len(scored) else 0.0
avg_marks = scored["Total_Marks"].mean()
avg_attendance = filtered_attendance["Attendance_Percentage"].mean()

student_totals = scored.groupby("Student_ID", as_index=False)["Total_Marks"].sum()
student_totals = student_totals.merge(
    filtered_students[["Student_ID", "Student_Name", "Department", "Semester", "Section"]],
    on="Student_ID", how="left", validate="one_to_one"
)
student_totals["Rank"] = student_totals["Total_Marks"].rank(
    method="dense", ascending=False
).astype("Int64")
attendance_by_student = filtered_attendance.groupby("Student_ID", as_index=False).agg(
    Attendance_Percentage=("Attendance_Percentage", "mean")
)
attendance_by_student = attendance_by_student.merge(
    filtered_students[["Student_ID", "Student_Name", "Department", "Semester", "Section"]],
    on="Student_ID", how="left", validate="one_to_one"
)
attendance_by_student["Attendance_Status"] = attendance_by_student["Attendance_Percentage"].apply(
    lambda value: "Below threshold" if value < threshold else "At/above threshold"
)
subject_summary = scored.merge(
    subjects[["Subject_ID", "Subject_Name"]], on="Subject_ID", how="left", validate="many_to_one"
).groupby("Subject_Name", as_index=False).agg(
    Average_Marks=("Total_Marks", "mean"),
    Scored_Records=("Total_Marks", "count"),
    Pass_Records=("Result", lambda values: int(values.eq("PASS").sum())),
    Fail_Records=("Result", lambda values: int(values.eq("FAIL").sum())),
)
subject_summary["Failure_Percentage"] = (
    subject_summary["Fail_Records"] / subject_summary["Scored_Records"] * 100
)

tabs = st.tabs([
    "Overview", "Student Performance", "Attendance Analysis",
    "Subject Analysis", "Student Ranking"
])

with tabs[0]:
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Students", f"{filtered_students['Student_ID'].nunique():,}")
    k2.metric("Average Marks", "—" if pd.isna(avg_marks) else f"{avg_marks:.2f}")
    k3.metric("Overall Pass Percentage", f"{pass_rate:.2f}%")
    k4.metric("Average Attendance", "—" if pd.isna(avg_attendance) else f"{avg_attendance:.2f}%")
    left, right = st.columns(2)
    with left:
        result_counts = pd.DataFrame({"Result": ["PASS", "FAIL"], "Records": [pass_count, fail_count]})
        st.plotly_chart(px.pie(result_counts, names="Result", values="Records", title="Pass / Fail Distribution"), use_container_width=True)
    with right:
        department_results = scored.merge(
            filtered_students[["Student_ID", "Department"]], on="Student_ID", how="left"
        ).groupby(["Department", "Result"]).size().reset_index(name="Records")
        st.plotly_chart(px.bar(department_results, x="Department", y="Records", color="Result",
                               barmode="group", title="Pass / Fail by Department"), use_container_width=True)

with tabs[1]:
    st.subheader("Student performance")
    st.plotly_chart(px.histogram(scored, x="Total_Marks", nbins=15, title="Marks Distribution"), use_container_width=True)
    st.dataframe(student_totals.sort_values(["Rank", "Student_ID"]), use_container_width=True, hide_index=True)

with tabs[2]:
    st.subheader("Attendance analysis")
    st.caption(f"Low-attendance threshold: {threshold:.1f}% (provisional configuration)")
    st.plotly_chart(px.histogram(attendance_by_student, x="Attendance_Percentage",
                                 color="Attendance_Status", title="Student Average Attendance"),
                    use_container_width=True)
    low = attendance_by_student[
        attendance_by_student["Attendance_Percentage"] < threshold
    ].sort_values("Attendance_Percentage")
    st.dataframe(low, use_container_width=True, hide_index=True)

with tabs[3]:
    st.subheader("Subject analysis")
    st.plotly_chart(px.bar(subject_summary, x="Subject_Name", y="Average_Marks",
                           title="Subject-wise Average Marks"), use_container_width=True)
    st.plotly_chart(px.bar(subject_summary, x="Subject_Name", y="Failure_Percentage",
                           title="Subject-wise Failure Percentage"), use_container_width=True)
    st.dataframe(subject_summary, use_container_width=True, hide_index=True)

with tabs[4]:
    st.subheader("Student ranking")
    st.caption("Dense ranking preserves equal aggregate marks.")
    st.dataframe(
        student_totals.loc[student_totals["Rank"] <= 10].sort_values(["Rank", "Student_ID"]),
        use_container_width=True, hide_index=True
    )
    selected_student = st.selectbox(
        "Student detail", filtered_students["Student_ID"].sort_values().tolist()
    )
    student_marks = filtered_marks[filtered_marks["Student_ID"].eq(selected_student)]
    student_attendance = filtered_attendance[filtered_attendance["Student_ID"].eq(selected_student)]
    detail = student_marks.merge(
        subjects[["Subject_ID", "Subject_Name"]], on="Subject_ID", how="left"
    ).merge(
        student_attendance[["Subject_ID", "Attendance_Percentage"]],
        on="Subject_ID", how="left", validate="one_to_one"
    )
    st.dataframe(
        detail[["Subject_Name", "Total_Marks", "Grade", "Result",
                "Record_Status", "Attendance_Percentage"]],
        use_container_width=True, hide_index=True
    )

st.sidebar.download_button(
    "Download filtered marks CSV", filtered_marks.to_csv(index=False),
    "filtered_marks.csv", "text/csv"
)
st.sidebar.download_button(
    "Download filtered attendance CSV", filtered_attendance.to_csv(index=False),
    "filtered_attendance.csv", "text/csv"
)
