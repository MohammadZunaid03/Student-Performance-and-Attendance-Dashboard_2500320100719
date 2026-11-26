# Final Evaluation Checklist
## Student Performance and Attendance Dashboard

**Evaluation status:** Not yet final — several components require local execution or desktop application evidence.

| Area | Evidence to inspect | Current status |
|---|---|---|
| Project definition, synopsis, SRS | docs/00_Project_Definition.md, docs/01_Synopsis.md, docs/02_SRS.md | Documentation committed |
| Dataset generator and raw data | src/01_generate_data.py, data/raw/ | Committed; execution reproducibility to verify |
| Data dictionary | docs/Data_Dictionary.md | Markdown dictionary committed; XLSX pending |
| Cleaning pipeline | src/02_clean_data.py, docs/Cleaning_Rules.md | Code committed; runtime test pending |
| Oracle schema | sql/schema.sql | DDL committed; Oracle compilation pending |
| ER/star schema | docs/star_schema.mmd | Diagram source committed; rendered image pending |
| SQL loader and queries | src/03_load_sql.py, sql/queries.sql | Code committed; Oracle execution pending |
| PL/SQL | sql/plsql/academic_analytics_pkg.sql | Package committed; Oracle compilation pending |
| Python charts | src/04_analysis_charts.py | Code committed; chart execution pending |
| Jupyter notebook | notebooks/Student_Performance_Analysis.ipynb | Notebook committed; execution pending |
| Streamlit | app/streamlit_app.py | Code committed; runtime review pending |
| Power BI model/report | docs/PowerBI_Data_Model.md, docs/PowerBI_Report_Guide.md | Instructions committed; PBIX pending |
| Excel | src/05_build_excel_workbook.py, docs/Excel_Workbook_Guide.md | Generator committed; workbook/PivotTables/slicers pending |
| Automated tests | tests/test_pipeline.py, tests/run_tests.py | Tests committed; execution pending |
| README | README.md | Updated |
| Final report | docs/03_Final_Project_Report.md | Draft committed; results pending |
| Viva | docs/04_Viva_Preparation.md | Question bank committed |
| Demo video | External recording | Not created |

## Final score
Do not assign a final score until artifacts are executed and inspected. Suggested rubric:
- Requirements and documentation: 10
- Dataset and data quality: 15
- Python pipeline and analysis: 15
- Oracle schema, SQL and PL/SQL: 20
- Power BI report: 15
- Excel verification: 5
- Automated testing and reconciliation: 10
- README, report and demo: 10

Total: 100.

## Required final evidence
- Successful generator and cleaning run with row counts.
- Data-quality log and quarantine review.
- Oracle DDL/package compilation and query outputs.
- Python charts and executed notebook.
- Streamlit run evidence.
- Completed PBIX and screenshots.
- Excel workbook opened, recalculated and reviewed; native PivotTables/slicers checked.
- Test report with PASS/FAIL/SKIP and Oracle reconciliation where configured.
- Report numbers match actual outputs.
