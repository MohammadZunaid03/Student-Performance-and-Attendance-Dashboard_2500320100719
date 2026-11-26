# Final Academic Project Report
## Student Performance and Attendance Dashboard

**Author:** Mohammad Zunaid  
**Project domain:** Education / Academic Analytics  
**Repository:** https://github.com/MohammadZunaid03/Student-Performance-and-Attendance-Dashboard_2500320100719  
**Report basis:** GitHub Actions run 45820262431 (Python/BI-export/notebook/Excel/test pipeline successful).  
**Data classification:** Synthetic fictional demonstration data only.

## Abstract
The Student Performance and Attendance Dashboard is an academic analytics project designed to integrate student master data, subject information, marks, attendance and academic-term metadata. Python/Pandas performs data generation, cleaning, quarantine handling, KPI calculations and charts. Oracle SQL/PLSQL source implements a warehouse star schema and business queries. Streamlit provides a runnable interactive dashboard. Power BI DAX/report specifications and an Excel verification workbook support cross-tool reporting.

The project uses deterministic synthetic data because the public datasets reviewed do not provide the exact combination of subject-level internal/external marks and class attendance aggregates required by the defined warehouse grain. The Python pipeline, notebook, chart generation, Excel workbook generation, 20-record manual validation and automated test suite have passed in GitHub Actions. Oracle compilation/reconciliation and native Power BI/Excel Desktop authoring remain external verification tasks.

## 1. Problem statement
Student marks and attendance are often stored in separate records. Producing a consistent academic overview can require repeated manual joining and calculation. The project demonstrates a reproducible workflow that validates source records, calculates academic indicators, identifies low-attendance students and summarises subject performance.

## 2. Objectives
1. Process a sample of at least 200 fictional students and five subjects with 1,000 student-subject marks/attendance records.
2. Validate primary/foreign keys, score ranges, attendance counts, duplicates and missing values.
3. Calculate total marks, grade, PASS/FAIL, attendance percentage, student ranking and subject metrics using one documented business-rule configuration.
4. Independently check at least 20 student records.
5. Deliver a reproducible Python workflow, Oracle schema/query/package source, interactive dashboard, Power BI model/report design and Excel verification workbook.

## 3. Scope
**Included:** synthetic data generation; cleaning and quarantine; field-level dictionary; Oracle star-schema DDL; SQL/PLSQL source; Python EDA/charts; Jupyter notebook; Streamlit dashboard; Power BI DAX/report specification; Excel workbook/data dictionary; automated tests and documentation.

**Not claimed:** live college ERP integration, authorised institutional data, production deployment, official academic decision support, compiled Oracle package, completed Power BI PBIX, or native Excel PivotTables/slicers created in Excel Desktop.

## 4. Tools and technologies
Python 3.11, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, Oracle SQL, Oracle PL/SQL, python-oracledb, Power BI Desktop, DAX, Excel/openpyxl, pytest, Jupyter, GitHub Actions and Git.

## 5. Dataset design and provenance
The raw dataset contains:
- 201 student master rows (200 valid students plus one duplicate).
- 5 subject master rows.
- 1,001 marks rows (1,000 intended student-subject records plus one duplicate).
- 1,001 attendance rows (1,000 intended student-subject records plus one duplicate).
- 1 academic term.

The generated records are fictional and deterministic. Intentional test defects include duplicate master/fact rows, blank department, inconsistent name formatting, missing/absent marks, invalid record status, invalid score components, an ABSENT row with populated scores, impossible and fractional attendance counts, and blank attendance Student_ID. Exact mark boundary records cover 0, the default passing mark 40 and maximum 100.

Three public datasets were reviewed:
- UCI Student Performance (Cortez & Silva): includes grades and absence-related attributes, but not the subject attendance and internal/external split required here.
- Open University Learning Analytics Dataset: includes student/course/assessment and VLE data, but not the classroom attendance summary used by this project.
- Mendeley Students Academic Performance Evaluation dataset: includes survey-style attendance and academic indicators, but not the required subject-level fact structure.

None was a direct drop-in replacement for the required grain; the synthetic sample is used to test the complete pipeline. See docs/Public_Dataset_Research.md for licence, feature and fit comparison.

## 6. Data cleaning and quality results
The cleaning pipeline applies documented rules and retains rejected rows in quarantine files. The latest successful CI run produced:

