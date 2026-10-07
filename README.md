# 🎓 ElectiveLens

### IR-Powered Personalized Elective Recommendation System

> **Find the electives that fit u.**

ElectiveLens is a personalized elective recommendation system that uses **Information Retrieval (IR)** techniques to recommend relevant university electives based on a student's interests, strong subjects, career goals, and preferred difficulty.

Instead of relying only on manually defined keywords, ElectiveLens represents student profiles and course information as text and ranks courses using **TF-IDF, Cosine Similarity, Jaccard Similarity, and a course-quality signal**.

---

## ✨ Features

- 🎯 Personalized Top-K elective recommendations
- 🔎 TF-IDF based course representation
- 📐 Cosine similarity
- 🔗 Jaccard similarity
- ⭐ Course-quality scoring
- 💡 Recommendation explanations
- 📊 Transparent ranking scores
- 🖥️ Interactive Streamlit interface
- 🧪 Comparison with a keyword-based baseline

---

## 🧠 How It Works

```text

Student Profile
      ↓
Text Preprocessing
      ↓
TF-IDF Representation
      ↓
Cosine + Jaccard Similarity
      ↓
Quality Score
      ↓
Weighted Ranking
      ↓
Top-K Electives
      ↓
Explanations
Ranking Formula
Final Score =
    0.60 × Cosine Similarity
  + 0.25 × Jaccard Similarity
  + 0.15 × Quality Score

Course documents are built from the course title, description, topics, learning outcomes, and prerequisites.

📚 Dataset

The project uses course information derived from the SNU B.Tech CSE curriculum/prospectus.

The generated dataset contains 41 course records with information such as:

Course code and title
Course type and credits
Prerequisites
Description
Learning outcomes
Topics

The recommender focuses on Major Elective courses with usable indexable content.

Dataset generation:

parser/build_dataset.py
        ↓
data/snu_courses.csv
📊 Evaluation

ElectiveLens was evaluated using three manually judged student profiles:

AI / ML
Data Science
Cyber Security

The IR system was compared against a simple keyword-overlap baseline using Precision@5.

System	Mean Precision@5
Keyword Baseline	0.333
ElectiveLens IR System	0.400
Improvement	+0.067

The evaluation is based on a small judged set and is intended as a prototype-level comparison.

🛠️ Tech Stack
Python
Streamlit
Pandas
Scikit-learn
TF-IDF
Cosine Similarity
Jaccard Similarity
HTML/CSS
Git/GitHub
📁 Project Structure
ElectiveLens/
├── app.py
├── data/
│   └── snu_courses.csv
├── parser/
│   └── build_dataset.py
├── recommender/
│   ├── preprocess.py
│   ├── tfidf_engine.py
│   ├── similarity.py
│   ├── ranking.py
│   ├── explanations.py
│   └── recommend.py
├── tests/
│   ├── baseline.py
│   ├── test_build_dataset.py
│   └── test_evaluation.py
├── requirements.txt
└── README.md
🚀 Setup
git clone https://github.com/aryanmittal210213/ElectiveLens.git
cd ElectiveLens

python -m venv venv
Windows
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
🤖 AI Usage

AI-assisted development was used for debugging, implementation guidance, programming explanations, frontend refinement, and documentation.

The final system was implemented, integrated, and tested as part of the project.

🎓 Academic Context

Developed for the CSD358 Information Retrieval Hackathon – Midsem Assignment under:

T3 — Recommender Systems and Personalization

The project demonstrates the application of Information Retrieval techniques to personalized academic course recommendation.


📌 Status

Working prototype

ElectiveLens provides an end-to-end pipeline from student profile input to IR-based ranking and explainable elective recommendations.


### Why this version is better

It cuts the README from **~900+ lines to roughly 150 lines**.

And importantly, it removes:

- ❌ the giant roadmap
- ❌ duplicate “What Currently Works” section
- ❌ duplicate module table
- ❌ weird `#`/Markdown corruption
- ❌ repeated explanations of the same IR components
- ❌ unnecessary GitHub-generated content
- ❌ excessive limitation discussion
- ❌ unnecessary “Project Status” pipeline repetition

