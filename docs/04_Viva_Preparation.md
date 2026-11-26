# Viva Preparation — Student Performance and Attendance Dashboard

Use the actual repository implementation when answering. The questions below are a practice bank; conduct interactive viva one question at a time and do not memorise unsupported claims.

## Python (8)
1. Why is Python used in this project?
2. What is a Pandas DataFrame?
3. How does read_csv handle blank values?
4. Why use a fixed random seed in synthetic data generation?
5. What is the purpose of a function in the cleaning pipeline?
6. How are rejected rows handled?
7. Why are environment variables used for Oracle credentials?
8. How do you make a Python script reproducible?

## Pandas and NumPy (5)
9. What is the difference between drop_duplicates and duplicated?
10. How do you detect missing values?
11. Why use merge with validate="many_to_one" or "one_to_one"?
12. How is attendance percentage calculated?
13. Why should missing marks not automatically become zero?

## Oracle SQL (7)
14. What is a primary key?
15. What is a foreign key?
16. Explain the difference between fact and dimension tables.
17. What is the purpose of GROUP BY?
18. What is the difference between WHERE and HAVING?
19. What does DENSE_RANK do when marks are tied?
20. Why should two fact tables not be joined carelessly?

## PL/SQL (5)
21. What is PL/SQL and how does it extend SQL?
22. What is the difference between a procedure and a function?
23. What is a package?
24. Why is exception handling important?
25. How does the project handle absent and missing marks?

## Power BI and DAX (7)
26. What is a star schema?
27. What is cardinality in a Power BI relationship?
28. Why is single-direction filtering recommended for this model?
29. What is the difference between a measure and a calculated column?
30. Explain the Pass Percentage DAX measure.
31. What is filter context?
32. How does the dashboard preserve tied student ranks?

## Data modelling (4)
33. What is the grain of Fact_Marks?
34. What is the grain of Fact_Attendance?
35. Why are surrogate keys used in a warehouse?
36. Why are dimensions shared by both fact tables?

## Architecture and business insights (4)
37. Explain the end-to-end flow from raw CSV to dashboard.
38. How do you validate a low-attendance student list?
39. What does a pass percentage mean in this project and what is its denominator?
40. What are the limitations of analysing synthetic data?

## Interactive practice
When practising in ChatGPT, ask one question at a time. Evaluate the answer for correctness, completeness and clarity, then explain corrections in simple English. Do not claim a feature exists unless it is present and tested in the repository.
