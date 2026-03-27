import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import os
import io

st.set_page_config(page_title="Feedback Analysis - GATEWAYS 2025",
                   page_icon=None, layout="wide",
                   initial_sidebar_state="expanded")

DARK       = "#0f2d5e"
CHART_FONT = dict(family="Inter", size=12, color=DARK)
TITLE_FONT = dict(size=14, color=DARK)
TICK_FONT  = dict(color=DARK, size=11)
PLOT_BG    = "rgba(0,0,0,0)"
PASTEL     = ["#bfdbfe","#a5f3fc","#bbf7d0","#fde68a","#e9d5ff","#fed7aa","#a7f3d0","#fca5a5"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
[data-testid="stAppViewContainer"]{background:linear-gradient(155deg,#e8f4ff 0%,#f0f8ff 50%,#eef1ff 100%);}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#dbeafe 0%,#e0e7ff 100%);border-right:1px solid #bfdbfe;}
[data-testid="stSidebar"] *{color:#0f2d5e !important;}
.block-container{padding-top:1.2rem;}
.page-header{
    background:linear-gradient(120deg,#0ea5e9 0%,#1d4ed8 100%);
    border-radius:18px; padding:1.5rem 2rem; color:white;
    margin-bottom:1.4rem; box-shadow:0 6px 24px rgba(14,165,233,.22);
}
.page-header h2{font-size:1.8rem;font-weight:800;margin:0;}
.page-header p{font-size:.9rem;opacity:.92;margin:.3rem 0 0 0;}
.section-title{font-size:1.05rem;font-weight:700;color:#0f2d5e;
    border-left:4px solid #3b82f6;padding-left:.55rem;margin-bottom:.9rem;}
.soft-divider{border:none;border-top:1px solid #bfdbfe;margin:1.3rem 0;}
.feedback-chip{
    display:inline-block;background:rgba(59,130,246,.08);border:1px solid #bfdbfe;
    border-radius:30px;padding:.25rem .8rem;font-size:.78rem;
    color:#0f2d5e;margin:.2rem;font-weight:600;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    st.markdown('<p style="font-size:.75rem;font-weight:700;color:#0f2d5e;text-transform:uppercase;letter-spacing:.07em;">Filters</p>', unsafe_allow_html=True)
    all_events = ["All"] + sorted(df["Event Name"].unique().tolist())
    sel_event  = st.selectbox("Event", all_events)
    all_states = ["All"] + sorted(df["State"].unique().tolist())
    sel_state  = st.selectbox("State", all_states)
    min_r, max_r = st.slider("Rating Range", 1, 5, (1, 5))
    st.markdown("---")
    st.caption("Christ University - Advance PP - 2025")

dff = df.copy()
if sel_event != "All": dff = dff[dff["Event Name"] == sel_event]
if sel_state != "All": dff = dff[dff["State"]      == sel_state]
dff = dff[dff["Rating"].between(min_r, max_r)]

avg_r = dff["Rating"].mean()
total = len(dff)

st.markdown(f"""
<div class="page-header">
  <h2>Feedback and Ratings Analysis</h2>
  <p>Analysing {total:,} responses - Avg rating: {avg_r:.2f} / 5</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Feedback Word Cloud</div>', unsafe_allow_html=True)

feedback_text = " ".join(dff["Feedback on Fest"].dropna().tolist())

@st.cache_data
def make_wordcloud(text):
    stopwords = set(STOPWORDS)
    stopwords.update(["and","the","is","in","of","for","to","a","very","it","was"])
    wc = WordCloud(
        width=900, height=380,
        background_color=None, mode="RGBA",
        colormap="Blues",
        max_words=80,
        stopwords=stopwords,
        prefer_horizontal=0.85,
        min_font_size=10,
        max_font_size=80,
        collocations=False,
    )
    wc.generate(text)
    return wc

if feedback_text.strip():
    wc = make_wordcloud(feedback_text)
    fig_wc, ax = plt.subplots(figsize=(11, 4))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig_wc.patch.set_facecolor("#e8f4ff")
    ax.set_facecolor("#e8f4ff")
    buf = io.BytesIO()
    fig_wc.savefig(buf, format="png", bbox_inches="tight", facecolor="#e8f4ff", dpi=130)
    buf.seek(0)
    st.image(buf, use_column_width=True)
    plt.close(fig_wc)
else:
    st.info("No feedback text available for selected filters.")

st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="section-title">Rating Distribution</div>', unsafe_allow_html=True)
    rd = dff["Rating"].value_counts().sort_index().reset_index()
    rd.columns = ["Rating","Count"]
    fig_rd = px.bar(rd, x="Rating", y="Count",
                    color="Count",
                    color_continuous_scale=["#dbeafe","#1d4ed8"],
                    text="Count",
                    labels={"Rating":"Rating (out of 5)","Count":"Responses"})
    fig_rd.update_traces(textposition="outside", textfont=dict(size=12, color=DARK))
    fig_rd.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=CHART_FONT, margin=dict(l=5,r=5,t=10,b=5),
        coloraxis_showscale=False,
        xaxis=dict(tickmode="linear", tick0=1, dtick=1,
                   gridcolor="rgba(0,0,0,0)", tickfont=TICK_FONT, title_font=TICK_FONT),
        yaxis=dict(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT),
    )
    st.plotly_chart(fig_rd, use_container_width=True)

with c2:
    st.markdown('<div class="section-title">Avg. Rating per Event</div>', unsafe_allow_html=True)
    re = dff.groupby("Event Name")["Rating"].mean().reset_index()
    re.columns = ["Event","Avg Rating"]
    re = re.sort_values("Avg Rating", ascending=True)
    fig_re = px.bar(re, x="Avg Rating", y="Event", orientation="h",
                    color="Avg Rating",
                    color_continuous_scale=["#dbeafe","#1d4ed8"],
                    text="Avg Rating", range_x=[0,5.5])
    fig_re.update_traces(texttemplate="%{text:.2f}", textposition="outside",
                         textfont=dict(color=DARK))
    fig_re.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=CHART_FONT, margin=dict(l=5,r=30,t=10,b=5),
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=TICK_FONT, title_font=TICK_FONT),
    )
    st.plotly_chart(fig_re, use_container_width=True)

st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Feedback Sentiment Tag Frequency</div>', unsafe_allow_html=True)

KEYWORDS = {
    "Excellent experience":           "Excellent",
    "Fun and informative":            "Fun",
    "Challenging and useful":         "Challenging",
    "Creative and interactive":       "Creative",
    "Well organized and informative": "Well Organized",
    "Good exposure to projects":      "Good Exposure",
    "Interesting and engaging session":"Engaging",
    "Very engaging and practical":    "Practical",
    "Needs slight improvement in timing":"Needs Improvement",
    "Good learning experience":       "Good Learning",
    "Very creative event":            "Creative Event",
    "Well structured event":          "Well Structured",
}

counts = {}
for phrase, tag in KEYWORDS.items():
    cnt = dff["Feedback on Fest"].str.contains(phrase, case=False, na=False).sum()
    if cnt > 0:
        counts[tag] = cnt

if counts:
    kf = pd.DataFrame(list(counts.items()), columns=["Tag","Count"]).sort_values("Count", ascending=True)
    fig_kf = px.bar(kf, x="Count", y="Tag", orientation="h",
                    color="Count",
                    color_continuous_scale=["#dbeafe","#93c5fd","#1d4ed8"],
                    text="Count")
    fig_kf.update_traces(textposition="outside", textfont=dict(color=DARK))
    fig_kf.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=CHART_FONT, margin=dict(l=5,r=20,t=10,b=5),
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=TICK_FONT, title_font=TICK_FONT),
    )
    st.plotly_chart(fig_kf, use_container_width=True)
    chip_html = "".join([f'<span class="feedback-chip">{t} ({c})</span>' for t,c in counts.items()])
    st.markdown(chip_html, unsafe_allow_html=True)

st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Rating Heatmap - State x Event</div>', unsafe_allow_html=True)

heat = dff.pivot_table(index="State", columns="Event Name", values="Rating", aggfunc="mean")
fig_heat = px.imshow(heat.round(2),
                     color_continuous_scale=["#dbeafe","#93c5fd","#1d4ed8"],
                     text_auto=".2f", aspect="auto",
                     title="Average Rating by State x Event")
fig_heat.update_layout(
    paper_bgcolor=PLOT_BG, font=CHART_FONT, title_font=TITLE_FONT,
    margin=dict(l=5,r=5,t=40,b=5),
    coloraxis_colorbar=dict(title="Avg Rating",
                            tickfont=TICK_FONT, titlefont=TICK_FONT),
    xaxis=dict(tickfont=TICK_FONT, title_font=TICK_FONT),
    yaxis=dict(tickfont=TICK_FONT, title_font=TICK_FONT),
    height=400,
)
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)
st.markdown('<div class="section-title">All Feedback Records</div>', unsafe_allow_html=True)
search = st.text_input("Search feedback...", placeholder="Type keyword (e.g. excellent, creative)")
show_df = dff[["Student Name","College","State","Event Name","Rating","Feedback on Fest"]].copy()
show_df.columns = ["Name","College","State","Event","Rating","Feedback"]
if search:
    show_df = show_df[show_df["Feedback"].str.contains(search, case=False, na=False)]
show_df = show_df.sort_values("Rating", ascending=False).reset_index(drop=True)
st.dataframe(show_df, use_container_width=True, height=320)
st.caption(f"Showing {len(show_df)} records")
