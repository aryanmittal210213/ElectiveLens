\# 🎓 ElectiveLens



\### IR-Powered Personalized Elective Recommendation System



> \*\*Find the electives that fit u.\*\*



ElectiveLens is a personalized elective recommendation system that uses \*\*Information Retrieval (IR)\*\* techniques to recommend relevant university electives based on a student's interests, strong subjects, career goals, and preferred difficulty level.



Instead of relying only on manually defined keywords, ElectiveLens represents both the student's profile and course information as text and uses \*\*TF-IDF, Cosine Similarity, Jaccard Similarity, and a course-quality signal\*\* to rank the most relevant electives.



\---



\## ✨ Features



\* 🎯 Personalized \*\*Top-K elective recommendations\*\*

\* 🔎 \*\*TF-IDF\*\* based course representation

\* 📐 \*\*Cosine Similarity\*\* for semantic/text relevance

\* 🔗 \*\*Jaccard Similarity\*\* for keyword overlap

\* ⭐ Course-quality scoring based on available course information

\* 💡 Human-readable explanations for recommendations

\* 📊 Transparent ranking scores

\* 📚 Course descriptions and topics

\* 🧑‍🎓 Student profile including:



&#x20; \* CGPA

&#x20; \* Current semester

&#x20; \* Interests

&#x20; \* Strong subjects

&#x20; \* Career goal

&#x20; \* Preferred difficulty

\* 🖥️ Interactive Streamlit interface

\* 🧪 Comparison against a simple keyword-overlap baseline



\---



\## 🧠 How ElectiveLens Works



ElectiveLens follows an Information Retrieval pipeline:



```text

&#x20;                STUDENT PROFILE

&#x20;                      │

&#x20;                      ▼

&#x20;             Build User Document

&#x20;                      │

&#x20;                      ▼

&#x20;             Text Preprocessing

&#x20;                      │

&#x20;                      ▼

&#x20;                TF-IDF Vector

&#x20;                      │

&#x20;                      ▼

&#x20;            ┌───────────────────┐

&#x20;            │                   │

&#x20;            ▼                   ▼

&#x20;     Course Corpus       User Representation

&#x20;            │                   │

&#x20;            └─────────┬─────────┘

&#x20;                      ▼

&#x20;             Similarity Scoring

&#x20;                      │

&#x20;            ┌─────────┴─────────┐

&#x20;            ▼                   ▼

&#x20;     Cosine Similarity    Jaccard Similarity

&#x20;            │                   │

&#x20;            └─────────┬─────────┘

&#x20;                      ▼

&#x20;               Quality Score

&#x20;                      │

&#x20;                      ▼

&#x20;                Final Ranking

&#x20;                      │

&#x20;                      ▼

&#x20;                 TOP-K COURSES

&#x20;                      │

&#x20;                      ▼

&#x20;             Explanation Engine

&#x20;                      │

&#x20;                      ▼

&#x20;               Streamlit Results

```



\### Final Ranking Formula



Each course receives a final ranking score:



```text

Final Score =

&#x20;   0.60 × Cosine Similarity

&#x20; + 0.25 × Jaccard Similarity

&#x20; + 0.15 × Quality Score

```



The system then returns the highest-ranked electives.



\---



\## 🔍 Information Retrieval Components



\### 1. TF-IDF



Course information is converted into TF-IDF vectors.



The indexed course document combines information such as:



\* Course title

\* Description

\* Topics

\* Learning outcomes

\* Prerequisites



The student's interests, subjects, career goal, and difficulty preference are combined into a user document.



TF-IDF provides a weighted representation of the terms appearing in these documents.



\---



\### 2. Cosine Similarity



Cosine similarity measures the similarity between the student's TF-IDF representation and each course representation.



A higher cosine similarity indicates stronger textual relevance between the student profile and the course.



\---



\### 3. Jaccard Similarity



Jaccard similarity provides an additional set-based measure of overlap between the words in the student's profile and the course document.



