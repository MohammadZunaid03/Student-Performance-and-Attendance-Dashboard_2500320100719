# Oracle database and star-schema design

## Fact-table grain
- **FACT_MARKS:** one student × subject × academic term marks outcome. ABSENT and MISSING rows are retained with null scores and explicit statuses.
- **FACT_ATTENDANCE:** one student × subject × academic term attendance aggregate.
- The two facts have separate measures and must not be joined to one another for aggregation. Join each fact independently to conformed dimensions, or aggregate each fact to the required common grain before combining.

## Dimensions
- DIM_STUDENT: descriptive student attributes and department/semester/section.
- DIM_SUBJECT: subject name/code and maximum/passing marks.
- DIM_ACADEMIC_TERM: academic-year and term boundaries.
- DIM_DATE: calendar attributes for date-based reporting. Current synthetic fact files are term aggregates and do not contain daily event dates; do not manufacture daily attendance dates.

## Keys and constraints
Surrogate numeric keys are used for warehouse relationships; source identifiers remain unique alternate keys. Foreign keys enforce valid dimensions. CHECK constraints enforce valid marks/status and attendance ranges. Unique student-subject-term constraints enforce the declared fact grain.

## Loading order
1. Load DIM_STUDENT, DIM_SUBJECT and DIM_ACADEMIC_TERM.
2. Populate DIM_DATE for a chosen reporting date range if date-level reporting is needed.
3. Resolve surrogate keys and load FACT_MARKS and FACT_ATTENDANCE.
4. Reconcile inserted row counts and quarantined source records.

## Oracle compatibility
DDL uses identity columns available in Oracle 12c+. If the target database is older, replace identity columns with sequences and before-insert triggers. Create users/permissions separately; credentials are never stored in this repository.
