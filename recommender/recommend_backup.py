import pandas as pd
from pathlib import Path


DATA_FILE = Path("data/snu_courses.csv")


def load_courses():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}. "
            "Run parser/build_dataset.py first."
        )

    return pd.read_csv(DATA_FILE)


def normalize(text):
    if pd.isna(text):
        return ""
    return str(text).lower()


def course_text(course):
    fields = [
        course.get("course_title", ""),
        course.get("description", ""),
        course.get("learning_outcomes", ""),
        course.get("topics", ""),
        course.get("prerequisites", ""),
    ]

    return normalize(" ".join(str(x) for x in fields))


def keyword_score(text, keywords):
    if not keywords:
        return 0, []

    matched = []

    for keyword in keywords:
        if normalize(keyword) in text:
            matched.append(keyword)

    return len(matched), matched


def career_keywords(career):
    mapping = {
        "Software Developer": [
            "software",
            "programming",
            "algorithm",
            "database",
            "systems",
            "object oriented",
        ],

        "Data Scientist / Data Analyst": [
            "data",
            "statistics",
            "machine learning",
            "data mining",
            "analytics",
            "probability",
        ],

        "AI / ML Engineer": [
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "neural",
            "computer vision",
            "natural language",
            "nlp",
        ],

        "Cyber Security": [
            "security",
            "cryptography",
            "cyber",
            "information security",
            "network",
        ],

        "Cloud / DevOps": [
            "systems",
            "network",
            "software",
            "performance",
            "distributed",
        ],

        "Higher Studies / Research": [
            "theory",
            "research",
            "mathematics",
            "computational",
            "modeling",
        ],

        "Not Sure Yet": [],
    }

    return mapping.get(career, [])


def difficulty_keywords(difficulty):
    mapping = {
        "Beginner": [
            "introduction",
            "foundation",
            "basic",
        ],

        "Intermediate": [
            "advanced",
            "applied",
            "design",
            "analysis",
            "systems",
        ],

        "Advanced": [
            "advanced",
            "deep",
            "computational",
            "theory",
            "performance",
            "cryptography",
        ],
    }

    return mapping.get(difficulty, [])


def recommend_courses(
    interests,
    subjects,
    career,
    difficulty,
    top_n=5,
):
    df = load_courses()

    # Only Major Electives should be recommended.
    df = df[
        df["course_type"].astype(str).str.lower()
        == "major elective"
    ].copy()

    results = []

    career_words = career_keywords(career)
    difficulty_words = difficulty_keywords(difficulty)

    for _, course in df.iterrows():

        text = course_text(course)

        interest_score, matched_interests = keyword_score(
            text,
            interests,
        )

        subject_score, matched_subjects = keyword_score(
            text,
            subjects,
        )

        career_score, matched_career = keyword_score(
            text,
            career_words,
        )

        difficulty_score, matched_difficulty = keyword_score(
            text,
            difficulty_words,
        )

        raw_score = (
            interest_score * 35
            + subject_score * 25
            + career_score * 30
            + difficulty_score * 10
        )

        max_possible = (
            max(len(interests), 1) * 35
            + max(len(subjects), 1) * 25
            + max(len(career_words), 1) * 30
            + max(len(difficulty_words), 1) * 10
        )

        match_percentage = min(
            100,
            round((raw_score / max_possible) * 100),
        )

        reasons = []

        if matched_interests:
            reasons.append(
                "Matches interests: "
                + ", ".join(matched_interests)
            )

        if matched_subjects:
            reasons.append(
                "Matches strong subjects: "
                + ", ".join(matched_subjects)
            )

        if matched_career:
            reasons.append(
                "Relevant to career goal"
            )

        if matched_difficulty:
            reasons.append(
                "Matches learning preference"
            )

        if not reasons:
            reasons.append(
                "Related to the selected academic profile"
            )

        results.append({
            "course_code": course["course_code"],
            "course_title": course["course_title"],
            "credits": course["credits"],
            "match_score": match_percentage,
            "reasons": reasons,
            "description": course["description"],
            "topics": course["topics"],
        })

    result_df = pd.DataFrame(results)

    if result_df.empty:
        return result_df

    result_df = result_df.sort_values(
        by="match_score",
        ascending=False,
    ).reset_index(drop=True)

    return result_df.head(top_n)
