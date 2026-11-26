# Data cleaning rules

| Dataset | Issue | Rule |
|---|---|---|
| Students | Missing Student_ID | Quarantine; cannot safely identify record |
| Students | Duplicate Student_ID | Keep first occurrence; quarantine later duplicate |
| Students | Missing Department | Use UNKNOWN; do not infer department |
| Students | Inconsistent name spacing/case | Trim and title-case display name |
| Subjects | Duplicate Subject_ID | Keep first occurrence and quarantine duplicate |
| Marks | Duplicate student-subject row | Keep first occurrence and quarantine later row |
| Marks | Missing/unknown student or subject key | Quarantine; do not create phantom master records |
| Marks | Invalid internal/external component | Quarantine PRESENT row if component is missing or outside synthetic 0–40 / 0–60 bounds |
| Marks | Absent record | Preserve as ABSENT; do not convert to zero |
| Marks | Missing record | Preserve as MISSING; do not convert to zero |
| Marks | Derived total/result/grade | Recalculate from valid components; grade bands are provisional demo rules in the script |
| Attendance | Duplicate student-subject row | Keep first occurrence and quarantine duplicate |
| Attendance | Missing/unknown key | Quarantine |
| Attendance | Impossible class counts | Quarantine if total <= 0, present < 0 or present > total |
| Attendance | Absent count and percentage | Recalculate as total-present and present/total × 100 |
| Academic term | Invalid dates | Quarantine if date parse fails or end date precedes start |

The attendance threshold is not applied during cleaning; it is an analytical filter and remains configurable. The current script uses 75% only as a provisional demonstration setting. The 40/60 assessment split, passing score 40 and grade bands are synthetic sample assumptions pending institutional confirmation.
