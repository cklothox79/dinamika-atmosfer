# File: pages/2_skala_regional/2_Visualisasi_BBLJ.py

import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="Visualisasi BBLJ", layout="wide")
st.title("💨 Belokan Angin Lapisan Bawah (BBLJ)")

st.markdown("""
BBLJ (Belokan Angin Lapisan Bawah) adalah fenomena atmosfer regional yang terjadi akibat perbedaan tekanan dan topografi,
menyebabkan angin berbelok dan menciptakan zona konvergensi yang sering memicu hujan lokal.

🗓️ **Tanggal Pengamatan**: {today}
""".format(today=datetime.today().strftime("%d %B %Y")))

# Perkiraan posisi BBLJ aktif (simulasi/dummy)
bblj_area = folium.Map(location=[-3.5, 120], zoom_start=5, tiles="cartodbpositron")
folium.Circle(location=[-3.5, 120], radius=300000, color="blue",
              fill=True, fill_opacity=0.3, tooltip="Zona Potensi BBLJ Aktif").add_to(bblj_area)
folium.Marker([-3.5, 120], popup="Wilayah terdampak BBLJ", icon=folium.Icon(color="blue")).add_to(bblj_area)

st.markdown("### 🗺️ Peta Zona Potensial BBLJ")
st_data = st_folium(bblj_area, width=700, height=500)

st.markdown("### ℹ️ Penjelasan Tambahan")
st.markdown("""
BBLJ umumnya diamati melalui data vektor angin lapisan rendah (925–850 hPa) dan muncul saat ada perlambatan angin
akibat tekanan lokal/topografi. Terutama berdampak di wilayah pesisir atau lembah pegunungan.
""")

st.caption("📌 Peta berbasis simulasi. Visualisasi lanjutan akan terhubung dengan dataset angin GFS/ERA5 di pembaruan mendatang.")
