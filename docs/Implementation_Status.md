# Implementation status

This file distinguishes committed source/documentation from artifacts that have actually been generated or executed. A Git commit alone is not evidence of runtime validation.

| Phase | Deliverable | Repository status | Verification status |
|---|---|---|---|
| P1 | Project definition | Committed | Requirements baseline drafted |
| P2 | Synopsis | Committed | Six-week plan documented |
| P3 | SRS | Committed | Acceptance criteria documented |
| P4 | Generator and raw CSVs | Committed | Generator/runtime reproducibility not yet executed in this environment |
| P5 | Data dictionary | Markdown committed; XLSX generator included | XLSX awaits local execution |
| P6 | Cleaning pipeline | Script and rules committed | Clean outputs and quality log await execution |
| P7 | Oracle star schema | DDL and Mermaid ER source committed | Oracle DDL not compiled; PNG rendering pending |
| P8 | Loader and 10 SQL queries | Committed | Requires configured Oracle instance |
| P9 | PL/SQL package | Committed | Requires Oracle compilation and tests |
| P10 | Seven-chart analysis | Script committed | Charts and KPI summary await execution |
| P11 | Jupyter notebook | Committed | Notebook cells not yet executed |
| P12 | Streamlit dashboard | Source committed | App runtime not yet tested |
| P13 | Power BI data model | Guide and DAX committed | Model must be created in Power BI Desktop |
| P14 | Power BI report | Three-page guide committed | PBIX and screenshots not yet created |
| P15 | Excel verification | Workbook generator and guide committed | Workbook awaits execution; native PivotTables/slicers require Excel Desktop |
| P16 | Automated tests | Tests, runner and CI workflow committed | Tests not yet run; Oracle integration requires credentials |
| P17 | README | Updated | Documentation committed |
| P18 | Final report | Evidence-based draft committed | Actual findings await pipeline execution |
| P19 | Viva | 40-question bank committed | Interactive viva can be conducted in chat |
| P20 | Final evaluation | Checklist committed | Final score withheld until artifacts are verified |

## Environment limitations
The repository integration can commit source files but cannot execute Python inside the user's local environment, compile against their Oracle database, create a native Power BI PBIX in Power BI Desktop, or add native Excel PivotTable slicers. A GitHub Actions workflow was added for Python validation, but no workflow run was returned by GitHub at the time this status was recorded.

## Required next execution
From the repository root, install requirements and run:
1. python src/01_generate_data.py
2. python src/02_clean_data.py
3. python src/04_analysis_charts.py
4. python src/05_build_excel_workbook.py
5. python tests/run_tests.py

Then configure Oracle, run schema/loader/PLSQL, and finish Power BI/Excel desktop steps. Update this status only with actual run evidence.
