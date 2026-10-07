from sklearn.metrics.pairwise import cosine_similarity


def calculate_cosine_similarity(user_vector, course_matrix):
    """
    Calculate cosine similarity between the student
    and every course.
    """

    scores = cosine_similarity(
        user_vector,
        course_matrix,
    )

    return scores.flatten()


def calculate_jaccard_similarity(user_document, course_documents):
    """
    Calculate Jaccard similarity between the student's
    document and each course document.
    """

    user_words = set(user_document.split())

    scores = []

    for document in course_documents:
        course_words = set(document.split())

        union = user_words | course_words

        if not union:
            scores.append(0.0)
            continue

        intersection = user_words & course_words

        score = len(intersection) / len(union)

        scores.append(score)

    return scores
