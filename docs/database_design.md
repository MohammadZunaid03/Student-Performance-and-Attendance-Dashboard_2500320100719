# Oracle database and star-schema design

## Fact-table grain
- **FACT_MARKS:** one student × subject × academic term marks outcome. ABSENT and MISSING rows remain present with null scores and explicit statuses.
- **FACT_ATTENDANCE:** one student × subject × academic term attendance aggregate.
- Both facts have independent measures. Never join facts only on Student_ID; use student + subject + term keys or aggregate each fact to a common grain first.

## Dimensions
- **DIM_STUDENT:** descriptive student attributes, department, semester and section.
- **DIM_SUBJECT:** subject name/code and subject maximum/passing marks.
- **DIM_ACADEMIC_TERM:** academic-year and term boundaries; this is the time filter for the current sample.
- **DIM_DATE:** calendar reference rows populated across term start/end dates. Current source facts are term-level aggregates and contain no event date, so DIM_DATE is not joined to either fact. Do not pretend these aggregates are daily events.
- **DIM_BUSINESS_RULE:** canonical numeric business-rule values loaded from config/business_rules.json, including attendance and component maxima.
- **DIM_GRADE_BAND:** grade-to-minimum-score mapping loaded from the same canonical JSON configuration.

## Keys and constraints
Surrogate numeric keys are used for warehouse relationships; source identifiers remain unique alternate keys. Foreign keys enforce valid student, subject and term dimensions. CHECK constraints enforce valid status, score arithmetic and attendance ranges. A trigger validates internal/external component maxima and subject-specific maximum marks against the loaded configuration. Unique student-subject-term constraints enforce fact grain.

## Business-rule configuration
`config/business_rules.json` is the single source of truth for provisional attendance threshold, internal/external/total marks maxima, default passing marks, grade bands and absent/missing labels. The Python loader reads it directly and the Oracle loader populates DIM_BUSINESS_RULE and DIM_GRADE_BAND. Power BI/Excel use CSV/workbook exports generated from the same JSON. Subject-level Passing_Marks remains authoritative for each subject.

## Loading order
1. Run the Python generator and cleaner; the cleaner attaches the only valid Term_ID to the cleaned facts. It stops if multiple terms exist without source term mapping.
2. Create DIM_STUDENT, DIM_SUBJECT and DIM_ACADEMIC_TERM.
3. Populate DIM_DATE for the calendar range of each term (reference calendar only).
4. Populate DIM_BUSINESS_RULE and DIM_GRADE_BAND from the shared JSON configuration.
5. Resolve surrogate keys and load FACT_MARKS and FACT_ATTENDANCE.
6. Reconcile row counts and quarantined records.

## Oracle compatibility and safety
DDL uses identity columns available in Oracle 12c+. If the target database is older, replace identity columns with sequences and before-insert triggers. The Python loader performs a full reload by deleting existing project rows before inserting the cleaned sample; back up the target schema and use a dedicated project schema before running it. Credentials are supplied through environment variables and are never stored in this repository.

## Execution status
DDL, loader and PL/SQL source are committed. Oracle compilation, trigger execution and query results remain NOT VERIFIED until run against an actual Oracle instance.