```text

Jaccard(A, B) = |A ∩ B| / |A ∪ B|

```



This gives the ranking system a second relevance signal beyond vector-space similarity.



\---



\### 4. Course Quality Score



A lightweight quality signal is calculated from available course metadata.



The current implementation considers:



\* Course credits

\* Availability of a sufficiently detailed description

\* Availability of topic information



This quality score contributes 15% to the final ranking.



\---



\## 📚 Dataset



The project uses course information derived from the \*\*SNU B.Tech CSE curriculum/prospectus data\*\*.



The dataset is processed by:



```text

parser/build\_dataset.py

```



The generated dataset is stored at:



```text

data/snu\_courses.csv

```



The dataset contains \*\*41 course records\*\*, including:



\* Course code

\* Course title

\* School

\* Department

\* Course type

\* Credits

\* LTP

\* Prerequisites

\* Description

\* Learning outcomes

\* Topics

\* Indexability

\* Source URL



For recommendation, ElectiveLens currently focuses on courses that are:



```text

course\_type = Major Elective

```



and have usable indexable content.



The dataset-building process also records courses for which sufficient indexable information is unavailable rather than silently inventing missing course information.



\---



\## 🛠️ Tech Stack



| Technology   | Purpose                           |

| ------------ | --------------------------------- |

| Python       | Core implementation               |

| Streamlit    | Interactive web application       |

| Pandas       | Dataset processing                |

| Scikit-learn | TF-IDF and cosine similarity      |

| HTML/CSS     | Frontend styling                  |

| Git/GitHub   | Version control and collaboration |



\---



\## 🚀 Setup



\### 1. Clone the repository



```bash

git clone https://github.com/aryanmittal210213/ElectiveLens.git

cd ElectiveLens

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



\### 3. Activate the virtual environment



\#### Windows PowerShell



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\#### Windows Command Prompt



```cmd

venv\\Scripts\\activate

```



\### 4. Install dependencies



```bash

pip install -r requirements.txt

```



\---



\## ▶️ How to Run



From the project root:



```bash

python -m streamlit run app.py

```



The application will open in your browser.



\### Example Student Profile



You can test the system with:



```text

CGPA: 8.0

Semester: 5th Semester



Interests:

\- Artificial Intelligence

\- Machine Learning



Strong Subjects:

\- Programming

\- Mathematics



Career Goal:

\- AI / ML Engineer



Difficulty:

\- Intermediate

```



The system then generates the student's top five recommended electives.



\---



\## 📊 Evaluation



ElectiveLens was evaluated using a small manually judged query set consisting of three student profiles:



1\. AI / ML Student

2\. Data Science Student

3\. Cyber Security Student



The IR-based system was compared against a simple \*\*keyword-overlap baseline\*\*.



\### Mean Precision@5



| System                     | Mean Precision@5 |

| -------------------------- | ---------------: |

| Keyword Baseline           |            0.333 |

| \*\*ElectiveLens IR System\*\* |        \*\*0.400\*\* |

| Improvement                |       \*\*+0.067\*\* |



The initial evaluation shows that the IR-based ranking system achieved a higher mean Precision@5 than the simple keyword baseline on the evaluated profiles.



> \*\*Note:\*\* This is a small judged evaluation set and should not be interpreted as a definitive measure of general recommendation quality. A larger relevance-labelled dataset would provide a stronger evaluation.



\---



\## 🧪 Baseline



The baseline system uses a simple keyword-overlap strategy.



The student's:



\* Interests

\* Strong subjects

\* Career goal



are treated as query terms.



Courses are ranked according to the proportion of query terms appearing in the course information.



This provides a simple reference point for evaluating whether the multi-signal IR approach improves recommendation quality.



The baseline implementation is available in:



```text

tests/baseline.py

```



\---



\## 📁 Project Structure



```text

ElectiveLens/

│

├── app.py

│

├── data/

│   └── snu\_courses.csv

│

├── parser/

│   └── build\_dataset.py

│

├── recommender/

