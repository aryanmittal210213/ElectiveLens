import pandas as pd
import re


# ---------------------------------------------------------
# SIMPLE KEYWORD BASELINE
# ---------------------------------------------------------

def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def baseline_recommend(
    interests,
    subjects,
    career,
    difficulty,
    top_k=5,
):
    """
    Simple keyword-matching baseline.

    This is intentionally simpler than the IR system.
    It does not use TF-IDF, cosine similarity,
    Jaccard similarity, or quality scoring.
    """

    df = pd.read_csv("data/snu_courses.csv")

    # Only selectable Major Electives.
    df = df[
        df["course_type"].astype(str).str.strip().str.lower()
        == "major elective"
    ].copy()

    # Only courses with usable content.
    df = df[
        df["indexable"].astype(str).str.lower() == "true"
    ].copy()

    query_terms = []

    query_terms.extend(interests)
    query_terms.extend(subjects)

    if career:
        query_terms.append(career)

    query = clean_text(" ".join(query_terms))
    query_words = set(query.split())

    scores = []

    for _, course in df.iterrows():

        course_text = clean_text(
            " ".join([
                str(course.get("course_title", "")),
                str(course.get("description", "")),
                str(course.get("topics", "")),
                str(course.get("learning_outcomes", "")),
            ])
        )

        course_words = set(course_text.split())

        # Count matching query words.
        matches = query_words & course_words

        if query_words:
            score = len(matches) / len(query_words)
        else:
            score = 0.0

        scores.append(score)

    df["baseline_score"] = scores

    df = df.sort_values(
        "baseline_score",
        ascending=False,
    )

    return df.head(top_k).reset_index(drop=True)


# ---------------------------------------------------------
# TEST PROFILES
# ---------------------------------------------------------

TEST_PROFILES = [
    {
        "name": "AI / ML Student",
        "interests": [
            "Artificial Intelligence",
            "Machine Learning",
        ],
        "subjects": [
            "Programming",
            "Mathematics",
        ],
        "career": "AI/ML Engineer",
        "difficulty": "Intermediate",
        "relevant_courses": [
            "CSD361",
            "CSD350",
            "CSD355",
        ],
    },

    {
        "name": "Data Science Student",
        "interests": [
            "Data Science",
            "Machine Learning",
        ],
        "subjects": [
            "Mathematics",
            "Statistics",
        ],
        "career": "Data Scientist / Data Analyst",
        "difficulty": "Intermediate",
        "relevant_courses": [
            "CSD355",
            "CSD361",
        ],
    },

    {
        "name": "Cyber Security Student",
        "interests": [
            "Cyber Security",
            "Security",
        ],
        "subjects": [
            "Programming",
            "Computer Networks",
        ],
        "career": "Cyber Security",
        "difficulty": "Intermediate",
        "relevant_courses": [
            "CSD353",
            "CSD356",
        ],
    },
]


# ---------------------------------------------------------
# PRECISION@5
# ---------------------------------------------------------

def precision_at_5(
    recommended_courses,
    relevant_courses,
):
    relevant = sum(
        1
        for course in recommended_courses
        if course in relevant_courses
    )

    return relevant / 5


# ---------------------------------------------------------
# RUN BASELINE EVALUATION
# ---------------------------------------------------------

if __name__ == "__main__":

    all_scores = []

    print()
    print("==========================================")
    print(" ELECTIVE LENS - KEYWORD BASELINE")
    print("==========================================")
    print()

    for profile in TEST_PROFILES:

        recommendations = baseline_recommend(
            interests=profile["interests"],
            subjects=profile["subjects"],
            career=profile["career"],
            difficulty=profile["difficulty"],
            top_k=5,
        )

        recommended_codes = (
            recommendations["course_code"].tolist()
        )

        precision = precision_at_5(
            recommended_codes,
            profile["relevant_courses"],
        )

        all_scores.append(precision)

        print(
            f"{profile['name']}:"
        )

        print(
            "  Recommended:",
            ", ".join(recommended_codes)
        )

        print(
            f"  Precision@5: {precision:.3f}"
        )

        print()

    mean_precision = sum(all_scores) / len(all_scores)

    print("------------------------------------------")
    print(
        f"Mean Precision@5: "
        f"{mean_precision:.3f}"
    )
    print("------------------------------------------")
    print()