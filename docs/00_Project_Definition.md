# Student Performance and Attendance Dashboard
## Project definition

**Domain:** Education and academic analytics  
**Project owner:** Mohammad Zunaid  
**Technology focus:** Python, Oracle SQL, Oracle PL/SQL and Power BI

### Problem statement
Academic marks and attendance are often maintained in separate records, making it difficult for faculty and academic coordinators to obtain a consistent view of student progress. Manual consolidation can delay identification of students with low attendance, weak subject performance or risk of failing. This project combines marks and attendance into a structured analytical dataset and presents verified academic indicators through SQL analysis and interactive dashboards.

### Objectives
1. **Integrate academic records:** combine student, subject, marks and attendance records using stable student and subject identifiers; validate referential integrity before analysis.
2. **Automate academic calculations:** calculate total/percentage, grade and pass/fail status using documented, configurable rules; verify a sample of at least 20 students manually.
3. **Identify attendance and performance risks:** produce a student-level list below the configured attendance threshold and subject-level performance summaries.
4. **Communicate results:** deliver a Power BI report with pass-rate, topper/rank and low-attendance views, backed by reproducible Python and Oracle SQL processing.

### Business questions
1. Which students have the highest overall academic performance, including ties?
2. Which students fall below the institution's attendance threshold?
3. What is the overall pass rate, using a clearly defined student/subject denominator?
4. Which subjects have the lowest average marks or highest failure rates?
5. How do attendance and marks vary together, and which students may need academic support?

### Users and stakeholders
- **Faculty:** review subject results, attendance and students requiring attention.
- **Academic coordinator:** compare class/semester performance and monitor pass rate.
- **Administrator/data operator:** maintain source records and refresh the analytical dataset.
- **Students (indirect beneficiaries):** receive timely academic feedback through institutional processes.

### Proposed KPIs and definitions
| KPI | Definition |
|---|---|
| Student count | Distinct valid Student_ID values in the selected cohort |
| Average marks | Mean of valid scored records; absent/missing records are excluded and reported separately |
| Pass rate | Passed eligible student-subject records divided by all eligible student-subject records × 100 |
| Attendance % | Present classes divided by conducted classes × 100 |
| Low-attendance count | Distinct students whose calculated attendance is below the configured threshold |
| Topper/rank | Rank based on the documented aggregate marks/percentage rule; ties retain equal rank |
| Subject average | Mean valid total marks for the subject |
| Failure rate | Failed eligible student-subject records divided by eligible student-subject records × 100 |

### Rules and assumptions requiring institutional confirmation
- The institution's official attendance threshold has not been supplied. It will be a configurable setting; **75% may be used only as a provisional demonstration default**, not represented as an institutional policy.
- Official grade boundaries, passing marks, treatment of absent candidates and weighting of internal/external marks must be confirmed. Until then, these remain configurable and documented assumptions.
- The spreadsheet brief requires absent-mark handling, low-attendance detection and tied-rank tests. Missing marks must not automatically be treated as zero.
- The initial dataset will be synthetic unless an approved, privacy-safe institutional dataset is provided. Synthetic results must never be presented as real college outcomes.

### Acceptance criteria
- Grade/result logic matches hand calculations for at least 20 selected student records once official rules are configured.
- A reproducible low-attendance list is generated using the configured threshold.
- Pass-rate denominator and numerator are documented and independently reconcilable.
- Topper/rank view handles ties correctly.
- Data-quality issues, exclusions and missing/absent records are visible in a report.
- Python outputs, Oracle query outputs and Power BI measures reconcile for the same filter context.

### Required industry-grade deliverables
Problem statement and KPI definitions; ER/star-schema diagram; Python cleaning/analysis notebook; Oracle DDL, DML and business queries; Power BI PBIX with slicers and drill-through; data-quality report; insights summary; README; GitHub repository; demo video (to be recorded after implementation).
