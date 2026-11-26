"""Export the canonical JSON business rules for Power BI and review.

Run: python src/07_export_business_rules.py
The JSON file remains the single source of truth.
"""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "config" / "business_rules.json"


def main():
    rules = json.loads(SOURCE.read_text(encoding="utf-8"))
    config_path = ROOT / "config" / "business_rules.csv"
    grade_path = ROOT / "config" / "grade_bands.csv"
    with config_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["Rule_Key", "Numeric_Value", "Description"])
        writer.writeheader()
        writer.writerow({
            "Rule_Key": "ATTENDANCE_THRESHOLD_PCT",
            "Numeric_Value": rules["attendance_threshold_pct"],
            "Description": "Provisional attendance threshold percentage",
        })
        writer.writerow({
            "Rule_Key": "INTERNAL_MARKS_MAX",
            "Numeric_Value": rules["assessment_components"]["internal_max"],
            "Description": "Synthetic internal assessment maximum",
        })
        writer.writerow({
            "Rule_Key": "EXTERNAL_MARKS_MAX",
            "Numeric_Value": rules["assessment_components"]["external_max"],
            "Description": "Synthetic external assessment maximum",
        })
        writer.writerow({
            "Rule_Key": "TOTAL_MARKS_MAX",
            "Numeric_Value": rules["assessment_components"]["total_max"],
            "Description": "Synthetic total marks maximum",
        })
        writer.writerow({
            "Rule_Key": "PASSING_MARKS_DEFAULT",
            "Numeric_Value": rules["passing_marks_default"],
            "Description": "Synthetic default passing mark; subject-level value remains authoritative",
        })
    with grade_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["Grade", "Minimum_Score"])
        writer.writeheader()
        for band in rules["grade_bands"]:
            writer.writerow({"Grade": band["grade"], "Minimum_Score": band["min_score"]})
    print(f"Exported {config_path} and {grade_path} from {SOURCE}")


if __name__ == "__main__":
    main()
