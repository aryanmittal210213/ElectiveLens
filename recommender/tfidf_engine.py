from sklearn.feature_extraction.text import TfidfVectorizer


def create_tfidf_matrix(documents):
    """
    Convert course documents into TF-IDF vectors.

    Returns:
        vectorizer: fitted TF-IDF vectorizer
        matrix: TF-IDF matrix for the courses
    """

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1,
    )

    matrix = vectorizer.fit_transform(documents)

    return vectorizer, matrix


def transform_user_document(vectorizer, user_document):
    """
    Transform the student's document using
    the already-fitted course vectorizer.
    """

    return vectorizer.transform([user_document])


def get_feature_names(vectorizer):
    """Return the vocabulary learned by TF-IDF."""

    return vectorizer.get_feature_names_out()
