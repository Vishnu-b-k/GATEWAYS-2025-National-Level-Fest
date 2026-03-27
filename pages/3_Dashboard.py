import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Executive Dashboard - GATEWAYS 2025",
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
    background:linear-gradient(120deg,#0284c7 0%,#1d4ed8 60%,#4f46e5 100%);
    border-radius:18px; padding:1.5rem 2rem; color:white;
    margin-bottom:1.4rem; box-shadow:0 6px 24px rgba(2,132,199,.22);
}
.page-header h2{font-size:1.8rem;font-weight:800;margin:0;}
.page-header p{font-size:.9rem;opacity:.92;margin:.3rem 0 0 0;}

.kpi-dash{
    background:rgba(255,255,255,.92);
    border:1px solid #bfdbfe; border-radius:16px;
    padding:1rem 1.2rem; text-align:center;
    box-shadow:0 4px 18px rgba(29,78,216,.08);
    transition:transform .2s, box-shadow .2s;
}
.kpi-dash:hover{transform:translateY(-3px);box-shadow:0 8px 26px rgba(29,78,216,.16);}
.kpi-dash .label{font-size:.67rem;font-weight:700;letter-spacing:.09em;
    text-transform:uppercase;color:#2563eb;margin-bottom:.12rem;}
.kpi-dash .value{font-size:1.7rem;font-weight:800;color:#0f2d5e;line-height:1;}
.kpi-dash .value-sm{font-size:1.2rem;font-weight:800;color:#0f2d5e;line-height:1.1;}

.section-title{font-size:1.05rem;font-weight:700;color:#0f2d5e;
    border-left:4px solid #3b82f6;padding-left:.55rem;margin-bottom:.9rem;}
.soft-divider{border:none;border-top:1px solid #bfdbfe;margin:1.3rem 0;}
.insight-card{
    background:rgba(255,255,255,.92);border:1px solid #bfdbfe;border-radius:14px;
    padding:.9rem 1.1rem; margin-bottom:.7rem;
    box-shadow:0 2px 12px rgba(29,78,216,.07);
}
.insight-title{font-size:.82rem;font-weight:700;color:#0f2d5e;margin-bottom:.3rem;}
.insight-body{font-size:.83rem;color:#0f2d5e;line-height:1.5;}
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
    st.markdown('<p style="font-size:.75rem;font-weight:700;color:#0f2d5e;text-transform:uppercase;letter-spacing:.07em;">Dashboard Filters</p>', unsafe_allow_html=True)
    all_events = ["All"] + sorted(df["Event Name"].unique().tolist())
    sel_events = st.multiselect("Events", all_events[1:], default=all_events[1:])
    all_states = ["All"] + sorted(df["State"].unique().tolist())
    sel_state  = st.selectbox("State", all_states)
    sel_type   = st.radio("Event Type", ["All", "Individual", "Group"])
    st.markdown("---")
    st.caption("Christ University - Advance PP - 2025")

dff = df.copy()
if sel_events:          dff = dff[dff["Event Name"].isin(sel_events)]
if sel_state != "All":  dff = dff[dff["State"]     == sel_state]
if sel_type  != "All":  dff = dff[dff["Event Type"]== sel_type]

total   = len(dff)
revenue = dff["Amount Paid"].sum()
avg_r   = dff["Rating"].mean()
top_ev  = dff["Event Name"].value_counts().idxmax() if total else "-"
top_st  = dff["State"].value_counts().idxmax()      if total else "-"
top_col = dff["College"].value_counts().idxmax()    if total else "-"

st.markdown(f"""
<div class="page-header">
  <h2>Executive Dashboard</h2>
  <p>Comprehensive overview - {total:,} participants - Rs.{revenue:,.0f} revenue - {avg_r:.2f}/5 avg rating</p>
</div>
""", unsafe_allow_html=True)

krow = st.columns(6)
KPIS = [
    ("Participants", f"{total:,}",            "value"),
    ("Revenue",      f"Rs.{revenue:,.0f}",    "value-sm"),
    ("Avg Rating",   f"{avg_r:.2f}/5",        "value"),
    ("Top Event",    top_ev,                  "value-sm"),
    ("Top State",    top_st,                  "value-sm"),
    ("Top College",  top_col,                 "value-sm"),
]
for col, (label, value, cls) in zip(krow, KPIS):
    col.markdown(f"""
    <div class="kpi-dash">
        <div class="label">{label}</div>
        <div class="{cls}">{value}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)

c1, c2 = st.columns([3, 2])
with c1:
    st.markdown('<div class="section-title">State x Event Participation Bubble Chart</div>', unsafe_allow_html=True)
    bubble = dff.groupby(["State","Event Name"]).agg(
        Count=("Student Name","count"),
        Avg_Rating=("Rating","mean")
    ).reset_index()
    fig_bub = px.scatter(bubble, x="Event Name", y="State",
                         size="Count", color="Avg_Rating",
                         color_continuous_scale=["#dbeafe","#93c5fd","#1d4ed8"],
                         hover_data={"Count":True,"Avg_Rating":":.2f"},
                         size_max=45,
                         title="Bubble size = Participants - Color = Avg Rating")
    fig_bub.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=CHART_FONT, title_font=TITLE_FONT,
        margin=dict(l=5,r=5,t=40,b=5),
        xaxis=dict(gridcolor="#bfdbfe", tickangle=-30,
                   tickfont=TICK_FONT, title_font=TICK_FONT),
        yaxis=dict(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT),
        coloraxis_colorbar=dict(title="Avg Rating",
                                tickfont=TICK_FONT, titlefont=TICK_FONT),
        height=400,
    )
    st.plotly_chart(fig_bub, use_container_width=True)

with c2:
    st.markdown('<div class="section-title">Top Colleges by Revenue</div>', unsafe_allow_html=True)
    col_rev = dff.groupby("College")["Amount Paid"].sum().nlargest(8).reset_index()
    col_rev.columns = ["College","Revenue"]
    fig_cr = px.bar(col_rev.sort_values("Revenue"), x="Revenue", y="College",
                    orientation="h", color="Revenue",
                    color_continuous_scale=["#dbeafe","#1d4ed8"],
                    text="Revenue")
    fig_cr.update_traces(texttemplate="Rs.%{text:,.0f}", textposition="outside",
                         textfont=dict(color=DARK))
    fig_cr.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=CHART_FONT, margin=dict(l=5,r=30,t=10,b=5),
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=TICK_FONT, title_font=TICK_FONT),
        height=400,
    )
    st.plotly_chart(fig_cr, use_container_width=True)

st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown('<div class="section-title">State - College - Event Sunburst</div>', unsafe_allow_html=True)
    fig_sun = px.sunburst(dff, path=["State","College","Event Name"],
                          color_discrete_sequence=PASTEL,
                          title="Hierarchical Participation Breakdown")
    fig_sun.update_layout(paper_bgcolor=PLOT_BG,
                          font=CHART_FONT, title_font=TITLE_FONT,
                          margin=dict(l=5,r=5,t=40,b=5), height=400)
    st.plotly_chart(fig_sun, use_container_width=True)

with c4:
    st.markdown('<div class="section-title">Rating Distribution per Event (Box Plot)</div>', unsafe_allow_html=True)
    fig_box = px.box(dff, x="Event Name", y="Rating",
                     color="Event Name", color_discrete_sequence=PASTEL,
                     points="all", title="Rating Spread per Event")
    fig_box.update_layout(
        showlegend=False, plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=CHART_FONT, title_font=TITLE_FONT,
        margin=dict(l=5,r=5,t=40,b=5),
        xaxis=dict(gridcolor="#bfdbfe", tickangle=-25,
                   tickfont=TICK_FONT, title_font=TICK_FONT),
        yaxis=dict(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT),
        height=400,
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)

c5, c6 = st.columns([2, 1])
with c5:
    st.markdown('<div class="section-title">Participants per Event Type by State</div>', unsafe_allow_html=True)
    gb = dff.groupby(["State","Event Type"]).size().reset_index(name="Count")
    fig_gb = px.bar(gb, x="State", y="Count", color="Event Type",
                    barmode="group",
                    color_discrete_sequence=["#bfdbfe","#93c5fd"],
                    text_auto=True)
    fig_gb.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=CHART_FONT, margin=dict(l=5,r=5,t=10,b=5),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", tickangle=-30,
                   tickfont=TICK_FONT, title_font=TICK_FONT),
        yaxis=dict(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT),
        legend=dict(font_size=11, bgcolor="rgba(0,0,0,0)",
                    font=dict(color=DARK)),
    )
    st.plotly_chart(fig_gb, use_container_width=True)

with c6:
    st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)
    top_event_count = dff["Event Name"].value_counts().max() if total else 0
    top_state_count = dff["State"].value_counts().max()      if total else 0
    pct_group       = round(100 * (dff["Event Type"] == "Group").sum() / total, 1) if total else 0
    pct_ind         = round(100 - pct_group, 1) if total else 0
    high_rat_ev     = dff.groupby("Event Name")["Rating"].mean().idxmax() if total else "-"

    insights = [
        ("Most Popular Event",
         f"<b>{top_ev}</b> leads with <b>{top_event_count}</b> participants."),
        ("Most Active State",
         f"<b>{top_st}</b> sent the most students (<b>{top_state_count}</b>)."),
        ("Event Type Split",
         f"<b>{pct_ind}%</b> Individual - <b>{pct_group}%</b> Group events."),
        ("Highest Rated Event",
         f"<b>{high_rat_ev}</b> has the best average rating."),
        ("Total Revenue",
         f"Fest collected <b>Rs.{revenue:,.0f}</b> from registrations."),
    ]
    for title, body in insights:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-title">{title}</div>
            <div class="insight-body">{body}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<hr class='soft-divider'>", unsafe_allow_html=True)

st.markdown('<div class="section-title">Registration Fee vs Rating (Scatter)</div>', unsafe_allow_html=True)
fig_sc = px.scatter(dff, x="Amount Paid", y="Rating",
                    color="Event Name", size_max=14,
                    color_discrete_sequence=PASTEL,
                    opacity=0.85,
                    hover_data=["College","State"],
                    trendline="lowess",
                    title="Does a higher fee lead to better rating?")
fig_sc.update_layout(
    plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
    font=CHART_FONT, title_font=TITLE_FONT,
    margin=dict(l=5,r=5,t=40,b=5),
    xaxis=dict(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT),
    yaxis=dict(gridcolor="#bfdbfe", tickfont=TICK_FONT, title_font=TICK_FONT),
    legend=dict(font_size=11, bgcolor="rgba(0,0,0,0)", font=dict(color=DARK)),
)
st.plotly_chart(fig_sc, use_container_width=True)
