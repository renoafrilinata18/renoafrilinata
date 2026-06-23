import streamlit as st
import pandas as pd

st.title("🏆 Dashboard Statistik Piala Dunia")

df = pd.read_csv("data_pialadunia.csv")

st.header("Data Piala Dunia")
st.dataframe(df)

st.header("Statistik Umum")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Jumlah Tim", len(df))

with col2:
    st.metric("Rata-rata Poin", round(df["Poin"].mean(), 2))

with col3:
    st.metric("Total Gol", df["Goal_Masuk"].sum())

st.header("Tim dengan Poin Tertinggi")

tim_terbaik = df.loc[df["Poin"].idxmax()]

st.success(
    f"{tim_terbaik['Negara']} memperoleh {tim_terbaik['Poin']} poin."
)

st.header("Grafik Poin Setiap Negara")
st.bar_chart(df.set_index("Negara")["Poin"])

st.header("Grafik Goal Masuk")
st.bar_chart(df.set_index("Negara")["Goal_Masuk"])

st.header("Ranking Tim")
ranking = df.sort_values(by="Poin", ascending=False)
st.dataframe(ranking)
