# File: pages/3_skala_lokal/1_Visualisasi_Angin_Lembah_Gunung.py

import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="Visualisasi Angin Lembah-Gunung", layout="wide")
st.title("🌬️ Angin Lembah – Gunung")

st.markdown("""
Angin lembah–gunung adalah sirkulasi lokal harian yang umum terjadi di daerah pegunungan. Siang hari, udara naik dari lembah ke gunung (*angin gunung*),
sementara malam hari sebaliknya (*angin lembah*).

🗓️ **Tanggal Pengamatan**: {today}
""".format(today=datetime.today().strftime("%d %B %Y")))

# Lokasi simulasi (misalnya lereng Gunung Arjuno, Malang)
m = folium.Map(location=[-7.78, 112.57], zoom_start=10, tiles="cartodbpositron")
folium.Marker(location=[-7.78, 112.57], popup="Lereng Gunung Arjuno", icon=folium.Icon(color="green")).add_to(m)
folium.Circle(location=[-7.78, 112.57], radius=10000, color="green", fill=True, fill_opacity=0.2,
              tooltip="Zona dominan angin lembah–gunung").add_to(m)

st.markdown("### 🗺️ Lokasi Perkiraan Aktivitas Angin Lembah – Gunung")
st_data = st_folium(m, width=700, height=500)

st.markdown("### 🧭 Penjelasan Tambahan")
st.markdown("""
- **Siang hari**: permukaan gunung lebih cepat panas, udara naik → angin dari lembah menuju puncak.
- **Malam hari**: udara di lereng mendingin dan turun → angin dari puncak ke lembah.

Fenomena ini penting dalam pembentukan awan orografis dan potensi hujan lokal di daerah pegunungan.
""")

st.caption("📌 Contoh lokasi: Gunung Arjuno, Jawa Timur. Visualisasi ini bersifat simulasi untuk keperluan edukasi.")
