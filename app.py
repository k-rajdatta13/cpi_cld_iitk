"""
╔══════════════════════════════════════════════════════════════════════╗
║         IIT KANPUR CPI CALCULATOR  —  app.py                        ║
║         Modern, Mobile-Friendly, Analytics-Powered                  ║
╚══════════════════════════════════════════════════════════════════════╝

HOW THIS FILE IS ORGANISED (read this first!):
  SECTION 1  —  Imports
  SECTION 2  —  Page Configuration  (MUST be the very first st.* call)
  SECTION 3  —  Custom CSS / Theming
  SECTION 4  —  Constants  (grade scale, colours)
  SECTION 5  —  Helper Functions  (CPI math + reusable UI blocks)
  SECTION 6  —  Sidebar  (navigation + inputs)
  SECTION 7  —  Hero Banner
  SECTION 8  —  Mode 1: Single-Semester Calculator
  SECTION 9  —  Mode 2: Multi-Semester Overall CPI
  SECTION 10 —  Mode 3: Quick Calculator
  SECTION 11 —  Footer
"""


# ══════════════════════════════════════════════════════════════════
# SECTION 1 — IMPORTS
#
# streamlit : the web-app framework (handles UI, routing, state)
# pandas    : for creating tables/dataframes
# plotly    : for interactive charts and graphs
# ══════════════════════════════════════════════════════════════════
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ══════════════════════════════════════════════════════════════════
# SECTION 2 — PAGE CONFIGURATION
#
# This MUST come before any other st.* call in the file.
# It sets the browser tab title, icon, and default layout.
# layout="wide"  → use the full browser width (better on desktop)
# ══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="IITK CPI Calculator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ══════════════════════════════════════════════════════════════════
# SECTION 3 — CUSTOM CSS / THEMING
#
# Streamlit lets us inject raw CSS with st.markdown(..., unsafe_allow_html=True).
# Everything visual — colours, fonts, card styles, animations, mobile
# breakpoints — lives here in one place so it's easy to change.
#
# Design Language:
#   • Deep navy background  (#0b1728)   — calm, academic, premium
#   • Gold accent           (#e8a020)   — IIT prestige / excellence
#   • Teal highlight        (#2dd4bf)   — data / analytics feel
#   • Fonts: Playfair Display (headings) + Outfit (body)
#   • Glassmorphism cards with subtle blur + gold border
# ══════════════════════════════════════════════════════════════════
CUSTOM_CSS = """
<style>

/* ── Google Fonts ─────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Outfit:wght@300;400;500;600;700&display=swap');

/* ── Design Tokens (change these to retheme everything) ───────── */
:root {
    --navy      : #0b1728;
    --navy2     : #122040;
    --navy3     : #1b2f52;
    --gold      : #e8a020;
    --gold2     : #f5c842;
    --teal      : #2dd4bf;
    --rose      : #f87171;
    --green     : #4ade80;
    --amber     : #fbbf24;
    --text      : #e8edf5;
    --muted     : #8fa3c0;
    --card-bg   : rgba(27, 47, 82, 0.55);
    --border    : rgba(232, 160, 32, 0.22);
    --radius    : 16px;
    --shadow    : 0 8px 32px rgba(0, 0, 0, 0.40);
}

/* ── Reset & Base ─────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family : 'Outfit', sans-serif !important;
    background  : var(--navy) !important;
    color       : var(--text) !important;
}

/* Remove default Streamlit top-padding and cap max width */
.block-container {
    padding-top    : 1.25rem !important;
    padding-bottom : 2.5rem  !important;
    max-width      : 1200px  !important;
}

/* ── Sidebar ──────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background  : linear-gradient(160deg, var(--navy2) 0%, var(--navy3) 100%) !important;
    border-right: 1px solid var(--border) !important;
}
/* Sidebar label text */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio > label {
    color          : var(--muted)   !important;
    font-size      : 0.75rem        !important;
    font-weight    : 700            !important;
    letter-spacing : 0.09em         !important;
    text-transform : uppercase      !important;
}

/* ── Hero Banner ──────────────────────────────────────────────── */
.hero-banner {
    background    : linear-gradient(135deg, #0e1e38 0%, #122040 55%, #1a3060 100%);
    border        : 1px solid var(--border);
    border-radius : var(--radius);
    padding       : 2rem 2.5rem;
    margin-bottom : 1.5rem;
    position      : relative;
    overflow      : hidden;
    box-shadow    : var(--shadow);
    animation     : fadeUp 0.6s ease both;
}
/* Decorative glow blobs */
.hero-banner::before {
    content       : '';
    position      : absolute;
    top : -70px; right : -70px;
    width : 240px; height : 240px;
    background    : radial-gradient(circle, rgba(232,160,32,.2) 0%, transparent 70%);
    border-radius : 50%;
}
.hero-banner::after {
    content       : '';
    position      : absolute;
    bottom : -50px; left : 35%;
    width : 160px; height : 160px;
    background    : radial-gradient(circle, rgba(45,212,191,.12) 0%, transparent 70%);
    border-radius : 50%;
}
.hero-title {
    font-family    : 'Playfair Display', serif !important;
    font-size      : clamp(1.7rem, 4vw, 2.6rem) !important;
    font-weight    : 700 !important;
    background     : linear-gradient(90deg, var(--gold), var(--gold2), var(--teal));
    -webkit-background-clip : text   !important;
    -webkit-text-fill-color : transparent !important;
    background-clip: text !important;
    margin         : 0 0 0.3rem 0   !important;
    line-height    : 1.2            !important;
    position       : relative; z-index: 1;
}
.hero-sub {
    color     : var(--muted) !important;
    font-size : 0.92rem      !important;
    margin    : 0            !important;
    position  : relative; z-index: 1;
}

/* ── Section Headers ──────────────────────────────────────────── */
.sec-head {
    font-family    : 'Playfair Display', serif;
    font-size      : 1.25rem;
    color          : var(--gold);
    margin         : 1.5rem 0 1rem;
    display        : flex;
    align-items    : center;
    gap            : 0.5rem;
}
.sec-head::after {
    content    : '';
    flex       : 1;
    height     : 1px;
    background : linear-gradient(90deg, var(--border), transparent);
    margin-left: 0.6rem;
}

/* ── Glassmorphism Metric Card ────────────────────────────────── */
.metric-card {
    background    : var(--card-bg);
    border        : 1px solid var(--border);
    border-radius : 12px;
    padding       : 1rem 1.2rem;
    text-align    : center;
    backdrop-filter: blur(10px);
    box-shadow    : var(--shadow);
    transition    : transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover { transform: translateY(-3px); box-shadow: 0 14px 40px rgba(0,0,0,.5); }
.metric-card .lbl  { font-size: 0.68rem; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin-bottom: .35rem; }
.metric-card .val  { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: var(--gold2); line-height: 1; }

/* ── Result Banner (appears after Calculate) ──────────────────── */
.result-banner {
    border-radius : var(--radius);
    padding       : 1.5rem;
    margin        : 0.8rem 0;
    text-align    : center;
    border        : 1px solid;
    animation     : fadeUp 0.45s ease both;
}
.result-banner.outstanding { background: rgba(232,160,32,.12); border-color: var(--gold); }
.result-banner.excellent   { background: rgba(74,222,128,.10); border-color: var(--green); }
.result-banner.good        { background: rgba(45,212,191,.10); border-color: var(--teal); }
.result-banner.average     { background: rgba(251,191,36,.10); border-color: var(--amber); }
.result-banner.low         { background: rgba(248,113,113,.10); border-color: var(--rose); }

.result-banner .cpi-num {
    font-family : 'Playfair Display', serif;
    font-size   : 3.4rem;
    font-weight : 700;
    line-height : 1;
}
.result-banner.outstanding .cpi-num { color: var(--gold2); }
.result-banner.excellent   .cpi-num { color: var(--green); }
.result-banner.good        .cpi-num { color: var(--teal);  }
.result-banner.average     .cpi-num { color: var(--amber); }
.result-banner.low         .cpi-num { color: var(--rose);  }

.result-banner .cpi-lbl { font-size:.72rem; color:var(--muted); letter-spacing:.1em; text-transform:uppercase; }
.result-banner .cpi-msg { font-size:1.05rem; margin-top:.5rem; font-weight:500; }

/* ── CPI Progress Bar ─────────────────────────────────────────── */
.prog-wrap { background:rgba(255,255,255,.07); border-radius:20px; height:9px; margin:.6rem auto .3rem; max-width:220px; overflow:hidden; }
.prog-bar  { height:100%; border-radius:20px; background:linear-gradient(90deg,var(--gold),var(--gold2)); transition:width .8s ease; }

/* ── Info Box ─────────────────────────────────────────────────── */
.info-box {
    background : rgba(45,212,191,.08);
    border     : 1px solid rgba(45,212,191,.3);
    border-radius: 10px;
    padding    : .65rem 1rem;
    font-size  : .86rem;
    color      : var(--teal);
    margin     : .4rem 0 .8rem;
}

/* ── Grade Scale Card ─────────────────────────────────────────── */
.grade-scale-wrap {
    background    : var(--card-bg);
    border        : 1px solid var(--border);
    border-radius : 12px;
    overflow      : hidden;
    margin-top    : .5rem;
}
.grade-scale-head {
    background : rgba(232,160,32,.1);
    padding    : .55rem 1rem;
    font-size  : .68rem;
    font-weight: 700;
    letter-spacing:.1em;
    text-transform: uppercase;
    color      : var(--muted);
}
.grade-table { width:100%; border-collapse:collapse; }
.grade-table th { padding:.35rem .8rem; font-size:.67rem; letter-spacing:.1em; text-transform:uppercase; color:var(--muted); text-align:center; }
.grade-table td { padding:.28rem .8rem; text-align:center; }

/* Grade Badges */
.gb { display:inline-block; padding:.12rem .55rem; border-radius:20px; font-size:.72rem; font-weight:700; letter-spacing:.05em; }
.gb-A  { background:rgba(74,222,128,.18);  color:var(--green);  border:1px solid var(--green); }
.gb-B  { background:rgba(45,212,191,.18);  color:var(--teal);   border:1px solid var(--teal);  }
.gb-C  { background:rgba(251,191,36,.18);  color:var(--amber);  border:1px solid var(--amber); }
.gb-D  { background:rgba(248,113,113,.18); color:var(--rose);   border:1px solid var(--rose);  }

/* ── Input Styling ────────────────────────────────────────────── */
.stTextInput input, .stNumberInput input {
    background : rgba(255,255,255,.06) !important;
    border     : 1px solid rgba(255,255,255,.12) !important;
    color      : var(--text) !important;
    border-radius: 8px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--gold) !important;
    box-shadow  : 0 0 0 2px rgba(232,160,32,.2) !important;
}
.stSelectbox > div > div {
    background  : rgba(255,255,255,.06) !important;
    border      : 1px solid rgba(255,255,255,.12) !important;
    border-radius: 8px !important;
}

/* ── Buttons ──────────────────────────────────────────────────── */
.stButton > button {
    background    : linear-gradient(135deg, var(--gold) 0%, #c97a10 100%) !important;
    color         : #0b1728 !important;
    font-weight   : 700 !important;
    font-family   : 'Outfit', sans-serif !important;
    border        : none !important;
    border-radius : 10px !important;
    padding       : .6rem 1.5rem !important;
    letter-spacing: .04em !important;
    box-shadow    : 0 4px 15px rgba(232,160,32,.35) !important;
    transition    : all .2s ease !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 22px rgba(232,160,32,.55) !important; }

/* ── Dataframe ────────────────────────────────────────────────── */
[data-testid="stDataFrame"] { border:1px solid var(--border) !important; border-radius:10px !important; overflow:hidden !important; }

/* ── Footer ───────────────────────────────────────────────────── */
.footer {
    text-align   : center;
    padding      : 2rem 0 1rem;
    color        : var(--muted);
    font-size    : .78rem;
    border-top   : 1px solid var(--border);
    margin-top   : 2.5rem;
    line-height  : 2;
}

/* ── Animations ───────────────────────────────────────────────── */
@keyframes fadeUp {
    from { opacity:0; transform:translateY(18px); }
    to   { opacity:1; transform:translateY(0); }
}

/* ── Mobile ───────────────────────────────────────────────────── */
@media (max-width: 768px) {
    .block-container     { padding: .5rem !important; }
    .hero-banner         { padding: 1.2rem !important; }
    .hero-title          { font-size: 1.55rem !important; }
    .metric-card .val    { font-size: 1.6rem !important; }
    .result-banner .cpi-num { font-size: 2.4rem !important; }
    .sec-head            { font-size: 1.05rem; }
}

/* Hide Streamlit default branding */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 4 — CONSTANTS
#
# GRADE_POINTS : Official IITK grade → numeric point mapping
#   A+ and A both map to 10 (IITK policy)
# GRADE_COLORS : Colour for each grade (used in charts)
# ══════════════════════════════════════════════════════════════════
GRADE_POINTS = {
    "A+": 10, "A": 10,
    "B+": 9,  "B": 8,
    "C+": 7,  "C": 6,
    "D+": 5,  "D": 4,
}

GRADE_COLORS = {
    "A+": "#4ade80", "A": "#4ade80",
    "B+": "#2dd4bf", "B": "#2dd4bf",
    "C+": "#fbbf24", "C": "#fbbf24",
    "D+": "#f87171", "D": "#f87171",
}

CHART_STYLE = dict(
    paper_bgcolor = "rgba(0,0,0,0)",
    plot_bgcolor  = "rgba(0,0,0,0)",
    font          = dict(color="#8fa3c0", family="Outfit", size=12),
    margin        = dict(t=50, b=20, l=10, r=10),
    xaxis         = dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True),
    yaxis         = dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True),
)


# ══════════════════════════════════════════════════════════════════
# SECTION 5 — HELPER FUNCTIONS
#
# Keeping calculation logic and reusable UI blocks here makes
# the main calculator sections below much cleaner to read.
# ══════════════════════════════════════════════════════════════════

def calc_cpi(grades: list, credits: list):
    """
    Core CPI formula:
        CPI = Σ(grade_point × credits) / Σ(credits)

    Returns: (cpi_float, total_grade_points, total_credits)
    """
    total_pts = sum(GRADE_POINTS[g] * c for g, c in zip(grades, credits))
    total_crd = sum(credits)
    cpi = total_pts / total_crd if total_crd > 0 else 0.0
    return cpi, total_pts, total_crd


def cpi_category(cpi: float):
    """
    Returns (css_class, emoji_message, accent_colour) based on CPI range.
    Used to pick the right style for the result banner.
    """
    if cpi >= 9.0: return "outstanding", "🏆 Outstanding Performance!",  "#f5c842"
    if cpi >= 8.0: return "excellent",   "🎉 Excellent Performance!",    "#4ade80"
    if cpi >= 7.0: return "good",        "👍 Good Performance!",          "#2dd4bf"
    if cpi >= 6.0: return "average",     "📈 Keep Improving!",            "#fbbf24"
    return             "low",        "📚 More Effort Needed!",       "#f87171"


def render_result_banner(cpi: float):
    """
    Renders the big animated CPI result card with colour,
    progress bar, and motivational message.
    """
    cls, msg, _ = cpi_category(cpi)
    pct = cpi / 10 * 100
    st.markdown(f"""
    <div class="result-banner {cls}">
        <div class="cpi-lbl">Cumulative Performance Index</div>
        <div class="cpi-num">{cpi:.2f}</div>
        <div class="prog-wrap">
            <div class="prog-bar" style="width:{pct:.1f}%"></div>
        </div>
        <div style="font-size:.72rem;color:#8fa3c0;margin-bottom:.3rem;">{pct:.1f} / 100</div>
        <div class="cpi-msg">{msg}</div>
    </div>
    """, unsafe_allow_html=True)
    if cpi >= 9.0:
        st.balloons()


def render_grade_scale():
    """Renders a styled grade-scale reference card (shown in right column)."""
    badge_class = {"A+":"gb-A","A":"gb-A","B+":"gb-B","B":"gb-B",
                   "C+":"gb-C","C":"gb-C","D+":"gb-D","D":"gb-D"}
    rows_html = "".join(
        f'<tr>'
        f'<td><span class="gb {badge_class[g]}">{g}</span></td>'
        f'<td style="font-family:\'Playfair Display\',serif;font-size:1.05rem;color:#f5c842;">{p}</td>'
        f'</tr>'
        for g, p in GRADE_POINTS.items()
    )
    st.markdown(f"""
    <div class="grade-scale-wrap">
        <div class="grade-scale-head">📐 IITK Grade Scale</div>
        <table class="grade-table">
            <thead><tr>
                <th>Grade</th><th>Points</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)


