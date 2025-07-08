# File: pages/3_skala_lokal/2_Visualisasi_Konvergensi_Mikro.py

import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="Visualisasi Konvergensi Mikro", layout="wide")
st.title("🌪️ Konvergensi Mikro")

st.markdown("""
Konvergensi mikro adalah fenomena bertemunya massa udara dalam skala sangat kecil (beberapa km),
sering terjadi di lingkungan urban atau dataran rendah akibat perbedaan suhu dan kelembapan.

🗓️ **Tanggal Pengamatan**: {today}
""".format(today=datetime.today().strftime("%d %B %Y")))

# Lokasi simulasi konvergensi mikro (misalnya kawasan Surabaya)
m = folium.Map(location=[-7.25, 112.75], zoom_start=11, tiles="cartodbpositron")
folium.Circle(location=[-7.25, 112.75], radius=5000, color="red", fill=True, fill_opacity=0.3,
              tooltip="Zona potensi konvergensi mikro (urban heating)").add_to(m)
folium.Marker([-7.25, 112.75], popup="Surabaya", icon=folium.Icon(color="red")).add_to(m)

st.markdown("### 🗺️ Lokasi Potensi Konvergensi Mikro")
st_data = st_folium(m, width=700, height=500)

st.markdown("### 🔬 Penjelasan Tambahan")
st.markdown("""
- **Pemanasan lokal** dari permukaan (asphalt, bangunan beton) menyebabkan udara panas naik.
- Jika bertemu dengan udara lembap dari sekitarnya → menciptakan konvergensi mikro.
- Potensi menghasilkan awan menjulang cepat (Cb) dan hujan deras singkat.

Fenomena ini sering terjadi di kota besar seperti Surabaya, Jakarta, dan sekitarnya pada siang–sore hari.
""")

st.caption("📌 Peta ini bersifat edukatif. Visualisasi lanjutan akan memanfaatkan citra suhu permukaan (LST) atau radar cuaca.")
