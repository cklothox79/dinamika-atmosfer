# File: pages/3_skala_lokal/3_Visualisasi_Efek_Urban.py

import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="Visualisasi Efek Urban", layout="wide")
st.title("🏙️ Efek Urban terhadap Cuaca")

st.markdown("""
Efek urban atau **urban heat island (UHI)** adalah pemanasan lokal yang terjadi di wilayah perkotaan akibat dominasi permukaan keras (aspal, beton),
kurangnya vegetasi, dan aktivitas manusia.

🗓️ **Tanggal Pengamatan**: {today}
""".format(today=datetime.today().strftime("%d %B %Y")))

# Lokasi simulasi (Jakarta Pusat)
m = folium.Map(location=[-6.2, 106.83], zoom_start=11, tiles="cartodbpositron")
folium.Circle(location=[-6.2, 106.83], radius=7000, color="orange", fill=True, fill_opacity=0.3,
              tooltip="Zona dominan Efek Urban").add_to(m)
folium.Marker([-6.2, 106.83], popup="Jakarta Pusat", icon=folium.Icon(color="orange")).add_to(m)

st.markdown("### 🗺️ Lokasi Efek Urban")
st_data = st_folium(m, width=700, height=500)

st.markdown("### 🔥 Penjelasan Tambahan")
st.markdown("""
- Wilayah urban menyimpan panas lebih lama dan mentransfernya ke atmosfer.
- Akibatnya, terbentuk pusat tekanan rendah mikro → udara lembap masuk → **awan konvektif** terbentuk.
- Efek ini memperbesar potensi **hujan lebat & petir lokal**, terutama saat sore–malam.

Kota besar seperti Jakarta, Surabaya, Medan sangat rentan terhadap efek ini, terutama saat musim kemarau.
""")

st.caption("📌 Data ini simulatif untuk edukasi. Integrasi data LST dan pengamatan radar akan ditambahkan pada versi selanjutnya.")
