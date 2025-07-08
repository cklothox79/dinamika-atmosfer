# File: pages/skala_global/1_Visualisasi_Nino34.py

import streamlit as st

st.set_page_config(page_title="Visualisasi Nino 3.4", layout="wide")
st.title("📍 Visualisasi Area Nino 3.4")

st.markdown("""
**Area Nino 3.4** adalah zona penting di Samudra Pasifik Tropis (antara 5°LU–5°LS dan 170°BB–120°BB),
digunakan untuk memantau gangguan suhu laut seperti **El Niño** dan **La Niña**.

Berikut ini perbandingan visual kondisi atmosfer dan laut pada kedua fenomena:
""")

st.image("https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/el_nino_vs_la_nina.png", use_container_width=True, caption="Perbandingan kondisi atmosfer dan laut pada El Niño vs La Niña")

st.markdown("📌 Gambar ini hanya ilustrasi. Untuk analisis numerik gunakan indeks ENSO dan IOD.")
