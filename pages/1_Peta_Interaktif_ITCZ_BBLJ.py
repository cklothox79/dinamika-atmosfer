# File: pages/2_skala_regional/1_Visualisasi_ITCZ.py

import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="Visualisasi ITCZ", layout="wide")
st.title("🌧️ Zona Konvergensi Intertropis (ITCZ)")

st.markdown("""
ITCZ adalah daerah bertemunya angin pasat timur laut dan tenggara yang mengangkat udara hangat dan lembab ke atas,
menghasilkan awan dan hujan. Lokasi ITCZ tidak tetap dan dapat bergeser ke utara atau selatan tergantung musim.

🗓️ **Tanggal Pengamatan**: {today}
""".format(today=datetime.today().strftime("%d %B %Y")))

# Koordinat perkiraan posisi ITCZ (misalnya dari satelit atau analisis manual)
itcz_coords = [
    [0, 90], [2, 110], [0, 120], [-1, 130], [-2, 140], [-1, 150], [0, 160]
]

m = folium.Map(location=[0, 120], zoom_start=4, tiles="cartodbpositron")
folium.PolyLine(locations=itcz_coords, color="red", weight=4, tooltip="Perkiraan Posisi ITCZ").add_to(m)
folium.Marker(location=[-1, 130], icon=folium.Icon(color="red"), popup="Posisi Tengah ITCZ").add_to(m)

st.markdown("### 🗺️ Peta Perkiraan Posisi ITCZ")
st_data = st_folium(m, width=700, height=500)

st.markdown("### 📊 Indeks ITCZ (jika tersedia)")
st.info("Saat ini belum tersedia indeks kuantitatif untuk ITCZ secara resmi. Analisis berbasis citra satelit dan konvergensi angin digunakan sebagai indikasi.")

st.caption("📌 Sumber estimasi posisi: simulasi / dummy data. Versi dinamis akan terhubung ke dataset satelit di versi berikutnya.")
