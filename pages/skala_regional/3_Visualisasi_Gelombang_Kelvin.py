# File: pages/2_skala_regional/3_Visualisasi_Gelombang_Kelvin.py

import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="Visualisasi Gelombang Kelvin", layout="wide")
st.title("🌊 Gelombang Kelvin Atmosfer")

st.markdown("""
Gelombang Kelvin adalah gelombang atmosfer tropis yang merambat dari barat ke timur, sering membawa gangguan konvektif
dan meningkatkan peluang hujan di sepanjang jalurnya.

🗓️ **Tanggal Pengamatan**: {today}
""".format(today=datetime.today().strftime("%d %B %Y")))

# Jalur perkiraan gelombang Kelvin (dummy)
kelvin_coords = [
    [-5, 90], [-5, 100], [-5, 110], [-5, 120], [-5, 130], [-5, 140], [-5, 150]
]

m = folium.Map(location=[-5, 120], zoom_start=4, tiles="cartodbpositron")
folium.PolyLine(locations=kelvin_coords, color="purple", weight=4, tooltip="Jalur Gelombang Kelvin").add_to(m)
folium.Marker(location=[-5, 120], icon=folium.Icon(color="purple"), popup="Posisi Saat Ini (Simulasi)").add_to(m)

st.markdown("### 🗺️ Jalur Pergerakan Gelombang Kelvin")
st_data = st_folium(m, width=700, height=500)

st.markdown("### 🧠 Penjelasan Tambahan")
st.markdown("""
Gelombang Kelvin berkontribusi pada peningkatan curah hujan dan pembentukan awan konvektif,
terutama saat berinteraksi dengan MJO atau faktor lokal. Deteksi biasanya berdasarkan data OLR, angin zonal,
dan tekanan di atmosfer bawah hingga tengah.
""")

st.caption("📌 Visualisasi berbasis simulasi. Pembaruan ke data satelit/inframerah akan diterapkan ke depannya.")
