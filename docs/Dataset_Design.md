# Dataset design and provenance

## Provenance
The initial dataset is synthetic and generated locally with fixed seed 20261126. Names are fictional labels. No real student personal data is included. Synthetic findings must not be described as college or institutional outcomes.

## Tables and expected raw row counts
| File | Grain | Expected rows | Key |
|---|---|---:|---|
| students.csv | One student master record | 201 (200 plus one intentional duplicate) | Student_ID |
| subjects.csv | One subject | 5 | Subject_ID |
| marks.csv | One student-subject marks record | 1,001 (1,000 plus one duplicate) | Marks_ID |
| attendance.csv | One student-subject attendance record | 1,001 (1,000 plus one duplicate) | Attendance_ID |
| academic_terms.csv | One academic term | 1 | Term_ID |

The counts include deliberate defects. Cleaning must report accepted, corrected, quarantined and duplicate records separately.

## students.csv
| Column | Type | Meaning |
|---|---|---|
| Student_ID | string | Stable student key |
| Student_Name | string | Fictional display name |
| Department | string | Department code |
| Semester | integer | Semester number |
| Section | string | Class section |

## subjects.csv
| Column | Type | Meaning |
|---|---|---|
| Subject_ID | string | Subject key |
| Subject_Name | string | Subject title |
| Subject_Code | string | Subject code |
| Maximum_Marks | integer | Maximum combined marks |
| Passing_Marks | integer | Synthetic minimum passing marks |

## marks.csv
| Column | Type | Meaning |
|---|---|---|
| Marks_ID | string | Marks record key |
| Student_ID | string | Student foreign key |
| Subject_ID | string | Subject foreign key |
| Internal_Marks | integer/blank | Internal score (synthetic maximum 40) |
| External_Marks | integer/blank | External score (synthetic maximum 60) |
| Total_Marks | integer/blank | Combined score |
| Grade | string/blank | Derived grade, populated later |
| Result | string/blank | Derived result, populated later |
| Record_Status | string | PRESENT, ABSENT or MISSING |

## attendance.csv
| Column | Type | Meaning |
|---|---|---|
| Attendance_ID | string | Attendance record key |
| Student_ID | string | Student foreign key |
| Subject_ID | string | Subject foreign key |
| Total_Classes | integer | Conducted classes |
| Present_Classes | integer | Attended classes |
| Absent_Classes | integer | Missed classes |
| Attendance_Percentage | decimal | Present / total × 100 |

## academic_terms.csv
| Column | Type | Meaning |
|---|---|---|
| Term_ID | string | Term key |
| Academic_Year | string | Academic year |
| Semester | string | Semesters covered by synthetic term |
| Start_Date | ISO date | Term start |
| End_Date | ISO date | Term end |

## Injected quality cases
- Duplicate student master row, marks row and attendance row.
- Missing department and missing attendance Student_ID.
- Inconsistent student-name whitespace/case.
- Internal mark above maximum and negative external mark.
- One explicitly absent marks record and one missing marks record.
- Exact marks boundary cases: 0, the configured passing mark (40 in the current demo), and the configured maximum (100).
- Invalid record status, an ABSENT row with populated score components, fractional attendance class count and impossible attendance count.
- Blank attendance Student_ID, blank student Department, inconsistent Student_Name casing/spacing and missing marks/result values in the raw source.
- Attendance present count greater than total classes.

## Business-rule caveats
The 40/60 internal/external split and 40/100 passing marks are synthetic design choices, not confirmed institutional regulations. Grade boundaries and attendance threshold remain configurable and require confirmation before institutional interpretation.
