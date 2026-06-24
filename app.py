import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="FIFA World Cup 2026 Command Center",
    page_icon="🏆",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================
st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

h1,h2,h3,h4{
    color:white;
}

[data-testid="metric-container"]{
    background:linear-gradient(135deg,#1E293B,#334155);
    border-radius:18px;
    padding:20px;
    border:1px solid #475569;
    box-shadow:0px 0px 20px rgba(59,130,246,0.3);
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================
df = pd.read_csv("data_pialadunia.csv")

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.title("🏆 FIFA World Cup 2026")

benua = st.sidebar.multiselect(
    "Filter Benua",
    options=df["Benua"].unique(),
    default=df["Benua"].unique()
)

df = df[df["Benua"].isin(benua)]

# ==================================================
# POWER SCORE
# ==================================================
df["Power_Score"] = (
    df["Poin"] * 10
    + df["Goal_Masuk"] * 2
    + df["Clean_Sheet"] * 3
)

# ==================================================
# HERO BANNER
# ==================================================
st.markdown("""
<div style="
background: linear-gradient(90deg,#0f172a,#1e3a8a,#7c3aed);
padding:45px;
border-radius:25px;
text-align:center;
color:white;
margin-bottom:25px;
box-shadow:0px 0px 30px rgba(124,58,237,0.5);
">

<h1>🏆 FIFA WORLD CUP 2026 COMMAND CENTER</h1>

<h3>The Ultimate Football Analytics Experience</h3>

<h4>⚽ 48 Nations • 🌎 6 Continents • 🏆 One Champion</h4>

<p>
Explore team performance, group standings,
continental dominance and championship predictions.
</p>

<h4><i>The Road To Glory Begins Here</i></h4>

</div>
""", unsafe_allow_html=True)

st.info(
    "📌 Gunakan filter benua di sidebar untuk melakukan analisis lebih spesifik."
)

st.divider()

# ==================================================
# KPI
# ==================================================
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "🌍 Total Negara",
        len(df)
    )

with col2:
    st.metric(
        "⚽ Total Gol",
        int(df["Goal_Masuk"].sum())
    )

with col3:
    st.metric(
        "🏅 Total Poin",
        int(df["Poin"].sum())
    )

with col4:
    st.metric(
        "🛡️ Clean Sheet",
        int(df["Clean_Sheet"].sum())
    )

st.divider()

# ==================================================
# PODIUM JUARA
# ==================================================
top5 = (
    df.sort_values(
        "Power_Score",
        ascending=False
    )
    .head(5)
)

st.markdown("""
# 🏅 Championship Podium

Berikut adalah negara dengan performa terbaik
berdasarkan kombinasi poin, produktivitas gol,
dan kekuatan pertahanan.
""")

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(
        "🥈 Runner Up",
        top5.iloc[1]["Negara"],
        top5.iloc[1]["Power_Score"]
    )

with col2:
    st.metric(
        "🥇 Favorite Champion",
        top5.iloc[0]["Negara"],
        top5.iloc[0]["Power_Score"]
    )

with col3:
    st.metric(
        "🥉 Third Place",
        top5.iloc[2]["Negara"],
        top5.iloc[2]["Power_Score"]
    )

st.balloons()

# ==================================================
# TOP 5 POWER SCORE
# ==================================================
fig_top = px.bar(
    top5,
    x="Negara",
    y="Power_Score",
    color="Power_Score",
    title="🏆 Top 5 Championship Contenders"
)

st.plotly_chart(
    fig_top,
    use_container_width=True
)

# ==================================================
# WINNER PROBABILITY
# ==================================================
st.markdown("""
# 🔮 World Cup Winner Probability

Prediksi peluang juara berdasarkan
Power Score masing-masing negara.
""")

prob = top5.copy()

prob["Probability"] = (
    prob["Power_Score"]
    /
    prob["Power_Score"].sum()
    * 100
)

for _, row in prob.iterrows():

    st.write(
        f"🏆 {row['Negara']} ({row['Probability']:.1f}%)"
    )

    st.progress(
        int(row["Probability"])
    )

st.divider()
# ==================================================
# GROUP STAGE STANDINGS
# ==================================================
st.markdown("""
# 🏟️ FIFA World Cup Group Stage

Fase grup menjadi fondasi perjalanan menuju gelar juara dunia.
Pilih grup untuk melihat klasemen dan tim yang berpotensi lolos.
""")

grup_pilih = st.selectbox(
    "Pilih Grup",
    sorted(df["Grup"].unique())
)

grup_df = (
    df[df["Grup"] == grup_pilih]
    .sort_values(
        ["Poin", "Goal_Masuk"],
        ascending=False
    )
)

st.subheader(f"🏆 Klasemen Grup {grup_pilih}")

st.dataframe(
    grup_df[
        [
            "Negara",
            "Poin",
            "Goal_Masuk",
            "Goal_Kemasukan",
            "Clean_Sheet"
        ]
    ],
    use_container_width=True
)

fig_group = px.bar(
    grup_df,
    x="Negara",
    y="Poin",
    color="Poin",
    title=f"Klasemen Grup {grup_pilih}"
)

st.plotly_chart(
    fig_group,
    use_container_width=True
)

juara_grup = grup_df.iloc[0]

st.success(
    f"🥇 Pemuncak Grup {grup_pilih}: {juara_grup['Negara']} "
    f"dengan {juara_grup['Poin']} poin."
)

lolos = grup_df.head(2)

st.info(
    f"✅ Prediksi Lolos Babak Berikutnya: "
    f"{lolos.iloc[0]['Negara']} dan "
    f"{lolos.iloc[1]['Negara']}"
)

st.divider()

# ==================================================
# GOAL MACHINES
# ==================================================
st.markdown("""
# ⚽ The Goal Machines

Negara-negara dengan produktivitas gol tertinggi sepanjang kompetisi.
""")

fig_goal = px.bar(
    df.sort_values(
        "Goal_Masuk",
        ascending=False
    ),
    x="Negara",
    y="Goal_Masuk",
    color="Goal_Masuk",
    title="Top Goal Scoring Nations"
)

st.plotly_chart(
    fig_goal,
    use_container_width=True
)

# ==================================================
# DEFENSE WALL
# ==================================================
st.markdown("""
# 🛡️ The Wall of Defense

Pertahanan terbaik sering kali menjadi pembeda
antara tim bagus dan tim juara.
""")

fig_def = px.bar(
    df.sort_values(
        "Clean_Sheet",
        ascending=False
    ),
    x="Negara",
    y="Clean_Sheet",
    color="Clean_Sheet",
    title="Best Defensive Teams"
)

st.plotly_chart(
    fig_def,
    use_container_width=True
)

st.divider()

# ==================================================
# CONTINENTAL DOMINANCE
# ==================================================
st.markdown("""
# 🌎 Continental Dominance

Perbandingan kekuatan antar benua berdasarkan total poin.
""")

benua_data = (
    df.groupby("Benua")["Poin"]
    .sum()
    .reset_index()
)

fig_benua = px.pie(
    benua_data,
    names="Benua",
    values="Poin",
    hole=0.5,
    title="Point Distribution by Continent"
)

st.plotly_chart(
    fig_benua,
    use_container_width=True
)

st.divider()

# ==================================================
# GOAL VS POINTS
# ==================================================
st.markdown("""
# 📈 Goal vs Points Analysis

Hubungan antara jumlah gol dan poin yang diperoleh.
Semakin besar lingkaran, semakin tinggi Power Score.
""")

fig_scatter = px.scatter(
    df,
    x="Goal_Masuk",
    y="Poin",
    size="Power_Score",
    color="Benua",
    hover_name="Negara"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# ==================================================
# POWER RANKING
# ==================================================
st.markdown("""
# 🌟 Power Ranking

15 negara dengan Power Score tertinggi.
""")

ranking = df.sort_values(
    "Power_Score",
    ascending=False
)

fig_rank = px.line(
    ranking.head(15),
    x="Negara",
    y="Power_Score",
    markers=True,
    title="Top 15 Power Ranking"
)

st.plotly_chart(
    fig_rank,
    use_container_width=True
)

st.divider()
