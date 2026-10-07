"""Build data/snu_courses.csv from SNU's official B.Tech CSE prospectus (Course Description pages).

  python build_dataset.py                 # downloads the PDF, parses it, writes data/snu_courses.csv
  python build_dataset.py --pdf my.pdf    # use a PDF you downloaded yourself
  python build_dataset.py --txt my.txt    # use already-extracted text

Source: Shiv Nadar University, Dept. of Computer Science and Engineering, "UG Prospectus B.Tech. CSE (2022 onwards)".
"""
import argparse
import re
import sys
import urllib.request
from pathlib import Path

import pandas as pd

SOURCE_URL = "https://snu.edu.in/site/assets/files/3888/prospectus_b_tech__-_cse_2022onwards.pdf?v=2"
DATA = Path("data")
COLUMNS = ["course_code", "course_title", "school", "department", "course_type", "credits", "ltp",
           "prerequisites", "description", "learning_outcomes", "topics", "indexable", "source_url"]

DEPT_NORMAL = {"CSE": "Computer Science and Engineering"}
TYPE_MAP = {"major core": "Major Core", "major elective": "Major Elective", "es": "Engineering Science"}
PLACEHOLDER = re.compile(r"detailed content will be provided by the faculty", re.I)
CODE = re.compile(r"Course\s+Code\s+([A-Z]{3}\s?\d{3})")


def download_pdf(dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())
    return dest


def pdf_to_text(pdf: Path) -> str:
    import fitz  # PyMuPDF
    with fitz.open(pdf) as doc:
        return "\n".join(page.get_text() for page in doc)


def clean(s: str | None) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


def _between(block: str, start_pat: str, end_pats: list[str]) -> str:
    m = re.search(start_pat, block, re.I)
    if not m:
        return ""
    rest = block[m.end():]
    cut = len(rest)
    for p in end_pats:
        e = re.search(p, rest, re.I)
        if e:
            cut = min(cut, e.start())
    return clean(rest[:cut])


def parse_courses(text: str) -> list[dict]:
    """Every 'Course Code XXX123' starts one course block that runs until the next one."""
    matches = list(CODE.finditer(text))
    rows, seen = [], set()
    for i, m in enumerate(matches):
        code = re.sub(r"\s", "", m.group(1))
        if code in seen:
            continue
        seen.add(code)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[m.start():end]
        # drop the NEXT course's header lines (Course:/School/Department/underscores) that trail this block
        block = re.split(r"\n\s*(?:_{5,}|Course:\s|School\s+School of)", block)[0]
        # school + department sit just BEFORE the 'Course Code' line
        head = text[max(0, m.start() - 250):m.start()]
        dept = re.findall(r"Department\s+([^\n]+)", head)
        school = re.findall(r"School\s+(School of [^\n]+)", head)
        dept = DEPT_NORMAL.get(clean(dept[-1]), clean(dept[-1])) if dept else ""

        title = re.search(r"Course\s+Title\s+([^\n]+)", block)
        credits = re.search(r"Credits\s+(\d+)", block)
        ltp = re.search(r"L-T-P\s*\(Contact Hours\)\s*(\d\s*[-–]\s*\d\s*[-–]\s*\d)", block)
        prereq = re.search(r"Prerequisites\s+(.*?)\s+Category\b", block, re.S)
        category = re.search(r"Category\s+([^\n]+)", block)
        prereq_txt = clean(prereq.group(1)) if prereq else ""
        if prereq_txt in ("-", "–", "—"):
            prereq_txt = ""
        cat = clean(category.group(1)) if category else ""

        description = _between(block, r"Course Summary:", [r"Learning Outcomes", r"Curriculum Content", r"Textbooks and References"])
        outcomes = _between(block, r"Learning Outcomes:?", [r"Curriculum Content", r"Textbooks and References"])
        topics = _between(block, r"Curriculum Content:", [r"Textbooks and References"])

        full = f"{description} {topics}"
        rows.append(dict(
            course_code=code, course_title=clean(title.group(1)) if title else "",
            school=clean(school[-1]) if school else "", department=dept,
            course_type=TYPE_MAP.get(cat.lower(), cat), credits=int(credits.group(1)) if credits else None,
            ltp=re.sub(r"\s", "", ltp.group(1)).replace("–", "-") if ltp else "",
            prerequisites=prereq_txt, description=description, learning_outcomes=outcomes, topics=topics,
            indexable=bool(len(full.strip()) >= 60 and not PLACEHOLDER.search(full)), source_url=SOURCE_URL))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf"); ap.add_argument("--txt"); ap.add_argument("--out", default=str(DATA / "snu_courses.csv"))
    a = ap.parse_args()
    if a.txt:
        text = Path(a.txt).read_text(encoding="utf-8")
    else:
        pdf = Path(a.pdf) if a.pdf else download_pdf(DATA / "raw" / "cse_prospectus.pdf")
        text = pdf_to_text(pdf)
    Path(DATA / "raw").mkdir(parents=True, exist_ok=True)
    (DATA / "raw" / "cse_prospectus.txt").write_text(text, encoding="utf-8")

    rows = parse_courses(text)
    if not rows:
        sys.exit("No courses found. Open data/raw/cse_prospectus.txt and check that 'Course Code' lines exist.")
    df = pd.DataFrame(rows, columns=COLUMNS)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.out, index=False, encoding="utf-8")

    # ---------------- self-check report
    print(f"\nParsed {len(df)} courses -> {a.out}   (expected about 43 for this PDF)")
    print(df.groupby("course_type").size().to_string(), "\n")
    print(f"indexable (real text to search): {int(df.indexable.sum())} / {len(df)}")
    bad = df[(df.course_title == "") | df.credits.isna() | (df.department == "")]
    if len(bad):
        print("WARNING - missing title/credits/department:", list(bad.course_code))
    thin = df[~df.indexable]
    if len(thin):
        print("Not indexable (placeholder / too little text):", ", ".join(thin.course_code))
    mentioned = set(re.findall(r"\bCSD\d{3}\b", text)) - set(df.course_code)
    if mentioned:
        print("Codes mentioned in the PDF but with no description page:", ", ".join(sorted(mentioned)))


if __name__ == "__main__":
    main()
