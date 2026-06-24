import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="FIFA World Cup Legends Dashboard",
    page_icon="🏆",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

champions = pd.read_csv("world_cup_champions.csv")
scorers = pd.read_csv("world_cup_top_scorers.csv")

# ==================================================
# DARK THEME CSS
# ==================================================

st.markdown("""
<style>

.main {
    background-color:#0E1117;
}

[data-testid="stSidebar"]{
    background-color:#111827;
}

.hero{
    background: linear-gradient(135deg,#001F54,#003566);
    padding:35px;
    border-radius:20px;
    color:white;
    text-align:center;
    margin-bottom:20px;
}

.kpi-card{
    background:#1F2937;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 0px 15px rgba(0,255,255,0.2);
    animation: pulse 2s infinite;
}

@keyframes pulse{
    0%{transform:scale(1);}
    50%{transform:scale(1.03);}
    100%{transform:scale(1);}
}

.big-number{
    font-size:32px;
    font-weight:bold;
    color:#00E5FF;
}

.section{
    background:#1F2937;
    padding:15px;
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("⚙ Dashboard Filter")

selected_country = st.sidebar.multiselect(
    "Filter Champion",
    champions["Champion"].unique(),
    default=champions["Champion"].unique()
)

filtered = champions[
    champions["Champion"].isin(selected_country)
]

# ==================================================
# HERO
# ==================================================

st.markdown("""
<div class='hero'>
<h1>🏆 FIFA World Cup Legends & History Analytics</h1>
<h4>1930 - 2022 Historical Football Intelligence Dashboard</h4>
</div>
""", unsafe_allow_html=True)

# ==================================================
# KPI SECTION
# ==================================================

tournament = len(champions)

champion_count = champions["Champion"].nunique()

top_scorer_count = len(scorers)

col1,col2,col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>Tournaments</h4>
    <div class='big-number'>{tournament}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>Champion Nations</h4>
    <div class='big-number'>{champion_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
    <h4>Top Scorers</h4>
    <div class='big-number'>{top_scorer_count}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================================================
# TIMELINE
# ==================================================

st.subheader("🏆 World Cup Champions Timeline")

timeline = px.scatter(
    filtered,
    x="Year",
    y="Champion",
    color="Champion",
    size=[18]*len(filtered),
    template="plotly_dark"
)

st.plotly_chart(
    timeline,
    use_container_width=True
)

# ==================================================
# TITLES BAR
# ==================================================

titles = champions["Champion"].value_counts().reset_index()
titles.columns = ["Country","Titles"]

st.subheader("🥇 Championship Ranking")

rank_fig = px.bar(
    titles,
    x="Country",
    y="Titles",
    color="Titles",
    text="Titles",
    template="plotly_dark"
)

st.plotly_chart(rank_fig, use_container_width=True)

# ==================================================
# PIE CHART
# ==================================================

st.subheader("🥧 World Cup Title Distribution")

pie = px.pie(
    titles,
    values="Titles",
    names="Country",
    hole=0.4,
    template="plotly_dark"
)

st.plotly_chart(pie, use_container_width=True)

# ==================================================
# TREEMAP
# ==================================================

st.subheader("🌎 Treemap Championship Distribution")

tree = px.treemap(
    titles,
    path=["Country"],
    values="Titles",
    color="Titles"
)

st.plotly_chart(tree, use_container_width=True)

# ==================================================
# TOP SCORERS
# ==================================================

st.subheader("⚽ Top World Cup Scorers")

top10 = scorers.sort_values(
    "Goals",
    ascending=False
).head(10)

goal_fig = px.bar(
    top10,
    x="Goals",
    y="Player",
    orientation="h",
    color="Goals",
    text="Goals",
    template="plotly_dark"
)

st.plotly_chart(goal_fig, use_container_width=True)

# ==================================================
# PLAYER COMPARISON
# ==================================================

st.subheader("🆚 Player Comparison")

c1,c2 = st.columns(2)

player1 = c1.selectbox(
    "Player 1",
    scorers["Player"]
)

player2 = c2.selectbox(
    "Player 2",
    scorers["Player"],
    index=1
)

compare = scorers[
    scorers["Player"].isin([player1,player2])
]

compare_fig = px.bar(
    compare,
    x="Player",
    y=["Goals","Matches"],
    barmode="group",
    template="plotly_dark"
)

st.plotly_chart(compare_fig, use_container_width=True)

# ==================================================
# GOALS VS MATCHES
# ==================================================

st.subheader("📈 Goals vs Matches")

scatter = px.scatter(
    scorers,
    x="Matches",
    y="Goals",
    size="Goals",
    color="Country",
    hover_name="Player",
    template="plotly_dark"
)

st.plotly_chart(scatter, use_container_width=True)

# ==================================================
# HEATMAP
# ==================================================

st.subheader("🔥 Performance Heatmap")

heat = scorers.copy()

heat["Efficiency"] = (
    heat["Goals"] /
    heat["Matches"]
).round(2)

heatmap = go.Figure(
    data=go.Heatmap(
        z=[heat["Efficiency"]],
        x=heat["Player"],
        y=["Goal Efficiency"]
    )
)

heatmap.update_layout(
    template="plotly_dark",
    height=300
)

st.plotly_chart(
    heatmap,
    use_container_width=True
)

# ==================================================
# RANKING TABLE
# ==================================================

st.subheader("🏅 World Cup Legend Ranking")

ranking = scorers.sort_values(
    ["Goals","Matches"],
    ascending=[False,True]
)

ranking.insert(
    0,
    "Rank",
    range(1,len(ranking)+1)
)

st.dataframe(
    ranking,
    use_container_width=True
)

# ==================================================
# INSIGHTS
# ==================================================

st.subheader("🧠 Automated Insights")

top_country = titles.iloc[0]["Country"]
top_titles = titles.iloc[0]["Titles"]

best_player = scorers.loc[
    scorers["Goals"].idxmax(),
    "Player"
]

best_goal = scorers["Goals"].max()

st.success(f"""

🏆 Most Successful Nation: {top_country}

🥇 Total Titles: {top_titles}

⚽ Greatest Scorer: {best_player}

🎯 Total Goals: {best_goal}

📊 Germany dominates both title races and top scorer records.

🌟 Lionel Messi and Kylian Mbappé represent the modern era of World Cup legends.

""")

# ==================================================
# DATASET
# ==================================================

st.subheader("📋 Full Dataset")

tab1,tab2 = st.tabs([
    "Champions",
    "Top Scorers"
])

with tab1:
    st.dataframe(
        champions,
        use_container_width=True
    )

with tab2:
    st.dataframe(
        scorers,
        use_container_width=True
    )

# ==================================================
# CONCLUSION
# ==================================================

st.subheader("📌 Executive Summary")

st.info("""
The FIFA World Cup is the most prestigious football tournament in history.

Brazil remains the most successful nation in terms of championships,
while Miroslav Klose holds the all-time World Cup scoring record.

Interactive analytics reveal long-term dominance trends,
player efficiency, championship distribution,
and historical evolution of football greatness.
""")
