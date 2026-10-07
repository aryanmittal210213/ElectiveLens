import re
import pandas as pd


def clean_text(text):
    """Clean and normalize text for NLP processing."""
    if pd.isna(text):
        return ""

    text = str(text).lower()

    # Replace punctuation with spaces.
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra whitespace.
    text = re.sub(r"\s+", " ", text).strip()

    return text


def build_course_document(course):
    """
    Create a searchable document from one course.
    """

    fields = [
        course.get("course_title", ""),
        course.get("description", ""),
        course.get("topics", ""),
        course.get("learning_outcomes", ""),
        course.get("prerequisites", ""),
    ]

    return clean_text(" ".join(str(value) for value in fields))


def build_user_document(
    interests,
    subjects,
    career,
    difficulty,
):
    """
    Convert a student's profile into one text document.
    """

    parts = []

    parts.extend(interests)
    parts.extend(subjects)

    if career:
        parts.append(career)

    if difficulty:
        parts.append(difficulty)

    return clean_text(" ".join(parts))


def prepare_course_corpus(df):
    """
    Create cleaned documents for all courses.
    """

    df = df.copy()

    df["document"] = df.apply(
        build_course_document,
        axis=1,
    )

    return df
