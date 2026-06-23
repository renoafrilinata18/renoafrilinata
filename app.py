import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Statistik Piala Dunia",
    page_icon="🏆",
    layout="wide"
)

# CSS Tampilan
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

[data-testid="metric-container"]{
    background: linear-gradient(135deg,#1E293B,#334155);
    border-radius:15px;
    padding:20px;
    box-shadow:0px 0px 15px rgba(0,0,0,0.3);
}

h1,h2,h3{
    color:white;
}
</style>
""", unsafe_allow_html=True)

# Membaca Data
df = pd.read_csv("data_pialadunia.csv")

# Sidebar
st.sidebar.title("🏆 Menu Dashboard")

negara = st.sidebar.multiselect(
    "Pilih Negara",
    options=df["Negara"],
    default=df["Negara"]
)

df = df[df["Negara"].isin(negara)]

# Header
st.title("🏆 Dashboard Statistik Piala Dunia")

st.markdown("""
### Analisis Performa Negara Peserta Piala Dunia

Selamat datang di Dashboard Statistik Piala Dunia.

Dashboard ini dibuat untuk menyajikan informasi mengenai performa
negara-negara peserta berdasarkan jumlah pertandingan, kemenangan,
kekalahan, jumlah gol yang dicetak, serta total poin yang diperoleh.

Melalui dashboard ini pengguna dapat:

✅ Melihat performa masing-masing negara

✅ Membandingkan jumlah poin antar negara

✅ Menganalisis produktivitas gol

✅ Mengetahui negara dengan performa terbaik

✅ Melakukan analisis data secara interaktif melalui visualisasi grafik

Visualisasi data yang ditampilkan bertujuan untuk mempermudah
pemahaman terhadap kondisi dan performa setiap negara dalam kompetisi.
""")

st.info(
    "📌 Gunakan menu filter pada sidebar sebelah kiri untuk memilih negara yang ingin dianalisis."
)

st.divider()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🌍 Total Negara", len(df))

with col2:
    st.metric("⚽ Total Goal", int(df["Goal_Masuk"].sum()))

with col3:
    st.metric("🏅 Total Poin", int(df["Poin"].sum()))

with col4:
    st.metric("📈 Rata-rata Poin", round(df["Poin"].mean(), 2))

st.divider()

# Grafik Ranking
col1, col2 = st.columns(2)

ranking = df.sort_values(
    by="Poin",
    ascending=False
)

with col1:
    fig1 = px.bar(
        ranking,
        x="Negara",
        y="Poin",
        color="Poin",
        title="🏅 Ranking Negara Berdasarkan Poin"
    )

    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(
        df,
        names="Negara",
        values="Poin",
        hole=0.5,
        title="📊 Distribusi Poin"
    )

    st.plotly_chart(fig2, use_container_width=True)

# Grafik Goal
col3, col4 = st.columns(2)

with col3:
    fig3 = px.bar(
        df,
        x="Goal_Masuk",
        y="Negara",
        orientation="h",
        color="Goal_Masuk",
        title="⚽ Goal Masuk Setiap Negara"
    )

    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.scatter(
        df,
        x="Goal_Masuk",
        y="Poin",
        size="Poin",
        color="Negara",
        title="🎯 Hubungan Goal dan Poin"
    )

    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# Negara Terbaik
terbaik = df.loc[df["Poin"].idxmax()]

st.success(
    f"🏆 Negara terbaik saat ini adalah {terbaik['Negara']} dengan total {terbaik['Poin']} poin."
)

# Tabel Ranking
st.subheader("📋 Tabel Ranking Lengkap")

st.dataframe(
    ranking,
    use_container_width=True
)

# Kesimpulan
st.markdown("---")

st.markdown("""
## Kesimpulan

Berdasarkan hasil analisis data, terlihat bahwa negara dengan jumlah poin yang tinggi
cenderung memiliki produktivitas gol yang lebih baik dibandingkan negara lainnya.

Dashboard ini membantu pengguna memahami performa setiap negara melalui
visualisasi data yang interaktif, sehingga proses analisis menjadi lebih mudah
dan informatif.

### Teknologi yang Digunakan

- Python
- Pandas
- Plotly
- Streamlit

Terima kasih telah menggunakan Dashboard Statistik Piala Dunia.
""")
