"""
Isolation Forest: course project website.
Run locally with:  streamlit run app.py
"""
import html
import re
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

import demo
from content import DEMO_INTRO, DEMO_TITLE, REFERENCES, SECTIONS

# Edit these placeholders before presenting.
PROJECT_INFO = {
    "course": "Design and Analysis of Algorithms",
    "university": "Najran University",
    "university_ar": "جامعة نجران",
    "instructor": "[Instructor Name]",
    "members": [  # (English name, Arabic name)
        ("Rayan Alahmari", "ريان الأحمري"),
        ("Saeed Al Sulaim", "سعيد آل سليم"),
        ("Fares Salem", "فارس سالم"),
        ("Khalid Yahya", "خالد يحيى"),
    ],
}

ASSETS = Path(__file__).parent / "assets"

IVORY, PALE, GOLD, GRAY, CHAR, RUST = "#F7F4EB", "#E9D99B", "#D6B75C", "#77766E", "#292923", "#A65A3A"

st.set_page_config(page_title="Isolation Forest", page_icon="❄", layout="centered")

# ------------------------------------------------------------------ style
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@500;600&family=Source+Sans+3:wght@400;600&display=swap');

html, body, [class*="css"], .stMarkdown, p, li, td, th { font-family: 'Source Sans 3', 'Segoe UI', sans-serif; }
.stMarkdown p, .stMarkdown li { font-size: 1.04rem; line-height: 1.7; color: #292923; }
h1, h2, h3, h4 { font-family: 'Source Serif 4', Georgia, serif !important; color: #292923 !important; }
h2 { border-bottom: 2px solid #E9D99B; padding-bottom: .35rem; margin-top: 2.6rem !important; }
h4 { margin-top: 1.4rem !important; font-weight: 600 !important; }
a, a:visited { color: #8C6D1F !important; }
.block-container { padding-top: 2.2rem; max-width: 820px; }

.hero { padding: 1.6rem 0 1.2rem 0; border-bottom: 1px solid #E9D99B; margin-bottom: .6rem; }
.hero .kicker { letter-spacing: .14em; text-transform: uppercase; font-size: .78rem; color: #77766E; }
.hero h1 { font-size: 2.6rem; margin: .2rem 0 .3rem 0; padding: 0; }
.hero .sub { color: #77766E; font-size: 1.05rem; }
.hero .meta { margin-top: .8rem; font-size: .92rem; color: #77766E; }
.group { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: .5rem; margin-top: 1rem; }
.group div { background: #FBF7E9; border-top: 2px solid #D6B75C; padding: .5rem .7rem; border-radius: 3px; }
.group b { display: block; font-size: .95rem; color: #292923; }
.group span { display: block; font-size: .9rem; color: #77766E; direction: rtl; text-align: left; }
.uni-ar { direction: rtl; unicode-bidi: isolate; }

.note { background: #FBF7E9; border-left: 4px solid #D6B75C; padding: .8rem 1rem; border-radius: 4px; margin: 1rem 0; }
.note p { margin: 0; }

table.acad { width: 100%; border-collapse: collapse; margin: .8rem 0 1.2rem 0; font-size: .95rem; }
table.acad th { background: #EFE5C2; color: #292923; text-align: left; padding: .5rem .6rem; font-weight: 600; border-bottom: 2px solid #D6B75C; }
table.acad td { padding: .5rem .6rem; border-bottom: 1px solid #E7E1CF; vertical-align: top; }
table.acad tr:nth-child(even) td { background: #FBF9F2; }

ol.steps { padding-left: 0; list-style: none; counter-reset: s; margin: .8rem 0 1.2rem 0; }
ol.steps li { counter-increment: s; position: relative; padding: .35rem 0 .35rem 2.6rem; line-height: 1.65; }
ol.steps li::before { content: counter(s); position: absolute; left: 0; top: .4rem; width: 1.8rem; height: 1.8rem;
    border-radius: 50%; background: #E9D99B; color: #292923; font-weight: 600; text-align: center; line-height: 1.8rem; font-size: .9rem; }

.code-title { font-family: 'Source Serif 4', Georgia, serif; font-weight: 600; margin: 1rem 0 .3rem 0; }
[data-testid="stCode"] pre, .stCode pre { background: #FFFDF6 !important; border: 1px solid #E7E1CF; }
[data-testid="stCode"] code { font-size: .86rem !important; color: #292923 !important; }

[data-testid="stImageCaption"], .stImage figcaption, [data-testid="caption"] { color: #77766E !important; font-size: .88rem !important; }
[data-testid="stSidebar"] { background: #EFEADB; }
[data-testid="stSidebar"] a { text-decoration: none; display: block; padding: .18rem 0; color: #292923 !important; }
[data-testid="stSidebar"] a:hover { color: #8C6D1F !important; }
[data-testid="stMetricValue"] { font-family: 'Source Serif 4', Georgia, serif; color: #292923; }
.stButton button { background: #D6B75C; color: #292923; border: none; font-weight: 600; padding: .5rem 1.4rem; }
.stButton button:hover { background: #C9A84A; color: #292923; }
.chip { display: inline-block; background: #F1E8C8; border-radius: 12px; padding: .15rem .6rem; margin: .15rem; font-size: .85rem; }
.small { color: #77766E; font-size: .9rem; }
</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------ helpers
def inline(text):
    """Escape HTML and turn **bold** into <b>."""
    text = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)


def render_table(headers, rows):
    head = "".join(f"<th>{inline(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{inline(str(c))}</td>" for c in r) + "</tr>" for r in rows)
    st.markdown(f'<table class="acad"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>',
                unsafe_allow_html=True)


def render_block(block):
    kind = block[0]
    if kind == "p":
        st.markdown(block[1])
    elif kind == "h":
        st.markdown(f"#### {block[1]}")
    elif kind == "bullets":
        st.markdown("\n".join(f"- {b}" for b in block[1]))
    elif kind == "steps":
        items = "".join(f"<li><b>{inline(t)}.</b> {inline(d)}</li>" for t, d in block[1])
        st.markdown(f'<ol class="steps">{items}</ol>', unsafe_allow_html=True)
    elif kind == "table":
        render_table(block[1], block[2])
    elif kind == "eq":
        st.latex(block[1])
    elif kind == "code":
        if block[1]:
            st.markdown(f'<div class="code-title">{inline(block[1])}</div>', unsafe_allow_html=True)
        st.code(block[2], language=None)
    elif kind == "img":
        st.image(str(ASSETS / block[1]), caption=block[2], width="stretch")
    elif kind == "note":
        st.markdown(f'<div class="note"><p>{inline(block[1])}</p></div>', unsafe_allow_html=True)


# ------------------------------------------------------------------ sidebar
nav = [(s["id"], s["title"]) for s in SECTIONS] + [("demo", "Additional Practical Example"), ("references", "References")]
with st.sidebar:
    st.markdown("### Contents")
    st.markdown("".join(f'<a href="#{i}">{n}. {t}</a>' for n, (i, t) in enumerate(nav, 1)), unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<span class="small">{PROJECT_INFO["course"]}<br>{PROJECT_INFO["university"]}<br>'
                f'<span class="uni-ar">{PROJECT_INFO["university_ar"]}</span></span>', unsafe_allow_html=True)

# ------------------------------------------------------------------ header
members = "".join(f"<div><b>{en}</b><span>{ar}</span></div>" for en, ar in PROJECT_INFO["members"])
uni = f'{PROJECT_INFO["university"]} · <span class="uni-ar">{PROJECT_INFO["university_ar"]}</span>'
st.markdown(
    f"""
<div class="hero">
  <div class="kicker">{PROJECT_INFO["course"]} · Course Project</div>
  <h1>Isolation Forest</h1>
  <div class="sub">Algorithm Explanation, Pseudocode, and Time Complexity Analysis</div>
  <div class="meta">{uni} · Instructor: {PROJECT_INFO["instructor"]}</div>
  <div class="group">{members}</div>
</div>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ academic sections
for number, section in enumerate(SECTIONS, 1):
    st.header(f"{number}. {section['title']}", anchor=section["id"])
    for block in section["blocks"]:
        render_block(block)

# ------------------------------------------------------------------ additional practical example
st.header(f"{len(SECTIONS) + 1}. {DEMO_TITLE}", anchor="demo")
st.markdown(DEMO_INTRO)


@st.cache_data
def load_data():
    raw = demo.load_raw()
    X, labels, report = demo.preprocess(raw)
    return X, report


X, report = load_data()

st.markdown(
    f"**Dataset:** {demo.DATASET_NAME}, Canadian Institute for Cybersecurity, University of New Brunswick "
    f"([official page]({demo.SOURCE_URL})). We use a bundled sample of {report['rows_in']:,} records and "
    f"{report['n_features']} numeric features. The dataset's label column is not used by the model."
)
st.markdown(
    f"**Model:** sklearn.ensemble.IsolationForest with t = {demo.MODEL_PARAMS['n_estimators']} trees, "
    f"ψ = {demo.MODEL_PARAMS['max_samples']} and contamination = {demo.MODEL_PARAMS['contamination']}. "
    "It returns 1 for normal points and −1 for anomalies."
)
with st.expander("Show the selected features and a data preview"):
    st.markdown(", ".join(demo.FEATURES))
    st.dataframe(X.head(5), width="stretch", hide_index=True)

if st.button("Run Detection"):
    with st.spinner("Training Isolation Forest..."):
        model, pred, score, decision = demo.run_isolation_forest(X)
    st.session_state["result"] = {"pred": pred, "score": score, "threshold": -model.offset_}

res = st.session_state.get("result")
if res is None:
    st.markdown('<p class="small">Press <b>Run Detection</b> to train the model on the sample.</p>',
                unsafe_allow_html=True)
else:
    pred, score, thr = res["pred"], res["score"], res["threshold"]
    n_normal, n_anom = int((pred == 1).sum()), int((pred == -1).sum())
    m1, m2 = st.columns(2)
    m1.metric("Normal (prediction = 1)", f"{n_normal:,}")
    m2.metric("Anomalies (prediction = −1)", f"{n_anom:,}")

    chart_df = pd.DataFrame({"score": score, "Prediction": ["Anomaly" if v == -1 else "Normal" for v in pred]})
    hist = (
        alt.Chart(chart_df)
        .mark_bar(opacity=0.9)
        .encode(
            x=alt.X("score:Q", bin=alt.Bin(maxbins=45), title="Anomaly score s(x, ψ)"),
            y=alt.Y("count():Q", title="Number of records"),
            color=alt.Color("Prediction:N", scale=alt.Scale(domain=["Normal", "Anomaly"], range=[GOLD, RUST]),
                            legend=alt.Legend(orient="top", title=None)),
        )
    )
    rule = alt.Chart(pd.DataFrame({"t": [thr]})).mark_rule(color=CHAR, strokeDash=[5, 4], size=1.5).encode(x="t:Q")
    chart = (hist + rule).properties(height=300).configure(background=IVORY).configure_view(
        stroke=None).configure_axis(labelColor=GRAY, titleColor=CHAR, gridColor="#E7E1CF", domainColor=GRAY)
    st.altair_chart(chart, width="stretch", theme=None)

    top = X.copy()
    top.insert(0, "Anomaly score", score.round(3))
    top = top[pred == -1].sort_values("Anomaly score", ascending=False).head(5)
    st.markdown("**Records with the highest anomaly scores**")
    st.dataframe(top[["Anomaly score", "Flow Duration", "Total Fwd Packets", "Flow Bytes/s", "Average Packet Size"]]
                 .round(1).assign(**{"Anomaly score": top["Anomaly score"]}), width="stretch", hide_index=True)

    st.markdown(
        f"The model marked **{n_anom:,}** records as anomalies and **{n_normal:,}** as normal. Records to the right "
        f"of the dashed line (score above about {thr:.3f}) had the shortest average path lengths, so they were the "
        "easiest to isolate. As explained in the Applications section, an anomaly is an unusual record, not a "
        "confirmed problem, so it still needs to be checked."
    )

# ------------------------------------------------------------------ references
st.header(f"{len(SECTIONS) + 2}. References", anchor="references")
for i, ref in enumerate(REFERENCES, 1):
    st.markdown(f"{i}. {ref}")

st.markdown("---")
st.markdown(f'<p class="small">{PROJECT_INFO["course"]} · {PROJECT_INFO["university"]}</p>', unsafe_allow_html=True)
