import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Participation Trends - GATEWAYS 2025",
                   page_icon=None, layout="wide",
                   initial_sidebar_state="expanded")

DARK       = "#0f2d5e"
ACCENT     = "#3b82f6"
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
    background:linear-gradient(120deg,#1d4ed8 0%,#06b6d4 100%);
    border-radius:18px; padding:1.5rem 2rem; color:white;
    margin-bottom:1.4rem; box-shadow:0 6px 24px rgba(29,78,216,.2);
}
.page-header h2{font-size:1.8rem;font-weight:800;margin:0;letter-spacing:-.02em;}
.page-header p{font-size:.9rem;opacity:.92;margin:.3rem 0 0 0;}
.section-title{font-size:1.05rem;font-weight:700;color:#0f2d5e;
    border-left:4px solid #3b82f6;padding-left:.55rem;margin-bottom:.9rem;}
.soft-divider{border:none;border-top:1px solid #bfdbfe;margin:1.3rem 0;}
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
    st.markdown("---")
    st.caption("Christ University - Advance PP - 2025")

dff = df.copy()
if sel_event != "All": dff = dff[dff["Event Name"] == sel_event]
if sel_state != "All": dff = dff[dff["State"]      == sel_state]

st.markdown(f"""
<div class="page-header">
  <h2>Participation Trends</h2>
  <p>Analyzing {len(dff):,} participants - {dff['State'].nunique()} states - {dff['Event Name'].nunique()} events</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">State-wise Participation — India Map</div>', unsafe_allow_html=True)

state_counts = dff.groupby("State").size().reset_index(name="Participants")

fig_map = px.choropleth(
    state_counts,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey="properties.ST_NM",
    locations="State",
    color="Participants",
    color_continuous_scale=["#dbeafe","#93c5fd","#1d4ed8"],
    title="Number of Participants by State",
    hover_name="State",
    hover_data={"Participants": True},
)
fig_map.update_geos(fitbounds="locations", visible=False, bgcolor=PLOT_BG)
fig_map.update_layout(
    paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
    font=CHART_FONT, title_font=dict(size=15, color=DARK),
    margin=dict(l=0,r=0,t=40,b=0),
    coloraxis_colorbar=dict(title="Participants",
                            tickfont=TICK_FONT, titlefont=TICK_FONT),
    height=480,
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown('<div class="section-title">State-wise Participant Count</div>', unsafe_allow_html=True)
sc = state_counts.sort_values("Participants", ascending=False)
fig_st = px.bar(sc, x="State", y="Participants",
                color="State", color_discrete_sequence=PASTEL,
                text="Participants", title="Participants per State")
fig_st.update_traces(textposition="outside", textfont=dict(size=11, color=DARK))
fig_st.update_layout(showlegend=False, plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
                     font=CHART_FONT, title_font=TITLE_FONT,
                     margin=dict(l=5,r=5,t=40,b=5))
fig_st.update_xaxes(gridcolor="rgba(0,0,0,0)", tickfont=TICK_FONT, title_font=TICK_FONT)
fig_st.update_yaxes(gridcolor="#bfdbfe",       tickfont=TICK_FONT, title_font=TICK_FONT)
st.plotly_chart(fig_st, use_container_width=True)

st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown('<div class="section-title">Event-wise Breakdown</div>', unsafe_allow_html=True)
    ev = dff["Event Name"].value_counts().reset_index()
    ev.columns = ["Event","Count"]
    fig_ev = px.bar(ev, x="Count", y="Event", orientation="h",
                    color="Event", color_discrete_sequence=PASTEL, text="Count")
    fig_ev.update_traces(textposition="outside", textfont=dict(color=DARK))
    fig_ev.update_layout(showlegend=False, plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
                         font=CHART_FONT, margin=dict(l=5,r=20,t=10,b=5))
    fig_ev.update_xaxes(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT)
    fig_ev.update_yaxes(gridcolor="rgba(0,0,0,0)", tickfont=TICK_FONT, title_font=TICK_FONT)
    st.plotly_chart(fig_ev, use_container_width=True)

with c2:
    st.markdown('<div class="section-title">College-wise Participation (Top 12)</div>', unsafe_allow_html=True)
    cv = dff["College"].value_counts().head(12).reset_index()
    cv.columns = ["College","Count"]
    fig_cv = px.bar(cv, x="Count", y="College", orientation="h",
                    color="Count", color_continuous_scale=["#dbeafe","#1d4ed8"], text="Count")
    fig_cv.update_traces(textposition="outside", textfont=dict(color=DARK))
    fig_cv.update_layout(showlegend=False, plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
                         font=CHART_FONT, margin=dict(l=5,r=20,t=10,b=5),
                         coloraxis_showscale=False)
    fig_cv.update_xaxes(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT)
    fig_cv.update_yaxes(gridcolor="rgba(0,0,0,0)", tickfont=TICK_FONT, title_font=TICK_FONT)
    st.plotly_chart(fig_cv, use_container_width=True)

st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown('<div class="section-title">Individual vs Group Events</div>', unsafe_allow_html=True)
    et = dff["Event Type"].value_counts().reset_index()
    et.columns = ["Type","Count"]
    fig_et = px.pie(et, values="Count", names="Type",
                    color_discrete_sequence=["#bfdbfe","#93c5fd"], hole=0.5)
    fig_et.update_traces(textinfo="percent+label",
                         textfont=dict(size=13, color=DARK),
                         marker=dict(line=dict(color="#fff",width=3)))
    fig_et.update_layout(paper_bgcolor=PLOT_BG, font=CHART_FONT,
                         margin=dict(l=5,r=5,t=10,b=5),
                         legend=dict(font=dict(color=DARK, size=11)))
    st.plotly_chart(fig_et, use_container_width=True)

with c4:
    st.markdown('<div class="section-title">Revenue by Event</div>', unsafe_allow_html=True)
    rv = dff.groupby("Event Name")["Amount Paid"].sum().reset_index()
    rv.columns = ["Event","Revenue"]
    rv = rv.sort_values("Revenue", ascending=True)
    fig_rv = px.bar(rv, x="Revenue", y="Event", orientation="h",
                    color="Revenue", color_continuous_scale=["#dbeafe","#1d4ed8"],
                    text="Revenue")
    fig_rv.update_traces(texttemplate="Rs.%{text:,.0f}", textposition="outside",
                         textfont=dict(color=DARK))
    fig_rv.update_layout(showlegend=False, plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
                         font=CHART_FONT, margin=dict(l=5,r=20,t=10,b=5),
                         coloraxis_showscale=False)
    fig_rv.update_xaxes(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT)
    fig_rv.update_yaxes(gridcolor="rgba(0,0,0,0)", tickfont=TICK_FONT, title_font=TICK_FONT)
    st.plotly_chart(fig_rv, use_container_width=True)

st.markdown('<div class="section-title">College x Event Treemap</div>', unsafe_allow_html=True)
tm = dff.groupby(["College","Event Name"]).size().reset_index(name="Count")
fig_tm = px.treemap(tm, path=["College","Event Name"], values="Count",
                    color="Count",
                    color_continuous_scale=["#dbeafe","#93c5fd","#1d4ed8"],
                    title="College Distribution across Events")
fig_tm.update_layout(paper_bgcolor=PLOT_BG, font=CHART_FONT, title_font=TITLE_FONT,
                     margin=dict(l=5,r=5,t=40,b=5), coloraxis_showscale=False)
st.plotly_chart(fig_tm, use_container_width=True)
