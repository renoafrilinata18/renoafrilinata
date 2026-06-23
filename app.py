import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Piala Dunia",
    page_icon="🏆",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

[data-testid="metric-container"]{
    background: linear-gradient(135deg,#1E293B,#334155);
    border-radius:15px;
    padding:20px;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.3);
}

h1,h2,h3{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# Membaca data
df = pd.read_csv("data_pialadunia.csv")

# Sidebar
st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/861/861512.png",
    width=80
)

st.sidebar.title("🏆 Statistik Piala Dunia")

negara = st.sidebar.multiselect(
    "Pilih Negara",
    options=df["Negara"],
    default=df["Negara"]
)

df = df[df["Negara"].isin(negara)]

# Judul
st.title("🏆 Dashboard Statistik Piala Dunia")
st.markdown("### Analisis Performa Negara Peserta")

st.divider()

# KPI Cards
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "🌍 Total Negara",
        len(df)
    )

with col2:
    st.metric(
        "⚽ Total Goal",
        int(df["Goal_Masuk"].sum())
    )

with col3:
    st.metric(
        "🏅 Total Poin",
        int(df["Poin"].sum())
    )

with col4:
    st.metric(
        "📈 Rata-rata Poin",
        round(df["Poin"].mean(),2)
    )

st.divider()

# Grafik 1 dan 2
col1,col2 = st.columns(2)

with col1:

    top_poin = df.sort_values(
        by="Poin",
        ascending=False
    )

    fig1 = px.bar(
        top_poin,
        x="Negara",
        y="Poin",
        color="Poin",
        title="🏅 Ranking Berdasarkan Poin"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:

    fig2 = px.pie(
        df,
        values="Poin",
        names="Negara",
        hole=0.5,
        title="📊 Distribusi Poin"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# Grafik 3 dan 4
col3,col4 = st.columns(2)

with col3:

    fig3 = px.bar(
        df,
        x="Goal_Masuk",
        y="Negara",
        orientation="h",
        color="Goal_Masuk",
        title="⚽ Goal Masuk Tiap Negara"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col4:

    fig4 = px.scatter(
        df,
        x="Goal_Masuk",
        y="Poin",
        size="Poin",
        color="Negara",
        title="🎯 Hubungan Goal dan Poin"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

st.divider()

# Tim Terbaik
terbaik = df.loc[df["Poin"].idxmax()]

st.success(
    f"🏆 Negara terbaik saat ini adalah {terbaik['Negara']} dengan {terbaik['Poin']} poin."
)

# Tabel Ranking
st.subheader("📋 Tabel Ranking Lengkap")

ranking = df.sort_values(
    by="Poin",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True
)

st.markdown("---")
st.caption("Dibuat dengan Streamlit • Dashboard Statistik Piala Dunia")
