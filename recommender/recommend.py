import pandas as pd

from recommender.preprocess import (
    prepare_course_corpus,
    build_user_document,
)

from recommender.tfidf_engine import (
    create_tfidf_matrix,
    transform_user_document,
)

from recommender.similarity import (
    calculate_cosine_similarity,
    calculate_jaccard_similarity,
)

from recommender.ranking import rank_courses

from recommender.explanations import (
    explain_recommendations,
)


def recommend_courses(
    interests,
    subjects,
    career,
    difficulty,
    top_k=5,
):
    """Run the complete TF-IDF recommendation pipeline."""

    df = pd.read_csv("data/snu_courses.csv")

    # Recommend only selectable Major Electives.
    df = df[
        df["course_type"].astype(str).str.strip().str.lower()
        == "major elective"
    ].copy()

    # Keep only courses with usable descriptions/content.
    df = df[
        df["indexable"].astype(str).str.lower() == "true"
    ].copy()

    if df.empty:
        return pd.DataFrame()

    # Build course documents.
    df = prepare_course_corpus(df)

    # Build student's document.
    user_document = build_user_document(
        interests=interests,
        subjects=subjects,
        career=career,
        difficulty=difficulty,
    )

    # TF-IDF course vectors.
    vectorizer, course_matrix = create_tfidf_matrix(
        df["document"].tolist()
    )

    # TF-IDF student vector.
    user_vector = transform_user_document(
        vectorizer,
        user_document,
    )

    # Similarity scores.
    cosine_scores = calculate_cosine_similarity(
        user_vector,
        course_matrix,
    )

    jaccard_scores = calculate_jaccard_similarity(
        user_document,
        df["document"].tolist(),
    )

    # Rank courses using cosine + Jaccard + quality.
    recommendations = rank_courses(
        df=df,
        cosine_scores=cosine_scores,
        jaccard_scores=jaccard_scores,
        top_k=top_k,
    )

    # Explanation information.
    user_profile = {
        "interests": interests,
        "subjects": subjects,
        "career": career,
        "difficulty": difficulty,
    }

    recommendations = explain_recommendations(
        recommendations,
        user_profile,
    )

    return recommendations
