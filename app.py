import html as _html
import html as _html
import re

import streamlit as st

from recommender.recommend import recommend_courses


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ElectiveLens",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# HELPERS (presentation only)
# ============================================================

def md(markup: str):
    """Render HTML safely through st.markdown: strips indentation and blank
    lines so Markdown never mistakes the markup for a code block."""
    lines = [ln.strip() for ln in markup.splitlines() if ln.strip()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


def esc(value) -> str:
    return _html.escape(str(value))


def ring(pct: float) -> str:
    pct = max(0.0, min(100.0, pct))
    circ = 2 * 3.14159 * 46
    dash = circ * pct / 100
    return f"""
    <svg viewBox="0 0 120 120" class="ring" role="img" aria-label="{pct:.0f}% match">
        <circle cx="60" cy="60" r="46" class="ring-track"/>
        <circle cx="60" cy="60" r="46" class="ring-fill"
                stroke-dasharray="{dash:.1f} {circ:.1f}"
                transform="rotate(-90 60 60)"/>
        <text x="60" y="58" class="ring-num">{pct:.0f}%</text>
        <text x="60" y="76" class="ring-cap">match</text>
    </svg>
    """


def bar(label: str, value: float, hint: str) -> str:
    width = max(0.0, min(100.0, value * 100))
    return f"""
    <div class="bar">
        <div class="bar-head">
            <span class="bar-label">{label}</span>
            <span class="bar-val">{value:.3f}</span>
        </div>
        <div class="bar-track"><div class="bar-fill" style="width:{width:.1f}%"></div></div>
        <div class="bar-hint">{hint}</div>
    </div>
    """


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:wght@400;500;600;700&display=swap');

    :root {
        --ink: #10302c;
        --ink-2: #1d4a44;
        --page: #fdf2c8;
        --paper: #faf4df;
        --surface: #ffffff;
        --line: #e7dfbf;
        --muted: #5b6f69;
        --amber: #e8a33d;
        --amber-soft: #fcf1d8;
        --mint: #d3eadf;
    }

    /* ---------- BASE ---------- */

    html, body, [class*="css"], .stApp, .stMarkdown, button, input, select, textarea {
        font-family: 'DM Sans', system-ui, sans-serif;
    }

    .stApp { background: var(--page); overflow-x: hidden; }

    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }

    .block-container {
        max-width: 1120px;
        padding-top: 0;
        padding-bottom: 3rem;
    }

    h1, h2, h3, .display { font-family: 'Bricolage Grotesque', 'DM Sans', sans-serif; }

    /* ---------- HERO ---------- */

    .hero {
        position: relative;
        left: 50%;
        width: 100vw;
        margin-left: -50vw;
        overflow: hidden;
        background: var(--ink);
        border-radius: 0 0 40px 40px;
        padding: 4.2rem 0 4rem;
        margin-bottom: 2.8rem;
    }
    .hero-inner {
        position: relative; z-index: 2;
        max-width: 1120px; margin: 0 auto; padding: 0 1.5rem;
    }
    .hero-text { max-width: 600px; }
    .hero-brand {
        display: inline-flex; align-items: center; gap: .55rem;
        color: var(--mint); font-weight: 600; font-size: .95rem;
        margin-bottom: 1.4rem;
    }
    .hero-brand .dot {
        width: 10px; height: 10px; border-radius: 50%;
        background: var(--amber); box-shadow: 0 0 0 4px rgba(232,163,61,.25);
    }
    .hero-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 3.6rem; line-height: 1.02; font-weight: 800;
        color: #fff; letter-spacing: -.035em; margin: 0;
    }
    .hero-sub {
        color: #bcd3cb; font-size: 1.1rem; line-height: 1.6;
        margin: 1.2rem 0 0; max-width: 480px;
    }
    .hero-lens {
        position: absolute; right: 6%; top: 50%;
        transform: translateY(-50%); width: 520px; height: 520px; z-index: 1;
    }
    .hero-lens circle { fill: none; stroke: var(--amber); }

    /* ---------- SECTION HEADINGS ---------- */

    .section-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.9rem; font-weight: 800; letter-spacing: -.025em;
        color: var(--ink); margin: .4rem 0 .2rem;
    }
    .section-subtitle { color: var(--muted); margin-bottom: 1.2rem; font-size: 1rem; }

    /* ---------- FORM PANEL ---------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--surface);
        border: 1px solid var(--line) !important;
        border-radius: 22px;
        padding: 1.2rem 1.3rem .6rem;
        box-shadow: 0 1px 2px rgba(16,48,44,.04);
    }

    label, .stSelectbox label, .stMultiSelect label, .stNumberInput label {
        color: var(--ink) !important; font-weight: 600 !important; font-size: .92rem !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-testid="stNumberInput"] input {
        background: var(--paper) !important;
        border: 1px solid var(--line) !important;
        border-radius: 12px !important;
        min-height: 2.9rem;
    }
    div[data-testid="stNumberInput"] input,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] div[value],
    div[data-baseweb="select"] > div {
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
        font-weight: 500;
    }
    div[data-testid="stNumberInput"] button {
        background: transparent !important; color: var(--ink) !important;
    }
    div[data-testid="stNumberInput"] button svg,
    div[data-baseweb="select"] svg { fill: var(--ink); color: var(--ink); }
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within {
        border-color: var(--ink-2) !important;
        box-shadow: 0 0 0 3px rgba(29,74,68,.15) !important;
    }
    span[data-baseweb="tag"] {
        background: var(--ink) !important; color: #fff !important;
        border-radius: 8px !important; font-weight: 500;
    }
    span[data-baseweb="tag"] span[role="presentation"] svg { fill: #fff; }

    /* ---------- BUTTON ---------- */

    .stButton > button {
        width: 100%; height: 3.5rem; border-radius: 14px; border: none;
        background: var(--ink); color: #fff;
        font-family: 'DM Sans', sans-serif; font-size: 1.05rem; font-weight: 700;
        transition: background .2s ease, transform .15s ease;
    }
    .stButton > button:hover {
        background: var(--ink-2); color: #fff; transform: translateY(-1px);
    }
    .stButton > button:focus-visible { outline: 3px solid var(--amber); outline-offset: 2px; }
    .stButton > button:active { transform: translateY(0); }

    /* ---------- PROFILE CHIPS ---------- */

    .chips { display: flex; flex-wrap: wrap; gap: .45rem; margin: 0 0 1.6rem; }
    .chip {
        background: var(--surface); border: 1px solid var(--line);
        color: var(--ink); border-radius: 999px;
        padding: .3rem .8rem; font-size: .85rem; font-weight: 500;
    }
    .chip.strong { background: var(--amber-soft); border-color: #f0d9a4; }

    /* ---------- COURSE CARD ---------- */

    .card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 1.7rem 1.9rem;
        margin-top: 1.4rem;
        display: grid;
        grid-template-columns: 150px 1fr;
        gap: 1.9rem;
        align-items: start;
    }
    .card.top { border: 2px solid var(--amber); box-shadow: 0 10px 34px rgba(232,163,61,.14); }

    .rank-col { text-align: center; }
    .rank-tag {
        display: inline-block; font-weight: 700; font-size: .82rem;
        color: var(--ink); background: var(--mint);
        border-radius: 999px; padding: .22rem .7rem; margin-bottom: .6rem;
    }
    .card.top .rank-tag { background: var(--amber); }

    .ring { width: 138px; height: 138px; display: block; margin: 0 auto; }
    .ring-track { fill: none; stroke: var(--mint); stroke-width: 10; }
    .ring-fill { fill: none; stroke: var(--ink); stroke-width: 10; stroke-linecap: round; }
    .card.top .ring-fill { stroke: var(--amber); }
    .ring-num {
        font-family: 'Bricolage Grotesque', sans-serif; font-size: 27px; font-weight: 800;
        fill: var(--ink); text-anchor: middle;
    }
    .ring-cap { font-size: 11px; fill: var(--muted); text-anchor: middle; font-weight: 500; }

    .course-code {
        display: inline-block; background: var(--paper); border: 1px solid var(--line);
        color: var(--muted); font-size: .82rem; font-weight: 600;
        border-radius: 8px; padding: .15rem .55rem; margin-bottom: .55rem;
    }
    .course-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.65rem; font-weight: 800; letter-spacing: -.02em;
        line-height: 1.15; color: var(--ink); margin: 0 0 1.2rem;
    }

    .bars { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2rem; margin-bottom: 1.3rem; }
    .bar-head { display: flex; justify-content: space-between; font-size: .88rem; margin-bottom: .35rem; }
    .bar-label { font-weight: 600; color: var(--ink); }
    .bar-val { color: var(--muted); font-variant-numeric: tabular-nums; }
    .bar-track { height: 7px; background: var(--paper); border-radius: 999px; overflow: hidden; }
    .bar-fill { height: 100%; background: var(--ink-2); border-radius: 999px; }
    .bar-hint { color: var(--muted); font-size: .76rem; margin-top: .3rem; }

    .why {
        background: var(--paper); border-radius: 16px; padding: 1rem 1.2rem;
    }
    .why-title { font-weight: 700; color: var(--ink); margin-bottom: .5rem; font-size: .95rem; }
    .why ul { list-style: none; margin: 0; padding: 0; }
    .why li {
        position: relative; padding-left: 1.5rem; margin: .35rem 0;
        color: #2c4540; font-size: .93rem; line-height: 1.5;
    }
    .why li::before {
        content: ""; position: absolute; left: 0; top: .42rem;
        width: .85rem; height: .85rem; border-radius: 50%; background: var(--mint);
        border: 3px solid var(--ink-2); box-sizing: border-box;
    }

    /* ---------- EXPANDERS ---------- */

    div[data-testid="stExpander"] {
        border: 1px solid var(--line); border-radius: 14px;
        background: var(--surface); margin-top: .6rem; overflow: hidden;
    }
    div[data-testid="stExpander"] summary { font-weight: 600; }
    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"],
    div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] *,
    div[data-testid="stExpander"] details > div,
    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] li,
    div[data-testid="stExpander"] span,
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary *,
    div[data-testid="stExpander"] [data-testid="stMetricLabel"] *,
    div[data-testid="stExpander"] [data-testid="stMetricValue"] * { color: var(--ink) !important; }
    div[data-testid="stExpander"] pre, div[data-testid="stExpander"] pre * { color: #e6efe9 !important; }
    div[data-testid="stMetric"] {
        background: var(--paper); border-radius: 12px; padding: .7rem .9rem;
    }

    hr { border-color: transparent !important; margin: .6rem 0 !important; }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center; color: var(--muted); font-size: .88rem;
        margin-top: 3.5rem; padding-top: 1.6rem; border-top: 1px solid var(--line);
    }
    .footer b { color: var(--ink); }

    /* ---------- RESPONSIVE ---------- */

    @media (max-width: 760px) {
        .hero { padding: 2.6rem 0 2.4rem; border-radius: 0 0 28px 28px; }
        .hero-title { font-size: 2.5rem; }
        .hero-lens { opacity: .35; right: -200px; }
        .card { grid-template-columns: 1fr; padding: 1.4rem; }
        .bars { grid-template-columns: 1fr; }
    }

    @media (prefers-reduced-motion: reduce) {
        * { transition: none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

md(
    """
    <div class="hero">
        <svg class="hero-lens" viewBox="0 0 520 520" aria-hidden="true">
            <circle cx="260" cy="260" r="250" stroke-width="1" opacity=".25"/>
            <circle cx="260" cy="260" r="190" stroke-width="1" opacity=".4"/>
            <circle cx="260" cy="260" r="130" stroke-width="1.5" opacity=".6"/>
            <circle cx="260" cy="260" r="70" stroke-width="2" opacity=".85"/>
            <circle cx="260" cy="260" r="12" fill="#e8a33d" stroke="none"/>
        </svg>
        <div class="hero-inner">
            <div class="hero-text">
                <div class="hero-brand"><span class="dot"></span>ElectiveLens</div>
                <h1 class="hero-title">Find the electives that fits you.</h1>
                <p class="hero-sub">
                    Find electives that match your interests, strengths,
                    career goals, and learning preferences.
                </p>
            </div>
        </div>
    </div>
    """
)


# ============================================================
# STUDENT PROFILE
# ============================================================

md(
    """
    <div class="section-title">Build your student profile</div>
    <div class="section-subtitle">
        Tell us a little about yourself so we can find the most relevant electives.
    </div>
    """
)

with st.container(border=True):

    col1, col2 = st.columns(2, gap="large")

    with col1:

        cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=10.0,
            value=8.0,
            step=0.1,
        )

        semester = st.selectbox(
            "Current Semester",
            [
                "1st Semester",
                "2nd Semester",
                "3rd Semester",
                "4th Semester",
                "5th Semester",
                "6th Semester",
                "7th Semester",
                "8th Semester",
            ],
        )

        interests = st.multiselect(
            "Your Interests",
            [
                "Artificial Intelligence",
                "Machine Learning",
                "Data Science",
                "Cyber Security",
                "Cloud Computing",
                "Software Development",
                "Computer Networks",
                "Natural Language Processing",
            ],
        )

    with col2:

        subjects = st.multiselect(
            "Your Strong Subjects",
            [
                "Programming",
                "Mathematics",
                "Statistics",
                "Database",
                "Computer Networks",
                "Algorithms",
                "Operating Systems",
            ],
        )

        career = st.selectbox(
            "Career Goal",
            [
                "Software Developer",
                "Data Scientist / Data Analyst",
                "AI / ML Engineer",
                "Cyber Security",
                "Cloud / DevOps",
                "Higher Studies / Research",
            ],
        )

        difficulty = st.selectbox(
            "Preferred Difficulty",
            [
                "Beginner",
                "Intermediate",
                "Advanced",
            ],
        )


# ============================================================
# RECOMMEND BUTTON
# ============================================================

st.write("")

if st.button(
    "Find my best electives",
    type="primary",
    use_container_width=True,
):

    if not interests and not subjects:

      st.markdown(
    """
    <div style="
        background:#ffe5e5;
        border:1px solid #ffb3b3;
        border-left:5px solid #dc2626;
        color:#b91c1c;
        padding:0.9rem 1rem;
        border-radius:10px;
        font-weight:600;
        margin-top:0.5rem;
    ">
        Please select at least one interest or strong subject
        before generating recommendations.
    </div>
    """,
    unsafe_allow_html=True,
)

    else:

        with st.spinner(
            "Analyzing your profile and ranking electives..."
        ):

            recommendations = recommend_courses(
                interests=interests,
                subjects=subjects,
                career=career,
                difficulty=difficulty,
                top_k=5,
            )

        if recommendations.empty:

            st.error(
                "No suitable elective recommendations were found."
            )

        else:

            # ====================================================
            # RESULTS HEADER
            # ====================================================

            md(
                """
                <div class="section-title" style="margin-top:2.2rem">Your top electives</div>
                <div class="section-subtitle">
                    Ranked using TF-IDF, Cosine Similarity, Jaccard Similarity,
                    and course quality.
                </div>
                """
            )

            chips = "".join(
                f'<span class="chip strong">{esc(i)}</span>' for i in interests
            ) + "".join(
                f'<span class="chip">{esc(s)}</span>' for s in subjects
            ) + (
                f'<span class="chip">{esc(career)}</span>'
                f'<span class="chip">{esc(difficulty)}</span>'
            )
            md(f'<div class="chips">{chips}</div>')

            # ====================================================
            # COURSE RESULTS
            # ====================================================

            for index, course in recommendations.iterrows():

                match_percentage = course["final_score"] * 100

                reasons = course.get("reasons", [])
                reasons_html = "".join(f"<li>{esc(r)}</li>" for r in reasons)
                why_html = (
                    f"""
                    <div class="why">
                        <div class="why-title">Why this course?</div>
                        <ul>{reasons_html}</ul>
                    </div>
                    """
                    if reasons_html
                    else ""
                )

                card_class = "card top" if index == 0 else "card"
                rank_label = "Best match" if index == 0 else f"#{index + 1}"

                md(
                    f"""
                    <div class="{card_class}">
                        <div class="rank-col">
                            <div class="rank-tag">{rank_label}</div>
                            {ring(match_percentage)}
                        </div>
                        <div>
                            <div class="course-code">{esc(course["course_code"])}</div>
                            <div class="course-title">{esc(course["course_title"])}</div>
                            <div class="bars">
                                {bar("Cosine similarity", course["cosine_score"], "Text relevance to your profile")}
                                {bar("Jaccard similarity", course["jaccard_score"], "Keyword overlap")}
                                {bar("Course quality", course["quality_score"], "Quality signal")}
                            </div>
                            {why_html}
                        </div>
                    </div>
                    """
                )

                # ------------------------------------------------
                # DESCRIPTION
                # ------------------------------------------------

                with st.expander("Course description"):

                    description = str(course.get("description", ""))

                    if description:
                        st.write(description)
                    else:
                        st.info("Course description is not available.")

                # ------------------------------------------------
                # TOPICS
                # ------------------------------------------------

                with st.expander("Topics covered"):

                    topics = str(course.get("topics", ""))

                    if topics:
                        st.write(topics)
                    else:
                        st.info("Topic information is not available.")

                # ------------------------------------------------
                # IR DETAILS
                # ------------------------------------------------

                with st.expander("How was this ranked?"):

                    st.write(
                        "ElectiveLens combines multiple "
                        "information-retrieval signals to produce "
                        "the final ranking."
                    )

                    detail1, detail2, detail3 = st.columns(3)

                    with detail1:
                        st.metric("Cosine", f"{course['cosine_score']:.4f}")

                    with detail2:
                        st.metric("Jaccard", f"{course['jaccard_score']:.4f}")

                    with detail3:
                        st.metric("Quality", f"{course['quality_score']:.4f}")

                    st.write("**Final Ranking Formula**")

                    st.code(
                        "Final Score = "
                        "0.60 × Cosine "
                        "+ 0.25 × Jaccard "
                        "+ 0.15 × Quality"
                    )

                st.divider()


# ============================================================
# FOOTER
# ============================================================

md(
    """
    <div class="footer">
        <b>ElectiveLens</b> — personalized elective recommendations
        <br>
        Built on TF-IDF, cosine similarity, Jaccard similarity and quality ranking.
    </div>
    """
)