def render_metric_pair(label1, val1, label2, val2):
    """Renders two metric cards side-by-side."""
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="lbl">{label1}</div>'
                    f'<div class="val">{val1}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="lbl">{label2}</div>'
                    f'<div class="val">{val2}</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 6 — SIDEBAR
#
# The sidebar is always visible (it collapses on mobile but is
# accessible via the ☰ button).
# It controls:
#   • Which calculator mode to show
#   • Number of courses / semesters / subjects
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo block
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 .5rem;">
        <div style="font-size:2.8rem;margin-bottom:.25rem;">🎓</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.1rem;
                    color:#e8a020;font-weight:700;letter-spacing:.03em;">IITK CPI</div>
        <div style="font-size:.67rem;color:#8fa3c0;letter-spacing:.12em;
                    text-transform:uppercase;">Calculator</div>
    </div>
    <hr style="border-color:rgba(232,160,32,.2);margin:.6rem 0;">
    """, unsafe_allow_html=True)

    calc_mode = st.radio(
        "MODE",
        ["📘 Single Semester", "📊 Multi-Semester CPI", "⚡ Quick Calculator"],
        index=0,
    )

    st.markdown('<hr style="border-color:rgba(232,160,32,.2);margin:.6rem 0;">', unsafe_allow_html=True)

    # Show different number-inputs depending on mode
    if calc_mode == "📘 Single Semester":
        semester_num = st.selectbox(
            "SEMESTER",
            options=list(range(1, 9)),
            format_func=lambda x: f"Semester {x}",
        )
        num_courses = st.number_input("NUMBER OF COURSES", 1, 15, 5, 1)

    elif calc_mode == "📊 Multi-Semester CPI":
        num_semesters = st.number_input("NUMBER OF SEMESTERS", 1, 8, 3, 1)

    else:  # Quick
        num_subjects = st.number_input("NUMBER OF SUBJECTS", 1, 20, 5, 1)

    # Formula reminder in sidebar
    st.markdown("""
    <div style="margin-top:1.5rem;padding:.7rem .9rem;
                background:rgba(232,160,32,.07);
                border-radius:10px;border:1px solid rgba(232,160,32,.2);">
        <div style="font-size:.67rem;color:#8fa3c0;text-transform:uppercase;
                    letter-spacing:.09em;margin-bottom:.35rem;">📐 Formula</div>
        <div style="font-size:.8rem;color:#e8edf5;line-height:1.7;">
            CPI = Σ(Grade × Credits)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;────────────────<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Σ Credits
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 7 — HERO BANNER
#
# Displayed at the top of every page, regardless of mode.
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🎓 IIT Kanpur CPI Calculator</div>
    <p class="hero-sub">
        Track academic performance &nbsp;·&nbsp; Visualise trends
        &nbsp;·&nbsp; Plan your semester
    </p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 8 — MODE 1: SINGLE SEMESTER CALCULATOR
