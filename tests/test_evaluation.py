import pandas as pd

from recommender.recommend import recommend_courses
from baseline import baseline_recommend


TEST_PROFILES = [
    {
        "name": "AI / ML Student",
        "interests": ["Artificial Intelligence", "Machine Learning"],
        "subjects": ["Programming", "Mathematics"],
        "career": "AI / ML Engineer",
        "difficulty": "Intermediate",
        "relevant_courses": ["CSD361", "CSD350", "CSD355"],
    },
    {
        "name": "Data Science Student",
        "interests": ["Data Science", "Machine Learning"],
        "subjects": ["Mathematics", "Statistics"],
        "career": "Data Scientist / Data Analyst",
        "difficulty": "Intermediate",
        "relevant_courses": ["CSD355", "CSD361"],
    },
    {
        "name": "Cyber Security Student",
        "interests": ["Cyber Security", "Security"],
        "subjects": ["Programming", "Computer Networks"],
        "career": "Cyber Security",
        "difficulty": "Intermediate",
        "relevant_courses": ["CSD353", "CSD356"],
    },
]


def precision_at_5(recommended_courses, relevant_courses):
    relevant = sum(
        1
        for course in recommended_courses
        if course in relevant_courses
    )
    return relevant / 5


if __name__ == "__main__":

    baseline_scores = []
    ir_scores = []

    print()
    print("==========================================")
    print(" ELECTIVE LENS - IR EVALUATION")
    print("==========================================")
    print()

    for profile in TEST_PROFILES:

        # ---------------- BASELINE ----------------

        baseline_results = baseline_recommend(
            interests=profile["interests"],
            subjects=profile["subjects"],
            career=profile["career"],
            difficulty=profile["difficulty"],
            top_k=5,
        )

        baseline_codes = baseline_results["course_code"].tolist()

        baseline_precision = precision_at_5(
            baseline_codes,
            profile["relevant_courses"],
        )

        # ---------------- IR SYSTEM ----------------

        ir_results = recommend_courses(
            interests=profile["interests"],
            subjects=profile["subjects"],
            career=profile["career"],
            difficulty=profile["difficulty"],
            top_k=5,
        )

        ir_codes = ir_results["course_code"].tolist()

        ir_precision = precision_at_5(
            ir_codes,
            profile["relevant_courses"],
        )

        baseline_scores.append(baseline_precision)
        ir_scores.append(ir_precision)

        # ---------------- PRINT RESULTS ----------------

        print(profile["name"])
        print("------------------------------------------")

        print("Baseline:")
        print("  " + ", ".join(baseline_codes))
        print(f"  Precision@5: {baseline_precision:.3f}")
        print()

        print("IR System:")
        print("  " + ", ".join(ir_codes))
        print(f"  Precision@5: {ir_precision:.3f}")
        print()

    # ---------------- SUMMARY ----------------

    baseline_mean = sum(baseline_scores) / len(baseline_scores)
    ir_mean = sum(ir_scores) / len(ir_scores)

    improvement = ir_mean - baseline_mean

    print("==========================================")
    print(" SUMMARY")
    print("==========================================")
    print()

    print(
        f"Baseline Mean Precision@5 : {baseline_mean:.3f}"
    )

    print(
        f"IR System Mean Precision@5 : {ir_mean:.3f}"
    )

    print(
        f"Improvement                : {improvement:+.3f}"
    )

    print()
    print("==========================================")