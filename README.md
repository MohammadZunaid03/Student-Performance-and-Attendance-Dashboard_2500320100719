# Student Performance and Attendance Dashboard

An academic analytics project that integrates student marks and attendance to report class performance, pass percentage, toppers, subject outcomes and low-attendance cases.

**Author:** Mohammad Zunaid  
**Domain:** Education and Academic Analytics  
**Status:** Python pipeline implemented and CI-validated; Oracle/Power BI Desktop integration pending

> **Data notice:** The committed raw dataset is synthetic and contains fictional student labels plus intentional data-quality defects. It is for software demonstration only and must not be presented as actual institutional performance.

## Objectives
- Integrate student, subject, marks and attendance records.
- Clean and validate data with an auditable quality log.
- Calculate grades/results and student ranks using configurable rules.
- Identify low-attendance students and subject performance patterns.
- Deliver reproducible Python, Oracle SQL/PLSQL and Power BI analytics.

## Technology stack
Python, Pandas, NumPy, Matplotlib, Seaborn, Oracle SQL, Oracle PL/SQL, Power BI Desktop, Streamlit, Excel, Git/GitHub.

## Current implementation
- Synthetic data generator with fixed seed and five raw CSV datasets.
- Public dataset research, data dictionary and cleaning rules.
- Single business-rule source in config/business_rules.json, exported for BI.
- Pandas cleaning pipeline with quarantine outputs.
- Oracle star-schema DDL, loader and ten business queries.
- PL/SQL analytics package.
- Python analysis/chart script.
- Jupyter notebook.
- Streamlit dashboard source.
- Power BI model/report instructions and DAX.
- Excel workbook generator and validation guide.
- Automated data validation and Streamlit smoke tests, manual 20-record checks and GitHub Actions CI.

Some deliverables require local software execution or desktop authoring. A committed script or guide does not mean its generated artifact has already been executed/created. In particular, the Oracle scripts need a configured Oracle instance, Power BI PBIX needs Power BI Desktop, and native Excel PivotTables/slicers need Excel Desktop.

## Repository structure
```text
app/
  streamlit_app.py
data/
  raw/                 # Synthetic input CSVs
  clean/               # Created by cleaning script
docs/                  # Definition, synopsis, SRS, data research, reports and guides
config/                # Canonical business rules and Power BI CSV exports
excel/                 # Generated workbook output
notebooks/
  Student_Performance_Analysis.ipynb
powerbi/               # Save PBIX and screenshots here
reports/
  charts/              # Created by analysis script
  sql_results/         # Created by Oracle loader
sql/
  schema.sql
  queries.sql
  plsql/
src/
  01_generate_data.py
  02_clean_data.py
  03_load_sql.py
  04_analysis_charts.py
  05_build_excel_workbook.py
  06_manual_validation.py
  07_export_business_rules.py
tests/
  test_pipeline.py
  test_dashboard.py
  run_tests.py
requirements.txt
README.md
```

## Setup
Use Python 3.10+.

```bash
python -m venv .venv
```

Windows:
```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the Python pipeline
Run from the repository root:

```bash
python src/01_generate_data.py
python src/02_clean_data.py
python src/07_export_business_rules.py
python src/04_analysis_charts.py
python src/05_build_excel_workbook.py
python src/06_manual_validation.py
python tests/run_tests.py
```

The generator is deterministic. It writes synthetic CSV files under data/raw. The cleaning script writes accepted data to data/clean, rejected records to quarantine CSVs and a row-level issue summary to reports/data_quality_log.csv. The analysis script writes charts, reports/analysis_summary.md, low-attendance, topper and pass-rate CSVs. The manual validation script independently checks 20 student records.

## Streamlit dashboard
After running the cleaning pipeline:

```bash
streamlit run app/streamlit_app.py
```

The dashboard has five sections (Overview, Student Performance, Attendance Analysis, Subject Analysis and Student Ranking), filters for Department, Semester, Section, Subject and Academic Year, KPI cards, charts, student drill-down and filtered CSV downloads.

## Oracle SQL and PL/SQL
1. Create an Oracle schema/user using your own database administration process.
2. Run `sql/schema.sql`.
3. Configure environment variables; do not commit credentials.

PowerShell example:
```powershell
$env:ORACLE_USER="your_user"
$env:ORACLE_PASSWORD="your_password"
$env:ORACLE_DSN="localhost:1521/your_service"
python src/03_load_sql.py
```

Run the PL/SQL package after loading:
```sql
@sql/plsql/academic_analytics_pkg.sql
@sql/plsql/test_academic_analytics_pkg.sql
```

The loader performs a controlled full reload by deleting facts before dimensions. Back up any database you care about before running it. Oracle execution has not been verified in this repository until run against a configured instance.

## Power BI and Excel
- Follow [Power BI data model guide](docs/PowerBI_Data_Model.md) and [report guide](docs/PowerBI_Report_Guide.md). Save the completed PBIX to powerbi/ after creating it in Power BI Desktop.
- Run `python src/05_build_excel_workbook.py` to generate the workbook. Follow [Excel workbook guide](docs/Excel_Workbook_Guide.md) to add native PivotTables and slicers in Excel Desktop.

## Business-rule assumptions
The canonical configuration is config/business_rules.json. The current synthetic sample uses 40 internal + 60 external marks, a 40/100 default passing mark, provisional grade bands and a provisional 75% attendance threshold. Subject-level Passing_Marks is authoritative. Change only the JSON source and regenerate/reload dependent outputs. Confirm official college policy before using the dashboard for real student decisions. Confirm official college policy before using the dashboard for real student decisions. Missing marks and absent marks remain distinct and are not silently converted to zero.

## Validation and limitations
Tests are defined in tests/test_pipeline.py and tests/test_dashboard.py. Run tests/run_tests.py after cleaning. GitHub Actions runs Python compilation, generation, cleaning, notebook execution, charts, Excel generation, 20-record manual validation and automated tests. Oracle integration tests are skipped unless ORACLE_USER, ORACLE_PASSWORD and ORACLE_DSN are configured. Do not report skipped or unexecuted tests as passed.

The current committed data is synthetic, not an authorised institutional dataset. Oracle SQL/PLSQL has not been compiled against a live Oracle instance; Python-to-Oracle reconciliation remains unverified. The actual Power BI PBIX and native Excel PivotTables/slicers still require desktop authoring. No live ERP integration or hosted service is claimed. Any conclusions from current sample data are synthetic demonstrations.

## AI usage disclosure
AI assistance may have been used to draft documentation and code. The project owner must review, execute, understand and validate all generated material before academic submission.

## Future enhancements
- Replace synthetic data with authorised anonymised institutional data.
- Confirm official grade and attendance policies.
- Complete Oracle compilation and Python/Oracle KPI reconciliation.
- Add date-level attendance if source events become available.
- Add role-based access and secure deployment.
- Complete Power BI PBIX, Excel PivotTables/slicers and demo recording.

## Repository
https://github.com/MohammadZunaid03/Student-Performance-and-Attendance-Dashboard_2500320100719
