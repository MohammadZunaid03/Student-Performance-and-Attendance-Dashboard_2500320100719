# Student Performance and Attendance Dashboard
## Project definition

**Domain:** Education and academic analytics  
**Project owner:** Mohammad Zunaid  
**Technology focus:** Python, Oracle SQL, Oracle PL/SQL and Power BI

### Problem statement
Academic marks and attendance are often maintained in separate records, making it difficult for faculty and academic coordinators to obtain a consistent view of student progress. Manual consolidation can delay identification of students with low attendance, weak subject performance or risk of failing. This project combines marks and attendance into a structured analytical dataset and presents verified academic indicators through SQL analysis and interactive dashboards.

### Objectives
1. **Integrate academic records:** process at least 200 fictional students, five subjects and 1,000 student-subject marks/attendance pairs; all accepted fact rows must reference valid student, subject and term dimensions.
2. **Automate academic calculations:** calculate total marks, percentage, grade and pass/fail using the canonical configurable rules; independently hand-check at least 20 student records and require 100% agreement.
3. **Identify attendance and performance risks:** produce a student-level below-threshold list, subject averages and failure rates; every accepted attendance value must be within 0–100%.
4. **Communicate results:** generate at least seven labelled charts, a five-section interactive Streamlit dashboard, ten SQL business queries and a three-page Power BI report design; reconcile KPI values across tools when Oracle/Power BI execution is available.

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
| KPI | Numerator | Denominator | Definition and exclusions |
|---|---|---|---|
| Student count | Distinct valid Student_ID | Not applicable | Distinct students in the selected cohort |
| Average marks | Sum of valid PRESENT total marks | Count of PRESENT student-subject records | Mean scored mark; ABSENT/MISSING excluded and separately counted |
| Pass rate | Count of PASS outcomes | Count of PRESENT scored student-subject records | PASS / PRESENT × 100; ABSENT/MISSING excluded |
| Attendance % | Present_Classes | Total_Classes | Present / conducted × 100, calculated per student-subject |
| Low-attendance count | Distinct students below threshold | Not applicable | Mean subject attendance below canonical configured threshold |
| Topper/rank | Aggregate PRESENT marks | Not applicable | Dense rank by sum of scored subject marks; ties retain equal rank |
| Subject average | Sum of PRESENT marks for subject | PRESENT scored records for subject | Mean scored marks for the subject |
| Failure rate | FAIL outcomes for subject | PRESENT scored records for subject | FAIL / PRESENT × 100; ABSENT/MISSING excluded |
| Absent records | Count of Record_Status=ABSENT | Not applicable | Kept distinct; not converted to zero |
| Missing records | Count of Record_Status=MISSING | Not applicable | Kept distinct; not converted to zero |

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
