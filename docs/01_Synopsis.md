# Project Synopsis
## Student Performance and Attendance Dashboard

### Problem
Student marks and attendance are commonly stored in separate records. Consolidating them manually makes it harder to monitor academic outcomes, detect low attendance and identify students who may need support. This project integrates those records and presents consistent, auditable academic insights.

### Objectives
- Integrate student, subject, marks and attendance data with validated keys.
- Automate grade, result, rank and attendance calculations using approved rules.
- Identify low-attendance students and subject-level performance patterns.
- Present class results, pass rate and topper information in Power BI.

### Scope
**In scope:** data generation/import; data quality checks; Python/Pandas cleaning and analysis; Oracle relational/star-schema design; SQL business queries; PL/SQL grade procedure/function; Power BI model/report specification and build; Excel spot-checks; automated validation; documentation.

**Out of scope unless separately approved:** live integration with college ERP/LMS, student login portal, predictive machine learning, production hosting, real-time attendance capture and decisions about student progression.

### Data source
The initial development dataset will be reproducible synthetic data because no authorised institutional dataset has been provided. It will contain fictional student, subject, marks, attendance and term records. Raw files will deliberately include documented quality defects for cleaning demonstrations. Any public or institutional dataset must be accompanied by its source, licence/permission and privacy review.

### Tools
| Tool | Purpose |
|---|---|
| Python, Pandas, NumPy | Generate, validate, clean and analyse records |
| Oracle SQL | Store structured data and answer business questions |
| Oracle PL/SQL | Encapsulate grade/result and summary logic |
| Power BI | Interactive academic and attendance reporting |
| Excel | Independent sample verification and pivot analysis |
| Git/GitHub | Version control and reproducible project delivery |

### Methodology
1. Define data model and business rules.
2. Generate or import raw records.
3. Profile and clean data with a quality log.
4. Load validated records into Oracle dimensions and fact tables.
5. Execute SQL/PLSQL calculations and business queries.
6. Analyse results in Python and build visualisations.
7. Build Power BI model/report and Excel cross-checks.
8. Run automated and manual validation; document limitations.

### Deliverables
Project definition, synopsis, SRS, reproducible raw/clean CSVs, data dictionary, Python scripts/notebook, Oracle DDL/DML/queries/PLSQL, ER and star-schema diagrams, Power BI model/report, Excel verification workbook, tests, quality log, README, final report and demo video.

### Six-week plan
| Week | Work | Deliverable |
|---|---|---|
| 1 | Confirm rules, requirements, data model and dataset design | Definition, synopsis, SRS, schema plan |
| 2 | Generate/profile data and build cleaning pipeline | Raw/clean CSVs, dictionary, quality log |
| 3 | Oracle schema, loading, SQL and PL/SQL | SQL scripts and validated query outputs |
| 4 | Python analysis, charts and notebook | Analysis scripts, charts and notebook |
| 5 | Power BI model/report and Excel verification | PBIX/report guide and workbook |
| 6 | Automated tests, reconciliation, documentation and demo | Test report, README and final report |

### Expected outcomes
A reproducible academic analytics workflow that consolidates marks and attendance, identifies low-attendance cases, reports pass rate and rankings, and makes subject/class performance easier to review. Quantitative findings will be reported only after the dataset is generated and calculations are executed. Synthetic-data findings will be labelled as demonstrations, not institutional facts.
