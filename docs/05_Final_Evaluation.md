# Final Evaluation — Student Performance and Attendance Dashboard

**Evaluation basis:** repository contents and successful GitHub Actions run 45820144140.  
**Score:** 75 / 100 implementation coverage. This is an evidence-based project-completeness score, not a college-awarded academic grade.

| Area | Available marks | Awarded | Evidence / deduction |
|---|---:|---:|---|
| Requirements and documentation | 10 | 10 | Project definition, synopsis, SRS, data dictionary, guides and implementation notes |
| Dataset and data quality | 15 | 15 | Deterministic synthetic generator, intentional defects, boundary cases, quarantine and before/after log |
| Python pipeline and analysis | 15 | 15 | CI generation/cleaning, seven charts, KPI reports, executed notebook and manual 20-record check |
| Oracle schema, SQL and PL/SQL | 20 | 10 | DDL, constraints, trigger, loader, ten queries, package and test script committed; Oracle compilation/execution and reconciliation not verified |
| Power BI report | 15 | 7 | Data model, DAX, three-page visual plan, slicers and drill-through documented; PBIX/screenshots not created in Power BI Desktop |
| Excel verification | 5 | 4 | Workbook, formulas, charts, data dictionary and validation generated; native PivotTables/slicers still require Excel Desktop |
| Automated tests and reconciliation | 10 | 8 | 17 tests passed, 0 failed; one Oracle integration test skipped because credentials were not configured |
| README, final report and demo | 10 | 6 | README, final report and viva bank complete; demonstration video not recorded |
| **Total** | **100** | **75** | |

## Verification evidence
- Python source compilation: PASS.
- Synthetic data generation: PASS.
- Data cleaning and quarantine: PASS.
- Shared business-rule export: PASS.
- Seven charts and KPI summary: PASS.
- Jupyter notebook execution: PASS.
- Excel workbook and data dictionary generation: PASS.
- Independent manual validation: 20/20 PASS.
- Automated tests: 17 PASS, 0 FAIL, 1 SKIP.
- Streamlit dashboard smoke test: PASS.
- Oracle compilation/reconciliation: NOT VERIFIED.
- Power BI PBIX: NOT CREATED.
- Native Excel PivotTables/slicers: NOT VERIFIED.

## Final judgement
The Python-centered prototype is reproducible and CI-validated. It is not accurate to describe the entire multi-platform solution as fully deployed or production-ready until Oracle, Power BI Desktop and Excel Desktop steps are completed and evidenced.

## Required to reach full completion
1. Oracle schema/trigger/package compilation, loader run, SQL outputs and KPI reconciliation.
2. Power BI PBIX creation, refresh, slicer/drill-through checks and screenshots.
3. Excel native PivotTables/slicers, refresh and reconciliation.
4. Final demonstration recording and review.
