"""Render a readable star-schema diagram from the documented project model."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
OUT_PNG = ROOT / "docs" / "star_schema.png"
OUT_SVG = ROOT / "docs" / "star_schema.svg"

NODES = {
    "DIM_STUDENT": (0.06, 0.67, 0.23, 0.15, "DIM_STUDENT\nstudent_key (PK)\nstudent_id (UK)\nname, department, semester, section"),
    "DIM_SUBJECT": (0.06, 0.37, 0.23, 0.15, "DIM_SUBJECT\nsubject_key (PK)\nsubject_id (UK)\nname, max marks, pass marks"),
    "DIM_ACADEMIC_TERM": (0.39, 0.84, 0.25, 0.12, "DIM_ACADEMIC_TERM\nterm_key (PK)\nterm_id (UK)\nacademic year, semester, dates"),
    "FACT_MARKS": (0.39, 0.55, 0.25, 0.17, "FACT_MARKS\nstudent_key (FK) • subject_key (FK)\nterm_key (FK)\ninternal, external, total, grade, result"),
    "FACT_ATTENDANCE": (0.72, 0.34, 0.24, 0.17, "FACT_ATTENDANCE\nstudent_key (FK) • subject_key (FK)\nterm_key (FK)\ntotal, present, absent, attendance %"),
    "DIM_DATE": (0.72, 0.78, 0.24, 0.12, "DIM_DATE\ndate_key (PK)\ncalendar date attributes"),
    "DIM_BUSINESS_RULE": (0.39, 0.12, 0.25, 0.11, "DIM_BUSINESS_RULE\nrule_key (PK) • numeric_value"),
    "DIM_GRADE_BAND": (0.72, 0.12, 0.24, 0.11, "DIM_GRADE_BAND\ngrade_code (PK) • minimum_score"),
}


def center(name):
    x, y, w, h, _ = NODES[name]
    return x + w / 2, y + h / 2


def draw_node(ax, node):
    x, y, w, h, label = NODES[node]
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.012",
        linewidth=1.3, edgecolor="#24415C", facecolor="#F2F6FA"
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
            fontsize=7.5, color="#172B3A", linespacing=1.35)


def connect(ax, source, target):
    sx, sy = center(source)
    tx, ty = center(target)
    arrow = FancyArrowPatch(
        (sx, sy), (tx, ty),
        arrowstyle="-|>", mutation_scale=10, linewidth=1.15,
        color="#52718A", connectionstyle="arc3,rad=0.0",
        shrinkA=42, shrinkB=42
    )
    ax.add_patch(arrow)


def main():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("Student Performance and Attendance — Oracle Star Schema",
                 fontsize=16, weight="bold", pad=18)
    for dim, fact in [
        ("DIM_STUDENT", "FACT_MARKS"),
        ("DIM_SUBJECT", "FACT_MARKS"),
        ("DIM_ACADEMIC_TERM", "FACT_MARKS"),
        ("DIM_STUDENT", "FACT_ATTENDANCE"),
        ("DIM_SUBJECT", "FACT_ATTENDANCE"),
        ("DIM_ACADEMIC_TERM", "FACT_ATTENDANCE"),
    ]:
        connect(ax, dim, fact)
    for name in NODES:
        draw_node(ax, name)
    ax.text(0.84, 0.70, "Calendar reference only:\ncurrent facts are term aggregates\n(no event date key)",
            ha="center", va="center", fontsize=8, color="#8A4B08")
    ax.text(0.52, 0.045, "Configuration tables are loaded from config/business_rules.json. "
            "No direct fact-to-fact join. Grain: Student × Subject × Term.",
            ha="center", va="center", fontsize=9, color="#333333")
    fig.tight_layout()
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, dpi=180, bbox_inches="tight")
    fig.savefig(OUT_SVG, bbox_inches="tight")
    plt.close(fig)
    print(f"Rendered {OUT_PNG} and {OUT_SVG}")


if __name__ == "__main__":
    main()