It still has everything an evaluator needs:

**Problem → IR method → formula → dataset → evaluation → tech stack → structure → setup → AI declaration → team.**

That's the README I'd actually put on the GitHub repo.
give me the whole readme together as copyable text in one go 

Absolutely — here is the entire README in one single copyable block. Just copy everything inside it and replace your current README.md.

# 🎓 ElectiveLens

### IR-Powered Personalized Elective Recommendation System

> **Find the electives that fit u.**

ElectiveLens is a personalized elective recommendation system that uses **Information Retrieval (IR)** techniques to recommend relevant university electives based on a student's interests, strong subjects, career goals, and preferred difficulty.

Instead of relying only on manually defined keywords, ElectiveLens represents student profiles and course information as text and ranks courses using **TF-IDF, Cosine Similarity, Jaccard Similarity, and a course-quality signal**.

---

## ✨ Features

- 🎯 Personalized Top-K elective recommendations
- 🔎 TF-IDF based course representation
- 📐 Cosine similarity
- 🔗 Jaccard similarity
- ⭐ Course-quality scoring
- 💡 Recommendation explanations
- 📊 Transparent ranking scores
- 🖥️ Interactive Streamlit interface
- 🧪 Comparison with a keyword-based baseline

---

## 🧠 How It Works

```text
Student Profile
      ↓
Text Preprocessing
      ↓
TF-IDF Representation
      ↓
Cosine + Jaccard Similarity
      ↓
Quality Score
      ↓
Weighted Ranking
      ↓
Top-K Electives
      ↓
Explanations
Ranking Formula
Final Score =
    0.60 × Cosine Similarity
  + 0.25 × Jaccard Similarity
  + 0.15 × Quality Score

Course documents are built from the course title, description, topics, learning outcomes, and prerequisites.

📚 Dataset

The project uses course information derived from the SNU B.Tech CSE curriculum/prospectus.

The generated dataset contains 41 course records with information such as:

Course code and title
Course type and credits
Prerequisites
Description
Learning outcomes
Topics

The recommender focuses on Major Elective courses with usable indexable content.

Dataset generation:

parser/build_dataset.py
        ↓
data/snu_courses.csv
📊 Evaluation

ElectiveLens was evaluated using three manually judged student profiles:

AI / ML
Data Science
Cyber Security

The IR system was compared against a simple keyword-overlap baseline using Precision@5.

System	Mean Precision@5
Keyword Baseline	0.333
ElectiveLens IR System	0.400
Improvement	+0.067

The evaluation is based on a small judged set and is intended as a prototype-level comparison.

🛠️ Tech Stack
Python
Streamlit
Pandas
Scikit-learn
TF-IDF
Cosine Similarity
Jaccard Similarity
HTML/CSS
Git/GitHub
📁 Project Structure
ElectiveLens/
├── app.py
├── data/
│   └── snu_courses.csv
├── parser/
│   └── build_dataset.py
├── recommender/
│   ├── preprocess.py
│   ├── tfidf_engine.py
│   ├── similarity.py
│   ├── ranking.py
│   ├── explanations.py
│   └── recommend.py
├── tests/
│   ├── baseline.py
│   ├── test_build_dataset.py
│   └── test_evaluation.py
├── requirements.txt
└── README.md
🚀 Setup
git clone https://github.com/aryanmittal210213/ElectiveLens.git
cd ElectiveLens

python -m venv venv
Windows
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run app.py
🤖 AI Usage

AI-assisted development was used for debugging, implementation guidance, programming explanations, frontend refinement, and documentation.

The final system was implemented, integrated, and tested as part of the project.

🎓 Academic Context

Developed for the CSD358 Information Retrieval Hackathon – Midsem Assignment under:

T3 — Recommender Systems and Personalization

The project demonstrates the application of Information Retrieval techniques to personalized academic course recommendation.

👥 Team
Contributor	Role
Kriti Sharma	Development, IR pipeline, frontend, testing
Aryan Mittal	Project collaboration
📌 Status

Working prototype

ElectiveLens provides an end-to-end pipeline from student profile input to IR-based ranking and explainable elective recommendations.



