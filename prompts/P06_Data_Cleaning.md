# P6 — Data Cleaning and Preprocessing

Build a reproducible Python/Pandas cleaning pipeline.

Input: `data/raw/`; output: `data/clean/`.

Requirements: detect duplicates using documented keys; identify missing required IDs; handle missing marks/attendance transparently; correct or quarantine invalid marks; standardize inconsistent text; recalculate attendance; validate attendance 0–100 and marks against maximum; distinguish absent marks from missing marks; validate referential integrity.

Never silently delete records or invent values. Retain rejected/quarantined rows with reasons. Log Issue, Rule Applied, Rows Affected, Before and After; explain every rule. Make reruns safe and deterministic.

**Output:** `src/02_clean_data.py`, `data/clean/`, `reports/data_quality_log.csv`, `docs/Cleaning_Rules.md`.