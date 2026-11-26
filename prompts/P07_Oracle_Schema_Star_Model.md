# P7 — Oracle Database and Star Schema

Design a relational database and star schema for the student analytics project.

Fact tables: Fact_Marks and Fact_Attendance. Dimensions: Dim_Student, Dim_Subject, Dim_Date and Dim_Academic_Term.

Provide grain definition for every fact/dimension, ER and star-schema diagrams, primary/foreign keys, Oracle data types, NOT NULL/CHECK/UNIQUE constraints, indexes and executable CREATE TABLE statements.

Rules: attendance percentage 0–100; marks cannot exceed maximum; present classes cannot exceed total; every fact row references valid dimensions. Explicitly explain how to avoid double-counting when marks and attendance have different grains. Handle absent/missing marks separately.

**Output:** `sql/schema.sql`, `docs/star_schema.png`, `docs/database_design.md`.