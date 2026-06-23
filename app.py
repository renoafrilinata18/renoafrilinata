import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================
st.set_page_config(
    page_title="FIFA World Cup 2026 Analytics Hub",
    page_icon="🏆",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================
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

# ==================================================
# MEMBACA DATA
# ==================================================
df = pd.read_csv("data_pialadunia.csv")

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.title("🏆 FIFA WORLD CUP 2026")

benua = st.sidebar.multiselect(
    "Pilih Benua",
    options=df["Benua"].unique(),
    default=df["Benua"].unique()
)

df = df[df["Benua"].isin(benua)]

# ==================================================
# POWER SCORE
# ==================================================
df["Power_Score"] = (
    df["Poin"] * 10 +
    df["Goal_Masuk"] * 2 +
    df["Clean_Sheet"] * 3
)

# ==================================================
# HERO SECTION
# ==================================================
st.title("🏆 FIFA World Cup 2026 Analytics Hub")

st.markdown("""
### *Exploring Performance, Dominance, and the Road to Glory*

Selamat datang di **FIFA World Cup 2026 Analytics Hub**, sebuah dashboard
interaktif yang dirancang untuk mengungkap cerita di balik angka dan statistik.

Piala Dunia bukan sekadar tentang menang atau kalah. Setiap pertandingan
menghasilkan data yang menggambarkan kekuatan tim, efektivitas strategi,
ketajaman lini serang, hingga ketangguhan pertahanan.

Melalui visualisasi dan analisis yang disajikan, dashboard ini membantu
mengidentifikasi negara-negara yang paling dominan, tim dengan performa
terbaik, serta kandidat terkuat untuk mengangkat trofi Piala Dunia 2026.

⚽ Analisis Performa Tim  
🛡️ Evaluasi Kekuatan Pertahanan  
🌎 Dominasi Antar Benua  
🏆 Prediksi Kandidat Juara Dunia  

*"Every statistic tells a story. Every match creates history."*
""")

st.info(
    "📌 Gunakan filter benua pada sidebar untuk melakukan analisis yang lebih spesifik."
)

st.divider()

# ==================================================
# KPI
# ==================================================
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

# ==================================================
# TOP 5 KANDIDAT JUARA
# ==================================================
st.markdown("""
## 🏆 Race for the Trophy

Persaingan menuju gelar juara dunia semakin menarik untuk dianalisis.
Berdasarkan kombinasi poin, produktivitas gol, dan kekuatan pertahanan,
berikut adalah negara-negara yang memiliki peluang terbesar untuk menjadi
penguasa sepak bola dunia.
""")

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

fig1 = px.bar(
    top5,
    x="Negara",
    y="Power_Score",
    color="Power_Score",
    title="🏆 Top 5 Kandidat Juara Dunia"
)

st.plotly_chart(fig1, use_container_width=True)

# ==================================================
# PRODUKTIVITAS GOL
# ==================================================
st.markdown("""
## ⚽ The Goal Machines

Gol adalah mata uang utama dalam sepak bola.

Bagian ini menampilkan negara-negara dengan produktivitas serangan
tertinggi sepanjang kompetisi. Semakin banyak gol yang dicetak,
semakin besar peluang tim untuk mengendalikan pertandingan.
""")

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

st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# PERTAHANAN
# ==================================================
st.markdown("""
## 🛡️ The Wall of Defense

Tim juara tidak hanya membutuhkan serangan yang tajam,
tetapi juga pertahanan yang solid.

Analisis berikut menunjukkan negara-negara yang mampu menjaga
stabilitas permainan dengan meminimalkan peluang lawan.
""")

fig3 = px.bar(
    df.sort_values(
        "Clean_Sheet",
        ascending=False
    ),
    x="Negara",
    y="Clean_Sheet",
    color="Clean_Sheet",
    title="Kekuatan Pertahanan Negara Peserta"
)

st.plotly_chart(fig3, use_container_width=True)

# ==================================================
# BENUA
# ==================================================
st.markdown("""
## 🌎 Continental Dominance

Piala Dunia mempertemukan berbagai gaya bermain dari seluruh dunia.

Analisis ini memperlihatkan bagaimana setiap benua berkontribusi
terhadap persaingan global dan siapa yang mendominasi turnamen.
""")

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
    title="Distribusi Poin Berdasarkan Benua"
)

st.plotly_chart(fig4, use_container_width=True)

# ==================================================
# SCATTER
# ==================================================
st.markdown("""
## 📈 Goal vs Points Analysis

Visualisasi berikut menunjukkan hubungan antara jumlah gol
yang dicetak dengan total poin yang diperoleh setiap negara.

Semakin besar ukuran lingkaran, semakin tinggi kekuatan
keseluruhan negara tersebut berdasarkan Power Score.
""")

fig5 = px.scatter(
    df,
    x="Goal_Masuk",
    y="Poin",
    size="Power_Score",
    color="Benua",
    hover_name="Negara"
)

st.plotly_chart(fig5, use_container_width=True)

# ==================================================
# INSIGHT
# ==================================================
terproduktif = df.loc[df["Goal_Masuk"].idxmax()]
terbaik = df.loc[df["Power_Score"].idxmax()]
pertahanan = df.loc[df["Clean_Sheet"].idxmax()]

st.markdown("## 🔥 Tournament Insights")

st.success(f"⚽ Negara paling produktif: {terproduktif['Negara']} ({terproduktif['Goal_Masuk']} gol)")
st.success(f"🛡️ Pertahanan terbaik: {pertahanan['Negara']} ({pertahanan['Clean_Sheet']} clean sheet)")
st.success(f"🏆 Kandidat juara terkuat: {terbaik['Negara']}")

# ==================================================
# PREDIKSI JUARA
# ==================================================
st.markdown("## 🔮 Road to Glory")

st.success(
    f"""
🏆 Berdasarkan kombinasi statistik poin, jumlah gol,
dan kekuatan pertahanan, {terbaik['Negara']}
muncul sebagai kandidat terkuat untuk menjuarai
FIFA World Cup 2026.

Konsistensi performa mereka menunjukkan dominasi
yang lebih baik dibandingkan negara peserta lainnya.
"""
)

# ==================================================
# TABEL
# ==================================================
st.subheader("📋 Statistik Lengkap Peserta")

ranking = df.sort_values(
    "Power_Score",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True
)

# ==================================================
# PENUTUP
# ==================================================
st.markdown("---")

st.markdown("""
# 📖 Final Whistle

Statistik memang tidak dapat meramalkan masa depan dengan sempurna,
namun mampu memberikan gambaran mengenai siapa yang tampil paling dominan
sepanjang kompetisi.

Dari ketajaman lini serang hingga kokohnya pertahanan, setiap angka
menceritakan perjalanan sebuah negara dalam mengejar kejayaan di panggung
sepak bola terbesar di dunia.

Pada akhirnya, hanya satu negara yang akan mengangkat trofi.
Namun berdasarkan data yang tersedia, kita dapat melihat siapa yang
paling siap untuk menuliskan sejarah baru di FIFA World Cup 2026.

### ⚽ Data Never Lies. Champions Make History.
""")
