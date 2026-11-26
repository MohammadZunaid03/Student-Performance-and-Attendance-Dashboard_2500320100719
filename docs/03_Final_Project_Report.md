# Final Academic Project Report
## Student Performance and Attendance Dashboard

**Author:** Mohammad Zunaid  
**Status:** Draft — update only after executing the complete pipeline and validating all outputs.

## Abstract
This project is designed to integrate student marks and attendance records using Python and Oracle SQL/PLSQL and present academic indicators through Power BI. The initial development dataset is synthetic and intended for demonstrating data-quality handling and analytical workflows.

## 1. Introduction
[Describe the academic reporting context and why consolidated marks/attendance analysis is useful.]

## 2. Problem Statement
Student marks and attendance are maintained separately, making it difficult to produce a consistent academic overview and identify low-attendance or weak-performance cases promptly.

## 3. Objectives
Refer to docs/00_Project_Definition.md. Report measurable completion evidence for each objective.

## 4. Existing and Proposed System
[Compare the current manual/source process with the implemented workflow. Do not claim institutional process facts without evidence.]

## 5. Scope
In-scope and out-of-scope boundaries are documented in docs/01_Synopsis.md.

## 6. Tools and Technologies
Python, Pandas, NumPy, Oracle SQL, Oracle PL/SQL, Power BI, Excel, Streamlit and GitHub.

## 7. Dataset Description
The initial data is synthetic: 200 fictional students, five subjects, marks and attendance at student-subject grain, plus one academic-term record. Refer to docs/Dataset_Design.md and docs/Data_Dictionary.md. Update row counts from the executed generator and cleaned outputs.

## 8. Data Cleaning and Preprocessing
Document duplicate handling, missing-value treatment, invalid marks, impossible attendance counts, quarantined rows and the actual reports/data_quality_log.csv values. Do not insert estimated counts.

## 9. System Architecture
[Insert verified architecture diagram after creation.]

## 10. Database Design
Refer to sql/schema.sql, docs/database_design.md and docs/star_schema.mmd. Explain the grain of each fact table and the conformed dimensions.

## 11. Python Implementation
Describe generator, cleaning pipeline, analysis script and notebook. Include only functions actually implemented and verified.

## 12. Oracle SQL Implementation
[Insert Oracle version, schema execution evidence, loader row counts and query output summaries after testing.]

## 13. PL/SQL Implementation
Refer to sql/plsql/academic_analytics_pkg.sql. Add compilation and routine test evidence from Oracle.

## 14. Power BI Dashboard
[Insert PBIX screenshots and describe page visuals after building the report in Power BI Desktop.]

## 15. Excel Verification
[Insert workbook screenshots and reconciliation results after generating and reviewing the workbook in Excel.]

## 16. Testing and Validation
[Insert actual PASS/FAIL/SKIP counts from reports/test_results.csv. Identify tests not run.]

## 17. Results and Findings
| Metric | Actual value | Source / calculation | Status |
|---|---:|---|---|
| Total students | Pending execution | Cleaned student master | Not verified |
| Average marks | Pending execution | PRESENT marks only | Not verified |
| Average attendance | Pending execution | Cleaned attendance | Not verified |
| Pass percentage | Pending execution | PASS / PRESENT scored rows | Not verified |
| Low-attendance students | Pending execution | Configured threshold | Not verified |

Do not replace “Pending execution” with guessed values. Clearly label synthetic-data findings.

## 18. Recommendations
Use the generated low-attendance and subject analysis to identify records for faculty review. The dashboard is decision support, not an automatic disciplinary or progression decision system.

## 19. Limitations
- Synthetic data is not evidence about a real institution.
- Attendance threshold, grade bands and passing policy are provisional until confirmed.
- Current facts are term-level aggregates; daily attendance trends require date-level source data.
- Oracle execution and Power BI PBIX creation require external desktop/database environments.

## 20. Future Scope
Use authorised data, confirm institutional policy, add daily attendance, secure access, complete Power BI report and conduct user evaluation.

## 21. Conclusion
The repository provides a reproducible foundation for an academic analytics pipeline. Final conclusions must be completed after execution, reconciliation and validation.

## 22. References
- Project source files and documentation in this repository.
- Oracle Database SQL Language Reference (consult the version installed).
- Microsoft Power BI documentation (for Desktop modelling and DAX).
- pandas and Python official documentation.
