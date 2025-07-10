import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Peta Dampak Skala Atmosfer", layout="wide")
st.title("🗺️ Peta Dampak Skala Atmosfer")

st.markdown("""
Halaman ini menampilkan **wilayah-wilayah Indonesia** yang sedang dipengaruhi oleh fenomena atmosfer besar seperti **ENSO, IOD, dan MJO** berdasarkan data terkini atau simulasi.

🧭 Warna wilayah:
- 🔴 El Niño → Wilayah terdampak kekeringan
- 🔵 La Niña → Wilayah terdampak hujan ekstrem
- 🟠 IOD Positif → Pengeringan barat Indonesia
- 🟢 IOD Negatif → Peningkatan hujan di Sumatra/Jawa
- ⚪ MJO Aktif → Hujan temporer skala mingguan
""")

# =========================
# Simulasi Titik Dampak
# =========================
data_dampak = [
    {"nama": "Nusa Tenggara Timur", "lat": -9.3, "lon": 124.0, "skala": "El Niño", "warna": "red"},
    {"nama": "Sumatra Barat", "lat": -0.9, "lon": 100.3, "skala": "La Niña", "warna": "blue"},
    {"nama": "Aceh", "lat": 4.6, "lon": 96.8, "skala": "IOD Positif", "warna": "orange"},
    {"nama": "Jawa Barat", "lat": -6.9, "lon": 107.6, "skala": "IOD Negatif", "warna": "green"},
    {"nama": "Papua", "lat": -4.2, "lon": 138.0, "skala": "MJO Aktif", "warna": "white"},
]

# =========================
# Tampilkan Peta
# =========================
m = folium.Map(location=[-2.5, 118.0], zoom_start=5)

for d in data_dampak:
    folium.CircleMarker(
        location=[d["lat"], d["lon"]],
        radius=10,
        popup=f"{d['nama']} ({d['skala']})",
        color=d["warna"],
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

st_data = st_folium(m, width=900, height=550)
