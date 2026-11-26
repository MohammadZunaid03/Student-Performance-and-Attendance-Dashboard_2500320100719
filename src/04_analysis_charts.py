"""Create reproducible charts and KPI summary from cleaned CSVs.

Run: python src/04_analysis_charts.py
"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from business_rules import RULES

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
REPORTS = ROOT / "reports"
CHARTS = REPORTS / "charts"
SUMMARY = REPORTS / "analysis_summary.md"


def load(name):
    path = CLEAN / name
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run src/02_clean_data.py first.")
    return pd.read_csv(path)


def save(fig, filename):
    fig.tight_layout()
    fig.savefig(CHARTS / filename, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main():
    CHARTS.mkdir(parents=True, exist_ok=True)
    students, subjects = load("students.csv"), load("subjects.csv")
    marks, attendance = load("marks.csv"), load("attendance.csv")
    scored = marks.loc[marks["Record_Status"].eq("PRESENT")].copy()
    scored["Total_Marks"] = pd.to_numeric(scored["Total_Marks"], errors="coerce")
    attendance["Attendance_Percentage"] = pd.to_numeric(attendance["Attendance_Percentage"], errors="coerce")

    # KPI denominator: scored PRESENT student-subject records only.
    pass_count = int(scored["Result"].eq("PASS").sum())
    fail_count = int(scored["Result"].eq("FAIL").sum())
    pass_rate = (pass_count / len(scored) * 100) if len(scored) else 0.0
    avg_marks = float(scored["Total_Marks"].mean()) if len(scored) else 0.0
    avg_attendance = float(attendance["Attendance_Percentage"].mean()) if len(attendance) else 0.0
    low_threshold = float(RULES["attendance_threshold_pct"])
    student_att = attendance.groupby("Student_ID")["Attendance_Percentage"].mean()
    low_attendance = student_att[student_att < low_threshold]
    low_attendance.rename("Average_Attendance_Percentage").to_csv(REPORTS / "low_attendance_students.csv")

    # 1. Marks distribution.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(scored["Total_Marks"].dropna(), bins=15, edgecolor="black")
    ax.set(title="Distribution of Student Marks", xlabel="Total marks (out of 100)", ylabel="Student-subject records")
    save(fig, "01_marks_distribution.png")

    # 2. Subject-wise average.
    subject_avg = scored.merge(subjects[["Subject_ID", "Subject_Name"]], on="Subject_ID")
    subject_avg = subject_avg.groupby("Subject_Name")["Total_Marks"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(9, 5))
    subject_avg.plot(kind="barh", ax=ax)
    ax.set(title="Subject-wise Average Marks", xlabel="Average marks", ylabel="Subject")
    save(fig, "02_subject_average.png")

    # 3. Pass/fail counts for scored records.
    result_counts = scored["Result"].value_counts().reindex(["PASS", "FAIL"], fill_value=0)
    fig, ax = plt.subplots(figsize=(7, 5))
    result_counts.plot(kind="bar", ax=ax)
    ax.set(title="Pass vs Fail (Scored Records)", xlabel="Result", ylabel="Records")
    save(fig, "03_pass_fail.png")

    # 4. Attendance distribution.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(attendance["Attendance_Percentage"].dropna(), bins=15, edgecolor="black")
    ax.axvline(low_threshold, linestyle="--", label=f"Provisional threshold: {low_threshold:.0f}%")
    ax.set(title="Attendance Percentage Distribution", xlabel="Attendance (%)", ylabel="Student-subject records")
    ax.legend()
    save(fig, "04_attendance_distribution.png")

    # 5. Attendance versus marks at the common student-subject grain.
    relation = scored.merge(
        attendance[["Student_ID", "Subject_ID", "Attendance_Percentage"]],
        on=["Student_ID", "Subject_ID"], how="inner", validate="one_to_one"
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(relation["Attendance_Percentage"], relation["Total_Marks"], alpha=0.65)
    ax.set(title="Attendance vs Academic Marks", xlabel="Attendance (%)", ylabel="Total marks")
    save(fig, "05_attendance_vs_marks.png")

    # 6. Top ten students by sum of scored marks; ties are not silently broken.
    student_totals = scored.groupby("Student_ID", as_index=False)["Total_Marks"].sum()
    student_totals = student_totals.merge(students[["Student_ID", "Student_Name"]], on="Student_ID")
    top = student_totals.sort_values(["Total_Marks", "Student_ID"], ascending=[False, True]).head(10)
    top.to_csv(REPORTS / "top_students.csv", index=False)
    pd.DataFrame([{"Pass_Records": pass_count, "Fail_Records": fail_count,
                   "Scored_Records": len(scored), "Pass_Percentage": round(pass_rate, 2),
                   "Absent_Records": int(marks["Record_Status"].eq("ABSENT").sum()),
                   "Missing_Records": int(marks["Record_Status"].eq("MISSING").sum())}]).to_csv(
        REPORTS / "pass_rate_summary.csv", index=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(top["Student_Name"][::-1], top["Total_Marks"][::-1])
    ax.set(title="Top 10 Students by Aggregate Scored Marks", xlabel="Aggregate marks", ylabel="Student")
    save(fig, "06_top_students.png")

    # 7. Subject-wise failure rate among scored PRESENT records only.
    subject_results = scored.merge(subjects[["Subject_ID", "Subject_Name"]], on="Subject_ID")
    subject_results["Is_Fail"] = subject_results["Result"].eq("FAIL").astype(int)
    failure = (subject_results.groupby("Subject_Name")["Is_Fail"].mean() * 100).sort_values()
    fig, ax = plt.subplots(figsize=(9, 5))
    failure.plot(kind="barh", ax=ax)
    ax.set(title="Subject-wise Failure Rate (Scored Records)", xlabel="Failure rate (%)", ylabel="Subject")
    save(fig, "07_subject_failure_rate.png")

    summary = [
        "# Analysis summary",
        "",
        "> This report is generated from synthetic demonstration data. It is not an institutional result.",
        "",
        "## KPI definitions",
        "- Pass rate = PASS / scored PRESENT marks records × 100; ABSENT and MISSING records are excluded.",
        "- Average marks = mean of valid PRESENT total marks.",
        "- Average attendance = mean of cleaned student-subject attendance percentages.",
        f"- Low attendance = student average below provisional {low_threshold:.1f}% threshold.",
        "",
        "## Calculated results",
        f"- Distinct students: {students['Student_ID'].nunique()}",
        f"- Scored student-subject records: {len(scored)}",
        f"- Average marks: {avg_marks:.2f}",
        f"- Average attendance: {avg_attendance:.2f}%",
        f"- Pass records: {pass_count}",
        f"- Fail records: {fail_count}",
        f"- Pass percentage: {pass_rate:.2f}%",
        f"- Students below provisional attendance threshold: {len(low_attendance)}",
        "",
        "## Subject summary",
        subject_avg.rename("average_marks").to_frame().to_markdown(),
        "",
        "## Notes",
        "- Missing and absent marks are not converted to zero.",
        "- The attendance threshold and grade rules are provisional demonstration settings.",
        "- Review quarantine outputs before treating any metric as final.",
    ]
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"Charts saved to {CHARTS}; summary saved to {SUMMARY}")


if __name__ == "__main__":
    main()