│   ├── \_\_init\_\_.py

│   ├── preprocess.py

│   ├── tfidf\_engine.py

│   ├── similarity.py

│   ├── ranking.py

│   ├── explanations.py

│   └── recommend.py

│

├── tests/

│   ├── baseline.py

│   ├── test\_build\_dataset.py

│   └── test\_evaluation.py

│

├── requirements.txt

├── .gitignore

└── README.md

```



\### Module Overview



| File                                                  | Responsibility                          |

| ----------------------------------------------------- | --------------------------------------- |

| `app.py`                                              | Streamlit user interface                |

| `preprocess.py`                                       | Text cleaning and document construction |

| `tfidf\_engine.py`                                     | TF-IDF vectorization                    |

| `similarity.py`                                       | Cosine and Jaccard similarity           |

| `ranking.py`                                          | Quality scoring and final ranking       |

| `explanations.py`                                     | Recommendation explanations             |

| `recommend.py`                                        | End-to-end recommendation pipeline      |

| `build\_dataset.py`                                    | Dataset generation                      |

| `baseline.py`                                         | Keyword-overlap baseline                |

| `test\_evaluation.py`                                  | Evaluation experiments                  |

| `test\_build\_dataset.File	Responsibility               |                                         |

| app.py	Streamlit user interface                       |                                         |

| preprocess.py	Text cleaning and document construction |                                         |

| tfidf\_engine.py	TF-IDF vectorization                  |                                         |

| similarity.py	Cosine and Jaccard similarity           |                                         |

| ranking.py	Quality scoring and final ranking          |                                         |

| explanations.py	Recommendation explanations           |                                         |

| recommend.py	End-to-end recommendation pipeline       |                                         |

| build\_dataset.py	Dataset generation                   |                                         |

| baseline.py	Keyword-overlap baseline                  |                                         |

| test\_evaluation.py	Evaluation experiments             |                                         |

| test\_build\_dataset.py	Dataset validation tests        |                                         |

| ✅ What Currently Works                                |                                         |

| Recommendation Engine                                 |                                         |



Student profile input



Course corpus construction



Text preprocessing



TF-IDF vectorization



User-vector generation



Cosine similarity



Jaccard similarity



Course quality scoring



Weighted final ranking



Top-K recommendation generation



Recommendation explanations



Dataset Pipeline



Automated dataset construction



Course metadata extraction



Course filtering



Indexability handling



Dataset validation



Application



Interactive Streamlit interface



Student profile form



Recommendation cards



Match score visualization



Similarity score visualization



Course descriptions



Topic information



IR ranking details



Responsive frontend styling



Evaluation



Keyword baseline



Judged test profiles



Precision@5 evaluation



