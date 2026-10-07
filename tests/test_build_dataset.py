from pathlib import Path

import pytest

from parser.build_dataset import parse_courses, pdf_to_text

SAMPLE = """Front matter that must be ignored.
Core Course Descriptions
______________________________________________
Course: Toy Algorithms
School School of Engineering
Department Computer Science and Engineering
Course Code CSD901
Course Title Toy Algorithms
Credits 4
L-T-P (Contact Hours) 3-0-1 (L:3H - T:0H - P:2H)
Prerequisites CSD101
Category Major Core
Course Summary:
Invented text about sorting
and searching puzzles for testing the parser end to end.
Learning Outcomes: On successful completion of the course, students will be able to:
1. Sort things.
2. Search things.
Curriculum Content:
1. Sorting basics and big-oh notation, plus lots of other invented words.
2. Searching basics with hashing and trees and graphs.
Textbooks and References:
1. Nobody, A Made Up Book.
__________________________________________________________________________________________
Elective Course Descriptions
__________________________________________________________________________________________
Course: Toy Learning
School School of Engineering
Department CSE
Course Code CSD902
Course Title Toy Learning
Credits 3
L-T-P (Contact Hours) 2-0-1 (L:2H - T:0H - P:2H)
Prerequisites CSD102/201, 
CSD210/209
Category Major Elective
Course Summary:
Invented description of learning from data with invented models and invented evaluation methods.
Curriculum Content:
Invented topics: regression, trees, clustering, evaluation, and invented extras.
Textbooks and References:
Research papers
__________________________________________________________________________________________
Special Topics in Toys
School School of Engineering
Department Computer Science and Engineering
Course Code CSD903
Course Title Special Topics in Toys
Credits 3
L-T-P (Contact Hours) 3-0-0 (L:3H - T:0H - P:0H)
Prerequisites -
Category Major Elective
Course Summary:
The course emphasis is on special topics.
Curriculum Content:
The detailed content will be provided by the faculty conducting the course as and when required.
Textbooks and References:
Research papers
__________________________________________________________________________________________
Course: Toy Lab
School School of Engineering
Department Computer Science and Engineering
Course Code CSD904
Course Title Toy Lab
Credits 2
L-T-P (Contact Hours) 0-0-2 (L:0H - T:0H - P:4H)
Prerequisites CSD102/201
Category Major Core
Course Summary:
Students build small invented programs.
__________________________________________________________________________________________
"""


@pytest.fixture(scope="module")
def rows():
    return {r["course_code"]: r for r in parse_courses(SAMPLE)}


def test_finds_all_courses(rows):
    assert set(rows) == {"CSD901", "CSD902", "CSD903", "CSD904"}


def test_metadata_fields(rows):
    r = rows["CSD901"]
    assert (r["course_title"], r["credits"], r["ltp"], r["course_type"]) == ("Toy Algorithms", 4, "3-0-1", "Major Core")
    assert r["prerequisites"] == "CSD101"
    assert r["department"] == "Computer Science and Engineering"
    assert rows["CSD902"]["department"] == "Computer Science and Engineering"   # 'CSE' normalised


def test_text_fields_and_no_leakage_between_courses(rows):
    r = rows["CSD901"]
    assert r["description"].startswith("Invented text about sorting and searching")
    assert "Sort things" in r["learning_outcomes"] and "Sorting basics" in r["topics"]
    assert "Nobody" not in r["topics"] and "Toy Learning" not in r["topics"]
    assert "Course:" not in rows["CSD904"]["description"] and "Special Topics" not in rows["CSD902"]["topics"]


def test_wrapped_and_empty_prerequisites(rows):
    assert rows["CSD902"]["prerequisites"] == "CSD102/201, CSD210/209"
    assert rows["CSD903"]["prerequisites"] == ""


def test_indexable_flags(rows):
    assert rows["CSD901"]["indexable"] and rows["CSD902"]["indexable"]
    assert not rows["CSD903"]["indexable"]      # placeholder
    assert not rows["CSD904"]["indexable"]      # too little text


def test_real_pdf_roundtrip(tmp_path):
    """Build a real PDF from the invented sample and parse it back through PyMuPDF."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    pdf = tmp_path / "s.pdf"
    c = canvas.Canvas(str(pdf), pagesize=A4)
    y = 800
    for line in SAMPLE.splitlines():
        if y < 40:
            c.showPage(); y = 800
        c.setFont("Helvetica", 8); c.drawString(30, y, line[:130]); y -= 10
    c.save()
    got = {r["course_code"]: r for r in parse_courses(pdf_to_text(pdf))}
    assert set(got) == {"CSD901", "CSD902", "CSD903", "CSD904"}
    assert got["CSD902"]["prerequisites"] == "CSD102/201, CSD210/209" and got["CSD901"]["credits"] == 4
