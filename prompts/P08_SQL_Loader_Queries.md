# P8 — Oracle SQL Loader and Business Queries

Create a Python loading process using Pandas and python-oracledb. Read cleaned CSVs, connect using environment variables (never hardcode credentials), load dimensions before facts, use bind parameters and transactions, rollback on failure, handle constraint errors, report row counts and make reruns safe.

Write at least 10 Oracle SQL business queries:
1. Top 10 students by total marks.
2. Student-wise overall percentage.
3. Subject-wise average marks.
4. Overall pass percentage.
5. Failed students.
6. Students below attendance threshold.
7. Attendance versus academic performance.
8. Subject-wise failure percentage.
9. Department-wise performance.
10. Tied student ranks.

Use JOIN, GROUP BY, HAVING, CASE, aggregates and analytic functions appropriately. Prevent fact-table grain multiplication. Explain each query and export actual query results to CSV.

**Output:** `src/03_load_sql.py`, `sql/queries.sql`, `reports/sql_results/`.