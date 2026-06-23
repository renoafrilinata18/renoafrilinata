import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="Piala Dunia 2026 Analytics",
    page_icon="🏆",
    layout="wide"
)

# ======================
# DATA
# ======================
df = pd.read_csv("data_pialadunia.csv")

# ======================
# SIDEBAR
# ======================
st.sidebar.title("🏆 FIFA WORLD CUP 2026")

benua = st.sidebar.multiselect(
    "Pilih Benua",
    df["Benua"].unique(),
    default=df["Benua"].unique()
)

df = df[df["Benua"].isin(benua)]

# ======================
# HEADER
# ======================
st.title("🏆 FIFA World Cup 2026 Analytics Dashboard")

st.markdown("""
### Analisis Performa Negara Peserta Piala Dunia

Dashboard ini dibuat untuk menganalisis performa negara peserta Piala Dunia
berdasarkan statistik pertandingan, produktivitas gol, kekuatan pertahanan,
serta peluang menjadi kandidat juara.

Melalui dashboard ini pengguna dapat memahami performa setiap negara
secara visual dan interaktif.
""")

st.info(
    "📌 Gunakan filter benua pada sidebar untuk melakukan analisis yang lebih spesifik."
)

st.divider()

# ======================
# KPI
# ======================
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("🌍 Total Negara", len(df))

with col2:
    st.metric("⚽ Total Gol", int(df["Goal_Masuk"].sum()))

with col3:
    st.metric("🏅 Total Poin", int(df["Poin"].sum()))

with col4:
    st.metric("🛡️ Clean Sheet", int(df["Clean_Sheet"].sum()))

st.divider()

# ======================
# POWER SCORE
# ======================
df["Power_Score"] = (
    df["Poin"] * 10
    + df["Goal_Masuk"] * 2
    + df["Clean_Sheet"] * 3
)

# ======================
# TOP 5 KANDIDAT JUARA
# ======================
st.subheader("🏆 Top 5 Kandidat Juara")

top5 = df.sort_values(
    "Power_Score",
    ascending=False
).head(5)

st.dataframe(
    top5[
        [
            "Negara",
            "Poin",
            "Goal_Masuk",
            "Clean_Sheet",
            "Power_Score"
        ]
    ],
    use_container_width=True
)

# ======================
# GRAFIK POWER RANKING
# ======================
fig1 = px.bar(
    top5,
    x="Negara",
    y="Power_Score",
    color="Power_Score",
    title="Power Ranking Negara"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ======================
# PRODUKTIVITAS GOL
# ======================
st.subheader("⚽ Analisis Produktivitas Gol")

fig2 = px.bar(
    df.sort_values(
        "Goal_Masuk",
        ascending=False
    ),
    x="Negara",
    y="Goal_Masuk",
    color="Goal_Masuk",
    title="Negara dengan Goal Terbanyak"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ======================
# PERTAHANAN
# ======================
st.subheader("🛡️ Analisis Pertahanan")

fig3 = px.bar(
    df.sort_values(
        "Clean_Sheet",
        ascending=False
    ),
    x="Negara",
    y="Clean_Sheet",
    color="Clean_Sheet",
    title="Clean Sheet Setiap Negara"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ======================
# PERFORMA BENUA
# ======================
st.subheader("🌎 Performa Berdasarkan Benua")

benua_data = (
    df.groupby("Benua")["Poin"]
    .sum()
    .reset_index()
)

fig4 = px.pie(
    benua_data,
    names="Benua",
    values="Poin",
    hole=0.5,
    title="Distribusi Poin per Benua"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ======================
# SCATTER
# ======================
st.subheader("📈 Hubungan Goal dan Poin")

fig5 = px.scatter(
    df,
    x="Goal_Masuk",
    y="Poin",
    size="Power_Score",
    color="Benua",
    hover_name="Negara"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ======================
# PREDIKSI JUARA
# ======================
juara = top5.iloc[0]

st.success(
    f"🏆 Berdasarkan statistik yang dianalisis, "
    f"{juara['Negara']} merupakan kandidat juara terkuat "
    f"dengan Power Score sebesar {juara['Power_Score']}."
)

# ======================
# TABEL LENGKAP
# ======================
st.subheader("📋 Tabel Statistik Lengkap")

ranking = df.sort_values(
    "Power_Score",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True
)

# ======================
# KESIMPULAN
# ======================
st.markdown("---")

st.markdown("""
## Kesimpulan

Berdasarkan hasil analisis statistik, performa setiap negara dapat
dievaluasi menggunakan kombinasi poin, jumlah gol, dan clean sheet.

Negara dengan nilai Power Score tertinggi menunjukkan konsistensi
yang baik dalam menyerang maupun bertahan sehingga memiliki peluang
lebih besar untuk menjadi kandidat juara.

Dashboard ini dibuat untuk membantu proses analisis data olahraga
menggunakan Python, Pandas, Plotly, dan Streamlit.

### Teknologi yang Digunakan

- Python
- Pandas
- Plotly
- Streamlit
""")
