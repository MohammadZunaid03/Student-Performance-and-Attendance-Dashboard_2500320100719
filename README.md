# Student Performance and Attendance Dashboard

An academic analytics project that integrates student marks and attendance to report class performance, pass percentage, toppers, subject outcomes and low-attendance cases.

**Author:** Mohammad Zunaid  
**Domain:** Education and Academic Analytics  
**Status:** Development in progress

> **Data notice:** The committed raw dataset is synthetic and contains fictional student labels plus intentional data-quality defects. It is for software demonstration only and must not be presented as actual institutional performance.

## Objectives
- Integrate student, subject, marks and attendance records.
- Clean and validate data with an auditable quality log.
- Calculate grades/results and student ranks using configurable rules.
- Identify low-attendance students and subject performance patterns.
- Deliver reproducible Python, Oracle SQL/PLSQL and Power BI analytics.

## Technology stack
Python, Pandas, NumPy, Matplotlib, Oracle SQL, Oracle PL/SQL, Power BI Desktop, Streamlit, Excel, Git/GitHub.

## Current implementation
- Synthetic data generator with fixed seed and five raw CSV datasets.
- Data dictionary and cleaning rules.
- Pandas cleaning pipeline with quarantine outputs.
- Oracle star-schema DDL, loader and ten business queries.
- PL/SQL analytics package.
- Python analysis/chart script.
- Jupyter notebook.
- Streamlit dashboard source.
- Power BI model/report instructions and DAX.
- Excel workbook generator and validation guide.
- Automated data validation tests.

Some deliverables require local software execution or desktop authoring. A committed script or guide does not mean its generated artifact has already been executed/created. In particular, the Oracle scripts need a configured Oracle instance, Power BI PBIX needs Power BI Desktop, and native Excel PivotTables/slicers need Excel Desktop.

## Repository structure
```text
app/
  streamlit_app.py
data/
  raw/                 # Synthetic input CSVs
  clean/               # Created by cleaning script
docs/                  # Definition, synopsis, SRS, design and guides
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
tests/
  test_pipeline.py
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
python src/04_analysis_charts.py
python src/05_build_excel_workbook.py
python tests/run_tests.py
```

The generator is deterministic. It writes synthetic CSV files under data/raw. The cleaning script writes accepted data to data/clean, rejected records to quarantine CSVs and a row-level issue summary to reports/data_quality_log.csv. The analysis script writes charts and reports/analysis_summary.md.

## Streamlit dashboard
After running the cleaning pipeline:

```bash
streamlit run app/streamlit_app.py
```

The dashboard provides cohort/subject filters, KPI cards, performance charts, topper list, low-attendance list and filtered CSV downloads.

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
```

The loader performs a controlled full reload by deleting facts before dimensions. Back up any database you care about before running it. Oracle execution has not been verified in this repository until run against a configured instance.

## Power BI and Excel
- Follow [Power BI data model guide](docs/PowerBI_Data_Model.md) and [report guide](docs/PowerBI_Report_Guide.md). Save the completed PBIX to powerbi/ after creating it in Power BI Desktop.
- Run `python src/05_build_excel_workbook.py` to generate the workbook. Follow [Excel workbook guide](docs/Excel_Workbook_Guide.md) to add native PivotTables and slicers in Excel Desktop.

## Business-rule assumptions
The synthetic sample uses 40 internal + 60 external marks and 40/100 passing marks. Grade bands are provisional demonstration values. The 75% attendance threshold is provisional. Confirm official college policy before using the dashboard for real student decisions. Missing marks and absent marks remain distinct and are not silently converted to zero.

## Validation and limitations
Tests are defined in tests/test_pipeline.py. Run tests/run_tests.py after cleaning. Oracle integration tests are skipped unless ORACLE_USER, ORACLE_PASSWORD and ORACLE_DSN are configured. Do not report skipped or unexecuted tests as passed.

The initial project has no authorised real institutional dataset, live ERP integration, hosted service or completed Power BI PBIX. Any conclusions from current sample data are synthetic demonstrations.

## AI usage disclosure
AI assistance may have been used to draft documentation and code. The project owner must review, execute, understand and validate all generated material before academic submission.

## Future enhancements
- Replace synthetic data with authorised anonymised institutional data.
- Confirm official grade and attendance policies.
- Add date-level attendance if source events become available.
- Add role-based access and secure deployment.
- Complete Power BI PBIX, Excel PivotTables/slicers and demo recording.

## Repository
https://github.com/MohammadZunaid03/Student-Performance-and-Attendance-Dashboard_2500320100719
