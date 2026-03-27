import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="GATEWAYS 2025 - Analytics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

DARK       = "#0f2d5e"
MID        = "#1e4db7"
ACCENT     = "#3b82f6"
CHART_FONT = dict(family="Inter", size=12, color=DARK)
TITLE_FONT = dict(size=14, color=DARK)
TICK_FONT  = dict(color=DARK, size=11)
PLOT_BG    = "rgba(0,0,0,0)"
PASTEL     = ["#bfdbfe","#a5f3fc","#bbf7d0","#fde68a","#e9d5ff","#fed7aa","#a7f3d0","#fca5a5"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(155deg, #e8f4ff 0%, #f0f8ff 50%, #eef1ff 100%);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #dbeafe 0%, #e0e7ff 100%);
    border-right: 1px solid #bfdbfe;
}
[data-testid="stSidebar"] * { color: #0f2d5e !important; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

.hero-banner {
    background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 55%, #60a5fa 100%);
    border-radius: 20px;
    padding: 2.2rem 2.6rem;
    color: white;
    margin-bottom: 1.6rem;
    box-shadow: 0 8px 32px rgba(29,78,216,.22);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: ''; position: absolute; top: -50px; right: -50px;
    width: 220px; height: 220px; border-radius: 50%;
    background: rgba(255,255,255,.09);
}
.hero-banner h1 { font-size: 2.2rem; font-weight: 800; margin: 0; letter-spacing: -.02em; }
.hero-banner p  { font-size: .95rem; opacity: .92; margin: .35rem 0 0 0; }
.hero-tag {
    display: inline-block; background: rgba(255,255,255,.22);
    border-radius: 20px; padding: .22rem .85rem;
    font-size: .75rem; font-weight: 600; margin-bottom: .7rem; letter-spacing: .06em;
}

.kpi-card {
    background: rgba(255,255,255,.9);
    border: 1px solid #bfdbfe; border-radius: 16px;
    padding: 1.1rem 1.2rem; text-align: center;
    box-shadow: 0 4px 18px rgba(29,78,216,.08);
    transition: transform .2s, box-shadow .2s;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 26px rgba(29,78,216,.16); }
.kpi-label { font-size: .68rem; font-weight: 700; letter-spacing: .09em;
             text-transform: uppercase; color: #2563eb; margin-bottom: .15rem; }
.kpi-value { font-size: 1.9rem; font-weight: 800; color: #0f2d5e; line-height: 1; }
.kpi-value-sm { font-size: 1.3rem; font-weight: 800; color: #0f2d5e; line-height: 1.1; }
.kpi-sub   { font-size: .68rem; color: #3b82f6; margin-top: .18rem; }

.section-title {
    font-size: 1.05rem; font-weight: 700; color: #0f2d5e;
    border-left: 4px solid #3b82f6; padding-left: .55rem; margin-bottom: .9rem;
}
.soft-divider { border: none; border-top: 1px solid #bfdbfe; margin: 1.4rem 0; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "C5-FestDataset - fest_dataset.csv")
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df["Rating"]      = pd.to_numeric(df["Rating"],      errors="coerce")
    df["Amount Paid"] = pd.to_numeric(df["Amount Paid"], errors="coerce")
    return df

df = load_data()

with st.sidebar:
    st.markdown("## GATEWAYS 2025")
    st.markdown("**National Level Tech Fest**")
    st.markdown("---")
    st.markdown("##### Pages")
    st.page_link("app.py",                              label="Home")
    st.page_link("pages/1_Participation_Trends.py",     label="Participation Trends")
    st.page_link("pages/2_Feedback_Analysis.py",        label="Feedback and Ratings")
    st.page_link("pages/3_Dashboard.py",                label="Executive Dashboard")
    st.markdown("---")
    st.caption("Christ University - Advance PP - 2025")

st.markdown("""
<div class="hero-banner">
  <div class="hero-tag">National Level Fest Analytics - 2025</div>
  <h1>GATEWAYS 2025</h1>
  <p>Data Intelligence Platform - explore participation trends, feedback insights and revenue analytics from 250+ students across India.</p>
</div>
""", unsafe_allow_html=True)

total_students = len(df)
total_states   = df["State"].nunique()
total_colleges = df["College"].nunique()
total_events   = df["Event Name"].nunique()
avg_rating     = df["Rating"].mean()
total_revenue  = df["Amount Paid"].sum()
top_event      = df["Event Name"].value_counts().idxmax()
top_state      = df["State"].value_counts().idxmax()
top_ev_count   = df["Event Name"].value_counts().max()
top_st_count   = df["State"].value_counts().max()

CARDS = [
    ("Total Participants", f"{total_students:,}", "Across all events",   "kpi-value"),
    ("States Represented", f"{total_states}",    f"Top: {top_state}",   "kpi-value"),
    ("Colleges",           f"{total_colleges}",  "From across India",   "kpi-value"),
    ("Avg. Rating",        f"{avg_rating:.2f}/5", f"{total_students} reviews", "kpi-value"),
]
cols = st.columns(4)
for col, (label, value, sub, cls) in zip(cols, CARDS):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="{cls}">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

CARDS2 = [
    ("Events Hosted",  f"{total_events}",          "Diverse tech categories",    "kpi-value"),
    ("Total Revenue",  f"Rs.{total_revenue:,.0f}", "Registration fees",           "kpi-value"),
    ("Top Event",      top_event,                  f"{top_ev_count} participants","kpi-value-sm"),
    ("Top State",      top_state,                  f"{top_st_count} students",    "kpi-value-sm"),
]
cols2 = st.columns(4)
for col, (label, value, sub, cls) in zip(cols2, CARDS2):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="{cls}">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Quick Overview</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    ev = df["Event Name"].value_counts().reset_index()
    ev.columns = ["Event", "Count"]
    fig = px.bar(ev, x="Count", y="Event", orientation="h",
                 color="Event", color_discrete_sequence=PASTEL,
                 title="Participants per Event")
    fig.update_layout(showlegend=False, plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
                      font=CHART_FONT, title_font=TITLE_FONT,
                      margin=dict(l=5,r=5,t=40,b=5))
    fig.update_xaxes(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0)", tickfont=TICK_FONT, title_font=TICK_FONT)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    sv = df["State"].value_counts().reset_index()
    sv.columns = ["State","Count"]
    fig2 = px.pie(sv, values="Count", names="State",
                  color_discrete_sequence=PASTEL,
                  title="State-wise Participation", hole=0.42)
    fig2.update_layout(paper_bgcolor=PLOT_BG, font=CHART_FONT, title_font=TITLE_FONT,
                       margin=dict(l=5,r=5,t=40,b=5),
                       legend=dict(font=dict(color=DARK, size=11)))
    fig2.update_traces(textposition="inside", textinfo="percent+label",
                       textfont=dict(color=DARK, size=11),
                       marker=dict(line=dict(color="#fff", width=2)))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption("Use the sidebar to navigate to detailed analysis pages.")
