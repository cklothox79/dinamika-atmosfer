# File: pages/1_Skala_Global.py

import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Skala Global", layout="wide")
st.title("🌐 Skala Atmosfer Global")

st.markdown("## 🌦️ El Niño dan La Niña")

st.markdown("""
**El Niño** terjadi saat suhu permukaan laut di wilayah tengah dan timur Samudra Pasifik (terutama area Nino 3.4) menghangat secara signifikan. Hal ini **melemahkan pertumbuhan awan hujan di Indonesia**, sehingga berpotensi menyebabkan kekeringan.

Sebaliknya, **La Niña** adalah kondisi ketika suhu permukaan laut di wilayah yang sama lebih **dingin dari normal**, sehingga **meningkatkan curah hujan** di wilayah Indonesia, khususnya bagian tengah dan timur.

🔵 **Area Nino 3.4** adalah zona penting yang berada di Samudra Pasifik Tengah (5°LU – 5°LS dan 170°BB – 120°BB), digunakan untuk memantau dan mengklasifikasikan ENSO.
""")

st.markdown("### 📊 Visualisasi Perbandingan El Niño dan La Niña")
st.image(
    "https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/el_nino_vs_la_nina.png",
    caption="Perbandingan kondisi atmosfer dan laut pada El Niño vs La Niña.",
    use_container_width=True
)

st.markdown("---")
st.markdown("## 📍 Lokasi Area Nino 3.4")

st.markdown("Berikut ini lokasi area Nino 3.4 secara spasial:")

# Koordinat area Nino 3.4 (5°LU–5°LS dan 170°BB–120°BB)
map_center = [0, -150]  # tengah Samudra Pasifik
m = folium.Map(location=map_center, zoom_start=3, tiles="cartodbpositron")

# Tambahkan area persegi panjang Nino 3.4
folium.Rectangle(
    bounds=[[5, -170], [-5, -120]],
    color="red",
    fill=True,
    fill_opacity=0.3,
    tooltip="Area Nino 3.4\n(5°LU – 5°LS, 170°BB – 120°BB)"
).add_to(m)

st_folium(m, width=700, height=450)

st.caption("🗺️ Peta area Nino 3.4 di Samudra Pasifik untuk klasifikasi ENSO (El Niño dan La Niña).")
