def generate_explanation(course, user_profile):
    """
    Generate human-readable reasons explaining
    why a course was recommended.
    """

    reasons = []

    interests = [
        str(item).lower()
        for item in user_profile.get("interests", [])
    ]

    subjects = [
        str(item).lower()
        for item in user_profile.get("subjects", [])
    ]

    career = str(
        user_profile.get("career", "")
    ).lower()

    difficulty = str(
        user_profile.get("difficulty", "")
    ).lower()

    course_text = " ".join([
        str(course.get("course_title", "")),
        str(course.get("description", "")),
        str(course.get("topics", "")),
        str(course.get("learning_outcomes", "")),
    ]).lower()

    # Interest match
    for interest in interests:
        keywords = interest.split()

        if any(keyword in course_text for keyword in keywords):
            reasons.append(
                f"Matches your interest in {interest.title()}."
            )
            break

    # Subject match
    for subject in subjects:
        keywords = subject.split()

        if any(keyword in course_text for keyword in keywords):
            reasons.append(
                f"Connects with your strength in {subject.upper()}."
            )
            break

    # Career match
    career_keywords = {
        "software developer": [
            "software",
            "programming",
            "development",
        ],
        "data scientist/analyst": [
            "data",
            "analytics",
            "statistics",
        ],
        "ai/ml engineer": [
            "artificial intelligence",
            "machine learning",
            "deep learning",
        ],
        "cyber security": [
            "security",
            "cryptography",
            "cyber",
        ],
        "cloud/devops": [
            "cloud",
            "distributed",
            "system",
        ],
        "higher studies/research": [
            "research",
            "advanced",
        ],
    }

    keywords = career_keywords.get(career, [])

    if any(keyword in course_text for keyword in keywords):
        reasons.append(
            f"Relevant to your goal of {user_profile.get('career', '')}."
        )

    # Difficulty match
    if difficulty:
        reasons.append(
            f"Considered for your preferred "
            f"{user_profile.get('difficulty', '')} difficulty level."
        )

    # Fallback
    if not reasons:
        reasons.append(
            "Recommended based on the overall similarity "
            "between your profile and this course."
        )

    return reasons


def explain_recommendations(recommendations, user_profile):
    """
    Add explanation reasons to every recommended course.
    """

    recommendations = recommendations.copy()

    recommendations["reasons"] = recommendations.apply(
        lambda course: generate_explanation(
            course,
            user_profile,
        ),
        axis=1,
    )

    return recommendations
