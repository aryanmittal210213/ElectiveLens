import pandas as pd


def calculate_quality_score(row):
    """
    Calculate a simple quality score for a course.

    Higher credits and richer course information
    slightly improve the score.
    """

    score = 0.0

    # Credits contribution
    try:
        credits = float(row.get("credits", 0))
        score += min(credits / 4.0, 1.0) * 0.4
    except (ValueError, TypeError):
        pass

    # Description quality
    description = str(row.get("description", ""))
    if len(description) >= 50:
        score += 0.3

    # Topics quality
    topics = str(row.get("topics", ""))
    if len(topics) >= 30:
        score += 0.3

    return score


def rank_courses(
    df,
    cosine_scores,
    jaccard_scores,
    top_k=5,
):
    """
    Combine similarity scores and quality score,
    then return the top-k courses.
    """

    result = df.copy()

    result["cosine_score"] = cosine_scores
    result["jaccard_score"] = jaccard_scores

    result["quality_score"] = result.apply(
        calculate_quality_score,
        axis=1,
    )

    # Weighted final score
    result["final_score"] = (
        0.60 * result["cosine_score"]
        + 0.25 * result["jaccard_score"]
        + 0.15 * result["quality_score"]
    )

    result = result.sort_values(
        "final_score",
        ascending=False,
    )

    return result.head(top_k).reset_index(drop=True)