#
# User enters: course name, credits, grade  for each course.
# Output: CPI for that semester + bar chart + pie chart + table.
# ══════════════════════════════════════════════════════════════════
if calc_mode == "📘 Single Semester":

    st.markdown(
        f'<div class="sec-head">📘 Semester {semester_num} — Course Details</div>',
        unsafe_allow_html=True,
    )

    # ── Session State ──────────────────────────────────────────
    # Streamlit re-runs the whole script on every interaction.
    # st.session_state persists data across those re-runs so that
    # entered grades/credits are not lost when you change a field.
    if "courses" not in st.session_state:
        st.session_state.courses = []

    # Keep the list exactly as long as num_courses
    while len(st.session_state.courses) < num_courses:
        st.session_state.courses.append({"name": "", "credit": 9, "grade": "A"})
    while len(st.session_state.courses) > num_courses:
        st.session_state.courses.pop()

    # ── Layout: Left (inputs) | Right (grade scale + result) ──
    left_col, right_col = st.columns([3, 2], gap="large")

    with left_col:
        st.markdown(
            '<div class="info-box">💡 Fill in course name, credits & grade. '
            'Course name is optional for calculation.</div>',
            unsafe_allow_html=True,
        )

        for i in range(num_courses):
            st.markdown(
                f'<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:.09em;color:#8fa3c0;margin:.55rem 0 .15rem;">'
                f'Course {i + 1}</div>',
                unsafe_allow_html=True,
            )
            c_name, c_cred, c_grade = st.columns([3, 1, 1])

            with c_name:
                name = st.text_input(
                    "Course Name", value=st.session_state.courses[i]["name"],
                    key=f"name_{i}", placeholder="e.g. Mathematics-I",
                    label_visibility="collapsed",
                )
                st.session_state.courses[i]["name"] = name

            with c_cred:
                cred = st.number_input(
                    "Credits", 1, 10, st.session_state.courses[i]["credit"],
                    key=f"cred_{i}", label_visibility="collapsed",
                )
                st.session_state.courses[i]["credit"] = cred

            with c_grade:
                grade = st.selectbox(
                    "Grade",
                    list(GRADE_POINTS.keys()),
                    index=list(GRADE_POINTS.keys()).index(st.session_state.courses[i]["grade"]),
                    key=f"grade_{i}", label_visibility="collapsed",
                )
                st.session_state.courses[i]["grade"] = grade

        # Calculate button
        if st.button("🧮  Calculate CPI", use_container_width=True, type="primary"):
            named = [c for c in st.session_state.courses if c["name"].strip()]
            all_c = st.session_state.courses  # include unnamed too in quick mode

            # Use named courses if any; otherwise use all
            working = named if named else st.session_state.courses
            cpi, tp, tc = calc_cpi(
                [c["grade"] for c in working],
                [c["credit"] for c in working],
            )
            st.session_state.single_result = (cpi, tp, tc, working)

    with right_col:
        render_grade_scale()

        if "single_result" in st.session_state:
            cpi, tp, tc, working = st.session_state.single_result
            st.markdown("<br>", unsafe_allow_html=True)
            render_result_banner(cpi)
            render_metric_pair("Total Credits", tc, "Grade Points", tp)

    # ── Charts (shown below once result is available) ──────────
    if "single_result" in st.session_state:
        cpi, tp, tc, working = st.session_state.single_result

        st.markdown('<div class="sec-head">📊 Analytics</div>', unsafe_allow_html=True)

        chart_left, chart_right = st.columns(2, gap="medium")

        with chart_left:
            # Bar chart: weighted grade points per course
            labels = [c["name"] or f"Course {i+1}" for i, c in enumerate(working)]
            wt_pts = [GRADE_POINTS[c["grade"]] * c["credit"] for c in working]
            colors = [GRADE_COLORS[c["grade"]] for c in working]

            fig_bar = go.Figure(go.Bar(
                x=labels, y=wt_pts,
                marker=dict(color=colors, line=dict(width=0)),
                text=wt_pts, textposition="outside",
                textfont=dict(color="#e8edf5"),
            ))
            fig_bar.update_layout(
                title="Weighted Grade Points per Course",
                **CHART_STYLE,
                yaxis=dict(**CHART_STYLE["yaxis"], title="Points"),
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with chart_right:
            # Donut chart: credit share per course
            fig_pie = go.Figure(go.Pie(
                labels=labels,
                values=[c["credit"] for c in working],
                hole=0.52,
                marker=dict(colors=[
                    "#e8a020","#2dd4bf","#4ade80","#f87171",
                    "#a78bfa","#fb923c","#38bdf8","#f472b6"
                ]),
                textfont=dict(color="white", size=11),
            ))
            fig_pie.update_layout(
                title="Credit Distribution",
                **CHART_STYLE,
                legend=dict(font=dict(size=10, color="#8fa3c0")),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # Detailed table (inside an expander to save space)
        with st.expander("📋 Full Breakdown Table + Formula"):
            rows = [
                {
                    "Course": c["name"] or f"Course {i+1}",
                    "Credits": c["credit"],
                    "Grade": c["grade"],
                    "Grade Points": GRADE_POINTS[c["grade"]],
                    "Weighted Points": GRADE_POINTS[c["grade"]] * c["credit"],
                }
                for i, c in enumerate(working)
            ]
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
            st.latex(
                r"CPI = \frac{\sum(Grade\_Pts \times Credits)}{\sum Credits}"
                r" = \frac{" + str(tp) + r"}{" + str(tc) + r"} = " + f"{cpi:.2f}"
            )


# ══════════════════════════════════════════════════════════════════
# SECTION 9 — MODE 2: MULTI-SEMESTER OVERALL CPI
#
# User enters: semester name, SPI (that semester's CPI), credits.
# Output:
#   • Overall weighted CPI across all semesters
#   • Combined bar + line chart (SPI bars + cumulative CPI line)
#   • Credits-by-semester chart coloured by SPI
#   • Comparison table showing cumulative CPI after each semester
# ══════════════════════════════════════════════════════════════════
elif calc_mode == "📊 Multi-Semester CPI":

    st.markdown(
        '<div class="sec-head">📊 Multi-Semester Overall CPI</div>',
        unsafe_allow_html=True,
    )

    if "semesters" not in st.session_state:
        st.session_state.semesters = []

    while len(st.session_state.semesters) < num_semesters:
        n = len(st.session_state.semesters) + 1
        st.session_state.semesters.append(
            {"name": f"Semester {n}", "spi": 8.0, "credits": 36}
        )
    while len(st.session_state.semesters) > num_semesters:
        st.session_state.semesters.pop()

    left_col, right_col = st.columns([3, 2], gap="large")

    with left_col:
        st.markdown(
            '<div class="info-box">💡 Enter the <b>SPI</b> (your grade for that semester, '
            'sometimes shown on your grade card as "SGPA") and total credits for each semester.</div>',
            unsafe_allow_html=True,
        )

        for i in range(num_semesters):
            st.markdown(
                f'<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:.09em;color:#8fa3c0;margin:.55rem 0 .15rem;">'
                f'{st.session_state.semesters[i]["name"]}</div>',
                unsafe_allow_html=True,
            )
            c_nm, c_spi, c_cr = st.columns([3, 1, 1])

            with c_nm:
                sn = st.text_input(
                    "Name", value=st.session_state.semesters[i]["name"],
                    key=f"sn_{i}", placeholder=f"Semester {i+1}",
                    label_visibility="collapsed",
                )
                st.session_state.semesters[i]["name"] = sn

            with c_spi:
                spi = st.number_input(
                    "SPI", 0.0, 10.0, float(st.session_state.semesters[i]["spi"]),
                    step=0.01, format="%.2f", key=f"spi_{i}",
                    label_visibility="collapsed",
                )
                st.session_state.semesters[i]["spi"] = spi

            with c_cr:
                scr = st.number_input(
                    "Credits", 1, 60, st.session_state.semesters[i]["credits"],
                    key=f"scr_{i}", label_visibility="collapsed",
                )
                st.session_state.semesters[i]["credits"] = scr

        if st.button("🧮  Calculate Overall CPI", use_container_width=True, type="primary"):
            valid = [s for s in st.session_state.semesters if s["spi"] > 0]
            if not valid:
                st.error("Please enter a valid SPI (> 0) for at least one semester.")
            else:
                tw = sum(s["spi"] * s["credits"] for s in valid)
                tc = sum(s["credits"] for s in valid)
                overall = tw / tc
                st.session_state.multi_result = (overall, tw, tc, valid)

    with right_col:
        render_grade_scale()

        if "multi_result" in st.session_state:
            overall, tw, tc, valid = st.session_state.multi_result
            st.markdown("<br>", unsafe_allow_html=True)
            render_result_banner(overall)
            render_metric_pair("Total Credits", tc, "Semesters", len(valid))

    # ── Charts ──────────────────────────────────────────────────
    if "multi_result" in st.session_state:
        overall, tw, tc, valid = st.session_state.multi_result
        names  = [s["name"]    for s in valid]
        spis   = [s["spi"]     for s in valid]
        creds  = [s["credits"] for s in valid]

        # Compute cumulative CPI after each semester
        cum_tw_run, cum_tc_run, cumulative_cpis = 0.0, 0.0, []
        for s in valid:
            cum_tw_run += s["spi"] * s["credits"]
            cum_tc_run += s["credits"]
            cumulative_cpis.append(round(cum_tw_run / cum_tc_run, 3))

        st.markdown('<div class="sec-head">📈 Trend & Comparison Analytics</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="medium")

        with c1:
            # Combined chart: bars for SPI + line for cumulative CPI
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Bar(
                x=names, y=spis, name="Semester SPI",
                marker_color="#e8a020", opacity=0.72,
            ))
            fig_trend.add_trace(go.Scatter(
                x=names, y=cumulative_cpis, name="Cumulative CPI",
                mode="lines+markers",
                line=dict(color="#2dd4bf", width=2.5),
                marker=dict(size=9, color="#2dd4bf"),
            ))
            fig_trend.add_hline(
                y=overall, line_dash="dot", line_color="#4ade80",
                annotation_text=f"Overall: {overall:.2f}",
                annotation_font=dict(color="#4ade80"),
            )
            fig_trend.update_layout(
                title="SPI per Semester & Cumulative CPI Trend",
                **CHART_STYLE,
                yaxis=dict(**CHART_STYLE["yaxis"], range=[0, 10.5]),
                legend=dict(font=dict(size=11, color="#8fa3c0"),
                            bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_trend, use_container_width=True)

        with c2:
            # Credits bar coloured by SPI using a colour scale
            fig_cred = go.Figure(go.Bar(
                x=names, y=creds,
                marker=dict(
                    color=spis,
                    colorscale=[
                        [0.0, "#f87171"],
                        [0.4, "#fbbf24"],
                        [0.7, "#2dd4bf"],
                        [1.0, "#4ade80"],
                    ],
                    cmin=4, cmax=10,
                    showscale=True,
                    colorbar=dict(
                        title="SPI",
                        tickfont=dict(color="#8fa3c0"),
                        titlefont=dict(color="#8fa3c0"),
                    ),
                ),
            ))
            fig_cred.update_layout(
                title="Credits per Semester (colour = SPI)",
                **CHART_STYLE,
                yaxis=dict(**CHART_STYLE["yaxis"], title="Credits"),
            )
            st.plotly_chart(fig_cred, use_container_width=True)

        # Semester comparison table with running cumulative CPI
        with st.expander("📋 Semester Comparison Table"):
            rows = []
            cw, cc = 0.0, 0.0
            for s in valid:
                cw += s["spi"] * s["credits"]
                cc += s["credits"]
                rows.append({
                    "Semester":       s["name"],
                    "SPI":            f"{s['spi']:.2f}",
                    "Credits":        s["credits"],
                    "Weighted SPI":   f"{s['spi'] * s['credits']:.2f}",
                    "Cumulative CPI": f"{cw / cc:.2f}",
                })
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
            st.latex(
                r"\text{Overall CPI} = \frac{\sum (SPI_i \times Credits_i)}{\sum Credits_i}"
                r" = \frac{" + f"{tw:.2f}" + r"}{" + str(tc) + r"} = " + f"{overall:.2f}"
            )


# ══════════════════════════════════════════════════════════════════
# SECTION 10 — MODE 3: QUICK CALCULATOR
#
# Fastest entry: just select credits + grade, no course names.
# Output: CPI + grade distribution bar chart.
# ══════════════════════════════════════════════════════════════════
else:
    st.markdown(
        '<div class="sec-head">⚡ Quick CPI Calculator</div>',
        unsafe_allow_html=True,
    )

    if "quick" not in st.session_state:
        st.session_state.quick = []

    while len(st.session_state.quick) < num_subjects:
        st.session_state.quick.append({"credit": 9, "grade": "A"})
    while len(st.session_state.quick) > num_subjects:
        st.session_state.quick.pop()

    left_col, right_col = st.columns([3, 2], gap="large")

    with left_col:
        st.markdown(
            '<div class="info-box">⚡ No course names needed — just credits & grades!</div>',
            unsafe_allow_html=True,
        )

        for i in range(num_subjects):
            st.markdown(
                f'<div style="font-size:.72rem;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:.09em;color:#8fa3c0;margin:.55rem 0 .15rem;">'
                f'Subject {i + 1}</div>',
                unsafe_allow_html=True,
            )
            c_cred, c_grade = st.columns(2)

            with c_cred:
                cred = st.number_input(
                    "Credits", 1, 10, st.session_state.quick[i]["credit"],
                    key=f"qcr_{i}", label_visibility="collapsed",
                )
                st.session_state.quick[i]["credit"] = cred

            with c_grade:
                grade = st.selectbox(
                    "Grade",
                    list(GRADE_POINTS.keys()),
                    index=list(GRADE_POINTS.keys()).index(st.session_state.quick[i]["grade"]),
                    key=f"qgr_{i}", label_visibility="collapsed",
                )
                st.session_state.quick[i]["grade"] = grade

        if st.button("⚡  Calculate CPI", use_container_width=True, type="primary"):
            cpi, tp, tc = calc_cpi(
                [s["grade"]  for s in st.session_state.quick],
                [s["credit"] for s in st.session_state.quick],
            )
            st.session_state.quick_result = (cpi, tp, tc)

    with right_col:
        render_grade_scale()

        if "quick_result" in st.session_state:
            cpi, tp, tc = st.session_state.quick_result
            st.markdown("<br>", unsafe_allow_html=True)
            render_result_banner(cpi)
            render_metric_pair("Total Credits", tc, "Grade Points", tp)

    # ── Grade distribution chart ────────────────────────────────
    if "quick_result" in st.session_state:
        cpi, tp, tc = st.session_state.quick_result

        st.markdown('<div class="sec-head">📊 Grade Distribution</div>', unsafe_allow_html=True)

        # Tally up credits by grade
        dist: dict = {}
        for s in st.session_state.quick:
            dist[s["grade"]] = dist.get(s["grade"], 0) + s["credit"]

        # Maintain official grade order
        ordered_grades = [g for g in GRADE_POINTS if g in dist]

        fig_dist = go.Figure(go.Bar(
            x=ordered_grades,
            y=[dist[g] for g in ordered_grades],
            marker=dict(
                color=[GRADE_COLORS[g] for g in ordered_grades],
                line=dict(width=0),
            ),
            text=[dist[g] for g in ordered_grades],
            textposition="outside",
            textfont=dict(color="#e8edf5"),
        ))
        fig_dist.update_layout(
            title="Credits by Grade",
            **CHART_STYLE,
            yaxis=dict(**CHART_STYLE["yaxis"], title="Credits"),
        )
        st.plotly_chart(fig_dist, use_container_width=True)

        # Quick breakdown table
        with st.expander("📋 Breakdown Table"):
            rows = [
                {
                    "Subject":        f"Subject {i + 1}",
                    "Credits":        s["credit"],
                    "Grade":          s["grade"],
                    "Grade Points":   GRADE_POINTS[s["grade"]],
                    "Weighted Points": GRADE_POINTS[s["grade"]] * s["credit"],
                }
                for i, s in enumerate(st.session_state.quick)
            ]
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
            st.latex(
                r"CPI = \frac{" + str(tp) + r"}{" + str(tc) + r"} = " + f"{cpi:.2f}"
            )


# ══════════════════════════════════════════════════════════════════
# SECTION 11 — FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    🏛️ IIT Kanpur CPI Calculator &nbsp;·&nbsp; Built with ❤️ using Streamlit
    <br>
    <span style="font-size:.7rem;">
        A+/A = 10 &nbsp;·&nbsp; B+ = 9 &nbsp;·&nbsp; B = 8 &nbsp;·&nbsp;
        C+ = 7 &nbsp;·&nbsp; C = 6 &nbsp;·&nbsp; D+ = 5 &nbsp;·&nbsp; D = 4
        &nbsp;·&nbsp; Follows official IITK grading system
    </span>
</div>
""", unsafe_allow_html=True)
