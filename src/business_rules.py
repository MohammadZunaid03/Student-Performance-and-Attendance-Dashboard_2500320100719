"""Load the single project-wide business-rule configuration."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "business_rules.json"


def load_business_rules():
    with CONFIG_PATH.open(encoding="utf-8") as handle:
        rules = json.load(handle)
    threshold = float(rules["attendance_threshold_pct"])
    if not 0 <= threshold <= 100:
        raise ValueError("attendance_threshold_pct must be between 0 and 100")
    components = rules["assessment_components"]
    if int(components["internal_max"]) + int(components["external_max"]) != int(components["total_max"]):
        raise ValueError("Internal and external maxima must sum to total_max")
    bands = rules["grade_bands"]
    if not bands or sorted(int(x["min_score"]) for x in bands) != sorted(set(int(x["min_score"]) for x in bands)):
        raise ValueError("Grade band minimum scores must be unique")
    if min(int(x["min_score"]) for x in bands) != 0:
        raise ValueError("Grade bands must include a zero minimum")
    return rules


RULES = load_business_rules()