Baseline comparisonpy` | Dataset validation tests                |



\---



\## ✅ What Currently Works



\### Recommendation Engine



\* \[x] Student profile input

\* \[x] Course corpus construction

\* \[x] Text preprocessing

\* \[x] TF-IDF vectorization

\* \[x] User-vector generation

\* \[x] Cosine similarity

\* \[x] Jaccard similarity

\* \[x] Course quality scoring

\* \[x] Weighted final ranking

\* \[x] Top-K recommendation generation

\* \[x] Recommendation explanations



\### Dataset Pipeline



\* \[x] Automated dataset construction

\* \[x] Course metadata extraction

\* \[x] Course filtering

\* \[x] Indexability handling

\* \[x] Dataset validation



\### Application



\* \[x] Interactive Streamlit interface

\* \[x] Student profile form

\* \[x] Recommendation cards

\* \[x] Match score visualization

\* \[x] Similarity score visualization

\* \[x] Course descriptions

\* \[x] Topic information

\* \[x] IR ranking details

\* \[x] Responsive frontend styling



\### Evaluation



\* \[x] Keyword baseline

\* \[x] Judged test profiles

\* \[x] Precision@5 evaluation

\* \[x] Baseline comparison



\---



\## 🚧 Planned Improvements



The current system is a working prototype. The following improvements are planned:



\### 1. Larger Evaluation Dataset



Expand the manually judged query set with more student profiles and relevance labels.



This would allow evaluation using additional metrics such as:



\* Recall@K

\* F1@K

\* Mean Average Precision

\* NDCG@K



\### 2. Stronger Personalization



The current interface collects CGPA and semester information, but these fields are \*\*not yet used directly in the ranking formula\*\*.



Future versions can incorporate:



\* Semester eligibility

\* CGPA requirements

\* Prerequisite matching

\* Academic history

\* Course workload



into the recommendation process.



\### 3. Better Cold-Start Handling



Improve recommendations when a student provides very little profile information.



Possible approaches include:



\* Popularity priors

\* Course metadata

\* Department-level preferences

\* Content-based fallback recommendations



\### 4. Diversity-Aware Ranking



The current system primarily optimizes relevance.



A future version could add diversity-aware re-ranking so that the Top-K results are not overly concentrated around a single topic.



\### 5. Improved Explainability



Future explanations can expose the strongest matching terms and the specific course sections responsible for the recommendation.



\### 6. Larger Course Corpus



The system can be extended to support a larger university-wide course catalogue.



\---



\## ⚠️ Limitations



\* The current evaluation uses a small manually judged dataset.

\* Course recommendations depend on the quality and completeness of available course descriptions.

\* Some courses may have insufficient information for meaningful text-based indexing.

\* CGPA and semester are currently collected by the interface but are not yet part of the recommendation score.

\* Difficulty preference is currently included in the student profile and explanation layer but does not have a dedicated course-difficulty dataset.

\* The quality score is a lightweight heuristic rather than a learned quality model.

\* The current system is primarily content-based and does not yet learn from historical student-course interactions.



\---



\## 🔐 Data and Privacy



ElectiveLens does not require a student's personal account information.



The application uses the information entered into the recommendation form to generate recommendations during the current session.



No personal student profile database is required by the current implementation.



\---



\## 🤖 AI Usage



AI-assisted development was used during the development process for tasks such as:



\* Debugging implementation issues

\* Explaining programming concepts

\* Suggesting implementation approaches

\* Improving frontend presentation

\* Assisting with documentation



The final project integrates and tests the generated suggestions within the team's own implementation.



The recommendation pipeline, dataset processing, evaluation setup, and application code are included in this repository.



\---



\## 👥 Team



\*\*ElectiveLens — IR Hackathon / CSD358\*\*



| Contributor  | Role                                        |

| ------------ | ------------------------------------------- |

| Kriti Sharma | Development, IR pipeline, frontend, testing |

| Aryan Mittal | Development and project collaboration       |



> Update the roles above to accurately reflect the actual division of work before submission.



\---



\## 📌 Project Status



\*\*Current status: Working prototype\*\*



ElectiveLens currently provides an end-to-end personalized elective recommendation pipeline:



```text

Student Profile

&#x20;     ↓

Text Representation

&#x20;     ↓

TF-IDF

&#x20;     ↓

Cosine + Jaccard

&#x20;     ↓

Quality Scoring

&#x20;     ↓

Weighted Ranking

&#x20;     ↓

Top-K Recommendations

&#x20;     ↓

Explainable Results

```



The system is functional and evaluated against a simple keyword-based baseline, while the planned improvements provide a clear path toward a larger and more robust recommendation platform.



\---



\## 📄 Academic Context



This project was developed as part of the \*\*CSD358 Information Retrieval Hackathon – Midsem Assignment\*\*, under the \*\*Recommender Systems and Personalization\*\* track.



The project demonstrates how Information Retrieval techniques can be applied to personalized academic course recommendation.



\---



\## ⭐ Acknowledgements



\* Course information: SNU B.Tech CSE curriculum/prospectus source used by the dataset-building pipeline.

\* Python ecosystem: Pandas, Scikit-learn, and Streamlit.

\* GitHub for version control and collaborative development.



\---



\### License



This project was developed for academic purposes.



