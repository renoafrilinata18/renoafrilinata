import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="FIFA World Cup Dashboard",
    page_icon="🏆",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
champions = pd.read_csv("world_cup_champions.csv")
scorers = pd.read_csv("world_cup_top_scorers.csv")

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.main {
    background-color:#f5f7fa;
}

.hero {
    background: linear-gradient(135deg,#001F54,#00509D);
    padding:40px;
    border-radius:15px;
    text-align:center;
    color:white;
}

.kpi {
    background:white;
    padding:20px;
    border-radius:12px;
    text-align:center;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================

st.markdown("""
<div class="hero">
<h1>🏆 FIFA World Cup Legends & History Analytics Dashboard</h1>
<h4>Explore World Cup Champions, Legends, Records & Historical Insights</h4>
</div>
""", unsafe_allow_html=True)

st.write("")

# =========================
# KPI
# =========================

total_tournaments = champions["Year"].count()
total_champions = champions["Champion"].nunique()
total_scorers = scorers["Player"].count()

c1,c2,c3 = st.columns(3)

with c1:
    st.metric("🏆 Total Tournaments", total_tournaments)

with c2:
    st.metric("🌎 Champion Countries", total_champions)

with c3:
    st.metric("⚽ Top Scorers Listed", total_scorers)

st.divider()

# =========================
# TIMELINE CHAMPIONS
# =========================

st.subheader("🏆 World Cup Champions Timeline")

fig = px.scatter(
    champions,
    x="Year",
    y="Champion",
    color="Champion",
    size=[15]*len(champions)
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# MOST TITLES
# =========================

st.subheader("🥇 Countries with Most World Cup Titles")

titles = champions["Champion"].value_counts().reset_index()
titles.columns=["Country","Titles"]

fig2 = px.bar(
    titles,
    x="Country",
    y="Titles",
    color="Titles",
    text="Titles"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# TOP SCORERS
# =========================

st.subheader("⚽ World Cup All-Time Top Scorers")

top10 = scorers.sort_values(
    "Goals",
    ascending=False
).head(10)

fig3 = px.bar(
    top10,
    x="Goals",
    y="Player",
    color="Goals",
    orientation="h",
    text="Goals"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# PLAYER COMPARISON
# =========================

st.subheader("🆚 Player Comparison")

col1,col2 = st.columns(2)

player1 = col1.selectbox(
    "Select Player 1",
    scorers["Player"]
)

player2 = col2.selectbox(
    "Select Player 2",
    scorers["Player"],
    index=1
)

compare = scorers[
    scorers["Player"].isin([player1,player2])
]

fig4 = px.bar(
    compare,
    x="Player",
    y=["Goals","Matches"],
    barmode="group"
)

st.plotly_chart(fig4, use_container_width=True)

# =========================
# GOALS VS MATCHES
# =========================

st.subheader("📈 Goals vs Matches Analysis")

fig5 = px.scatter(
    scorers,
    x="Matches",
    y="Goals",
    color="Country",
    size="Goals",
    hover_name="Player"
)

st.plotly_chart(fig5, use_container_width=True)

# =========================
# INSIGHT
# =========================

st.subheader("🧠 Automatic Insights")

top_country = titles.iloc[0]["Country"]
top_title = titles.iloc[0]["Titles"]

top_player = scorers.iloc[
    scorers["Goals"].idxmax()
]["Player"]

top_goals = scorers["Goals"].max()

st.success(
f"""
• Country with most titles: {top_country} ({top_title} titles)

• Greatest scorer: {top_player} ({top_goals} goals)

• Germany and Brazil dominate both championships and scoring records.

• Lionel Messi and Mbappe are active legends still shaping World Cup history.
"""
)

# =========================
# DATA TABLE
# =========================

st.subheader("📋 Complete Dataset")

tab1,tab2 = st.tabs(
    ["Champions Data","Top Scorer Data"]
)

with tab1:
    st.dataframe(champions,
                 use_container_width=True)

with tab2:
    st.dataframe(scorers,
                 use_container_width=True)

# =========================
# CONCLUSION
# =========================

st.subheader("📌 Final Conclusion")

st.info("""
The FIFA World Cup has produced legendary champions and players across generations.

Brazil remains the most successful nation, while Miroslav Klose holds the all-time scoring record.

The analysis demonstrates how football history can be explored through data visualization, helping identify trends, dominance periods, and player achievements over time.
""")
