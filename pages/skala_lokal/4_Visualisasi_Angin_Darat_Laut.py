# File: pages/3_skala_lokal/4_Visualisasi_Angin_Darat_Laut.py

import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="Visualisasi Angin Darat dan Laut", layout="wide")
st.title("🌬️ Angin Darat dan Angin Laut")

st.markdown("""
Angin darat–laut merupakan sirkulasi angin lokal yang disebabkan oleh perbedaan pemanasan antara daratan dan lautan.
Fenomena ini sangat penting dalam membentuk cuaca harian di wilayah pesisir.

🗓️ **Tanggal Pengamatan**: {today}
""".format(today=datetime.today().strftime("%d %B %Y")))

# Lokasi simulasi (pantai utara Jawa, misalnya Gresik)
m = folium.Map(location=[-7.15, 112.65], zoom_start=10, tiles="cartodbpositron")
folium.Marker(location=[-7.15, 112.65], popup="Wilayah Pesisir Gresik", icon=folium.Icon(color="blue")).add_to(m)
folium.Circle(location=[-7.15, 112.65], radius=8000, color="blue", fill=True, fill_opacity=0.25,
              tooltip="Zona pengaruh angin darat dan laut").add_to(m)

st.markdown("### 🗺️ Lokasi Simulasi Angin Darat–Laut")
st_data = st_folium(m, width=700, height=500)

st.markdown("### 🌊 Penjelasan Tambahan")
st.markdown("""
- **Siang hari**: Daratan lebih cepat panas → tekanan rendah → angin bertiup dari laut → **angin laut**.
- **Malam hari**: Laut lebih lambat mendingin → tekanan relatif lebih rendah di laut → angin bertiup dari darat → **angin darat**.

Pola ini sangat umum di wilayah pesisir Indonesia, dan sering memicu **awan konvektif di sore hari**.
""")

st.caption("📌 Contoh lokasi: Gresik, Jawa Timur. Simulasi ini untuk edukasi dinamika pesisir.")
