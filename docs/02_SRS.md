# Software Requirements Specification
## Student Performance and Attendance Dashboard

**Version:** 1.0  
**Status:** Initial requirements baseline

## 1. Introduction
This SRS defines the requirements for a student academic analytics project that combines marks and attendance records and presents validated results through Python, Oracle SQL/PLSQL and Power BI.

## 2. Purpose and scope
The purpose is to provide a reproducible way to analyse student performance, attendance, pass rate, subject outcomes and ranking. The system is an academic analytics prototype, not a replacement for an institutional ERP or official examination system.

## 3. Overall description
### Users
- Administrator/data operator: supplies and refreshes data.
- Faculty: reviews subject and student performance.
- Academic coordinator: reviews class/semester summaries and low-attendance cases.

### Assumptions
- Student_ID and Subject_ID are stable identifiers.
- Initial data is synthetic unless authorised real data is supplied.
- Attendance threshold, grade boundaries, passing marks and absent policy are configurable and require institutional confirmation.
- Missing marks and absent marks are distinct states.

### Constraints
- Oracle availability and version may affect database execution.
- Power BI Desktop is required to create and save the PBIX.
- No real student personal data should be committed to a public repository.
- Results must be traceable to source rows and documented business rules.

## 4. Functional requirements
| ID | Requirement | Priority | Verification |
|---|---|---|---|
| FR1 | Import student and subject master records with unique identifiers | High | Duplicate-key test |
| FR2 | Import marks records linked to valid students and subjects | High | Foreign-key validation |
| FR3 | Import attendance records linked to valid students and subjects | High | Foreign-key and range tests |
| FR4 | Detect duplicates, missing values, invalid values and inconsistent text | High | Data-quality report |
| FR5 | Produce cleaned datasets without silently discarding records | High | Rejected-row and row-count reconciliation |
| FR6 | Calculate total marks and percentage using configured assessment rules | High | Hand-check sample |
| FR7 | Classify pass/fail using configured passing rules | High | Boundary test cases |
| FR8 | Assign grades using configurable grade boundaries | High | Grade boundary tests |
| FR9 | Calculate student ranks and preserve ties | High | Equal-score test |
| FR10 | Identify students below the configured attendance threshold | High | Threshold boundary test |
| FR11 | Produce subject-wise and cohort-wise summaries | High | SQL aggregate reconciliation |
| FR12 | Present KPI and detail views in Power BI | High | Visual/filter review |
| FR13 | Export analysis and validation outputs | Medium | File existence/content checks |

## 5. Non-functional requirements
| ID | Requirement | Measurement / acceptance target |
|---|---|---|
| NFR1 | Reproducibility | Same fixed seed and configuration produce byte-identical raw CSV files on repeated runs |
| NFR2 | Data integrity | 100% of accepted fact rows reference valid student, subject and term keys |
| NFR3 | Auditability | Every defined cleaning rule records issue, rule, affected rows, before and after treatment |
| NFR4 | Correctness | At least 20/20 selected records reconcile with independent hand calculations |
| NFR5 | Maintainability | Attendance threshold, component maxima and grade bands are stored in one JSON configuration source |
| NFR6 | Privacy | Public repository contains no real student PII or credentials |
| NFR7 | Usability | Every KPI has a documented definition, denominator, unit and filter context |
| NFR8 | Reliability | Missing required inputs cause a clear error and non-zero process exit |
| NFR9 | Performance | The 200-student/1,000-fact synthetic pipeline completes within 60 seconds in the CI runner |
| NFR10 | Testability | Automated Python suite reports PASS/FAIL/SKIP and retains a machine-readable test report |

## 6. Data requirements
Core entities: Students, Subjects, Academic_Terms, Marks and Attendance. IDs must be stable and unique in their master tables. Marks must be within configured valid ranges. Attendance counts must be non-negative, present classes cannot exceed conducted classes, and calculated attendance must be 0–100%. Absence and missingness must be represented separately.

## 7. Security and privacy
Use fictional data for public development. Do not commit credentials, connection strings, real student names, phone numbers, addresses or institutional identifiers. Oracle credentials must be supplied through environment variables or a local ignored configuration file.

## 8. Acceptance criteria
1. At least 20 selected student records reconcile with independently calculated totals/grades after grading rules are approved.
2. Low-attendance output exactly follows the configured threshold and boundary rule.
3. Pass-rate numerator and denominator are stated and reproducible.
4. Tied scores receive equal rank according to the selected ranking method.
5. Data-quality log accounts for each documented correction, quarantine or exclusion.
6. Python and Oracle outputs reconcile on equivalent inputs and definitions.
7. Power BI KPI values reconcile with validated source outputs for the same filters.
8. Missing marks are not silently converted to zero.
