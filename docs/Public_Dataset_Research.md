# Public dataset research and selection rationale

The project brief requires reviewing public student datasets before choosing a synthetic dataset. The following three candidates were reviewed. None exactly matches this project's desired institution-style combination of student master, subject-level internal/external marks, per-subject attendance, and academic-term keys; the reproducible synthetic dataset is therefore retained for the full demonstration pipeline.

| Dataset | Source and direct URL | Licence | Relevant columns / content | Fit and limitations |
|---|---|---|---|---|
| UCI Student Performance (Cortez & Silva, 2008) | [UCI dataset 320](https://archive.ics.uci.edu/dataset/320/student+performance), DOI: 10.24432/C5TG7T | CC BY 4.0 | School, sex, age, address, study/support attributes, absences, G1/G2/G3 grades and final grade | Has grades and absence counts, but not the requested per-subject attendance percentage or separate internal/external marks. Dataset represents two Portuguese secondary schools; records are separated by subject and there is no universal student ID across both subject files. |
| Open University Learning Analytics Dataset (OULAD) | [UCI dataset 349](https://archive.ics.uci.edu/dataset/349/open+university+learning+analytics+dataset) and [Open University project page](https://research.stem.open.ac.uk/ouanalyse/dataset/) | CC BY 4.0 | Student/course registration, assessment IDs, scores, submission dates, module/presentation, VLE interaction logs | Rich relational learning analytics and assessment scores, but not classroom attendance counts/percentages or a simple internal/external assessment split. It is larger and requires substantial joins and interpretation. |
| Students Academic Performance Evaluation Dataset (Mendeley Data, 2024) | [Mendeley Data DOI 10.17632/dc3797vf3t.1](https://data.mendeley.com/datasets/dc3797vf3t/1) | CC BY 4.0 | 1,195 respondents and 31 features including CGPA, SGPA, class attendance, study habits and student status | Includes attendance and academic outcome features, but the published description is survey-based and does not provide subject-level marks/attendance fact records needed for this star schema. |

## Selection
The three public candidates are useful for benchmarking and future external validation, but none fully satisfies the project's required relational grain and calculation demonstrations. The current project therefore uses deterministic synthetic records with explicit defects. This is a modelling and software-testing choice, not a claim that synthetic values represent any college.

## Data governance
- Do not merge any public dataset into the synthetic project without recording its provenance and schema mapping.
- Follow the dataset licence and cite its creators.
- Never infer a student's identity from de-identified or survey data.
- If the institution later supplies data, use written permission, data minimisation and anonymisation before loading it.