| Dataset | Raw rows | Accepted clean rows | Quarantined rows |
|---|---:|---:|---:|
| Students | 201 | 200 | 1 |
| Subjects | 5 | 5 | 0 |
| Marks | 1,001 | 996 | 5 |
| Attendance | 1,001 | 997 | 4 |
| Academic terms | 1 | 1 | 0 |

Important treatments:
- One duplicate student and one duplicate marks/attendance record are quarantined.
- One blank department is standardised to UNKNOWN rather than inferred.
- Invalid/out-of-range marks, unknown status and ABSENT rows with populated components are quarantined.
- One valid ABSENT and one valid MISSING marks record are preserved with null score totals.
- Impossible, fractional and foreign-key-invalid attendance rows are quarantined.
- Absent classes and attendance percentage are recomputed for accepted rows.
- Clean fact files receive a derived Term_ID because the sample has exactly one valid term. The cleaner stops if multiple terms exist without a source term mapping.
- The quality log records issue, rule applied, affected row count, before condition and after treatment.

See the generated `reports/data_quality_log.csv` and quarantine CSVs in the GitHub Actions validation artifact.

## 7. Business rules and KPI definitions
The canonical source is `config/business_rules.json`. It currently defines provisional demonstration values: internal maximum 40, external maximum 60, total maximum 100, default passing mark 40, grade bands and attendance threshold 75%.

Subject-level Passing_Marks is authoritative for each subject. Grade bands and the attendance threshold are not official institutional policy.

| KPI | Definition |
|---|---|
| Average marks | Mean of PRESENT total marks only |
| Pass percentage | PASS / PRESENT scored marks records × 100 |
| Average attendance | Mean of cleaned student-subject attendance percentages |
| Low-attendance count | Students whose mean subject attendance is below configured threshold |
| Student aggregate rank | Sum of PRESENT subject marks; dense rank preserves ties |
| Subject average | Mean PRESENT total marks for that subject |
| Subject failure rate | FAIL / PRESENT scored records for that subject × 100 |
| ABSENT/MISSING | Separate statuses; neither is converted to zero |

## 8. Verified Python analysis results
The successful CI run produced these synthetic-data metrics:

| Metric | Result |
|---|---:|
| Distinct students | 200 |
| Subjects | 5 |
| Scored student-subject records | 994 |
| Average marks | 61.44 / 100 |
| Average attendance | 85.07% |
| PASS records | 853 |
| FAIL records | 141 |
| Pass percentage | 85.81% |
| Students with at least one failed subject | 59 |
| ABSENT records | 1 |
| MISSING records | 1 |
| Students below provisional 75% attendance | 1 |
| Low-attendance student | STU178 (73.00% average) |
| Attendance/marks Pearson correlation | -0.034 (descriptive only) |

Subject averages:
- Highest average: Computer Networks — 62.21.
- Lowest average: Data Structures — 60.45.
- Highest subject failure rate: Mathematics for Computing — 16.08%.

These results describe only the synthetic sample. The weak negative correlation does not establish causation and must not be interpreted as an institutional finding.

## 9. System architecture and data model
Workflow:
1. Generate raw CSV files.
2. Clean, validate and quarantine source rows.
3. Attach the validated term key to clean facts.
4. Calculate Python KPIs and charts.
5. Load dimensions and facts into Oracle when credentials/schema are configured.
6. Export ten SQL business-query result CSVs.
7. Display the same KPI definitions through Streamlit, Power BI and Excel.

Oracle dimensions: DIM_STUDENT, DIM_SUBJECT, DIM_ACADEMIC_TERM, DIM_DATE, DIM_BUSINESS_RULE and DIM_GRADE_BAND.

Oracle facts:
- FACT_MARKS: one student × subject × term marks result.
- FACT_ATTENDANCE: one student × subject × term attendance aggregate.

Do not join the two fact tables only by Student_ID. DIM_DATE is a calendar reference dimension; the current facts are term-level aggregates with no event date, so no daily date relationship is claimed.

See sql/schema.sql, docs/database_design.md and docs/star_schema.mmd.

## 10. Python implementation
- `src/01_generate_data.py`: deterministic raw dataset generator.
- `src/02_clean_data.py`: validation, cleaning, derived fields, quarantine and quality log.
- `src/04_analysis_charts.py`: seven labelled charts and KPI/summary CSV outputs.
- `src/06_manual_validation.py`: independent grade/result arithmetic check for 20 students.
- `src/07_export_business_rules.py`: Power BI-friendly rule CSV exports from the canonical JSON file.
- `notebooks/Student_Performance_Analysis.ipynb`: executed EDA and KPI walkthrough.

## 11. Oracle SQL and PL/SQL
Committed:
- Oracle DDL, constraints, indexes and marks validation trigger.
- Python loader with environment-variable credentials, full-reload warning and query result CSV export.
- Ten business queries covering ranking, student percentages, subject averages, pass rate, failed students, low attendance, attendance/marks join, subject failure rate, department results and tied toppers.
- PL/SQL package with grade lookup, student percentage, read-only result classification, ranking, low attendance and student summary.
- PL/SQL smoke-test script.

**Execution status:** Oracle DDL, trigger, loader, queries and package have not been compiled or executed against a configured Oracle instance. No Oracle result or Python-to-Oracle reconciliation is claimed.

## 12. Streamlit dashboard
The five-section application provides:
1. Overview — KPI cards and cohort outcome summary.
2. Student Performance — marks distribution and student results.
3. Attendance Analysis — attendance distribution and low-attendance list.
4. Subject Analysis — subject averages and failure percentage.
5. Student Ranking — dense rank and individual student detail.

Filters include Department, Semester, Section, Subject and Academic Year. The app has a Streamlit AppTest smoke test and was included in successful CI validation.

Run locally after cleaning:
```bash
streamlit run app/streamlit_app.py
```

## 13. Power BI
The repository includes import instructions, six star-schema relationships, shared Business_Rules and Grade_Bands imports, DAX measures, three-page visual specification, slicers and student drill-through design.

**Execution status:** The PBIX has not been created in Power BI Desktop. The actual PBIX, refresh test and screenshots remain pending desktop authoring.

## 14. Excel
The generated workbook includes:
- Raw source tables and separate raw data tabs.
- Cleaned marks table.
- Student summary, rank and topper status.
- Attendance analysis and recalculated checks.
- Subject analysis.
- Dashboard formulas and chart.
- Validation sheet with Python values and Oracle reconciliation pending.
- Business rules, grade bands and data-quality checks.

A separate Data_Dictionary.xlsx contains 33 source/ETL field definitions with examples and validation rules.

**Execution status:** The workbook and data dictionary were generated in CI and inspected for expected sheets/tables. Native PivotTables and slicer objects still need to be added and saved in Excel Desktop.

## 15. Testing and verification
The latest successful CI run completed:
- Python source compilation.
- Synthetic data generation.
- Data cleaning and quality log creation.
- Shared business-rule CSV export.
- Seven chart generation and KPI summary.
- Jupyter notebook execution.
- Excel workbook and data dictionary generation.
- 20-record independent manual validation.
- Automated tests, including Streamlit dashboard smoke test.

Test report: 18 tests total — 17 PASS, 0 FAIL, 1 SKIP. The skipped test is Python-to-Oracle KPI reconciliation because Oracle credentials were not configured. The 20-record manual check reported grade and result agreement for all 20 records.

## 16. Limitations and risks
1. All current data is synthetic, not actual college data.
2. Attendance threshold, assessment maxima, passing mark and grade bands are provisional.
3. Raw marks and attendance lack term IDs; ETL attaches one term only. Multi-term data requires source term mapping.
4. Daily attendance trends cannot be inferred from term-level aggregates.
5. Oracle execution and reconciliation remain unverified.
6. PBIX and native Excel PivotTables/slicers require Power BI Desktop and Excel Desktop.
7. Correlation does not imply causation.

## 17. Recommendations
- Obtain written approval and anonymised institutional records before replacing the synthetic sample.
- Confirm grade bands, passing marks and attendance threshold with official academic regulations.
- Add a term identifier to each source marks and attendance record before supporting multiple terms.
- Add date-level attendance events only if a real source system provides them.
- Compile and test the Oracle scripts in a dedicated schema, then reconcile all KPIs.
- Complete Power BI Desktop and Excel Desktop deliverables before final institutional submission.

## 18. Conclusion
The Python-based data pipeline, notebook, charts, Streamlit dashboard smoke test, Excel workbook generation, data dictionary, manual validation and automated tests are verified by GitHub Actions. The project is a working synthetic academic analytics prototype with documented Oracle and Power BI implementation paths. It is not yet a production system or fully verified multi-platform deployment because Oracle execution, PBIX creation and native Excel PivotTables/slicers remain outstanding.
