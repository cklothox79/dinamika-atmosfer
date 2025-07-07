# File: pages/2_skala_regional/2_Peta_Interaktif_ITCZ_BBLJ.py

import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Peta Interaktif Regional", layout="wide")
st.title("🗺️ Peta Interaktif: ITCZ & Belokan Angin (BBLJ)")
st.markdown("**Editor: Ferri Kusuma (STMKG/M8TB_14.22.0003)**")

st.markdown("""
Peta ini menunjukkan kemungkinan **posisi ITCZ** dan **BBLJ (Belokan Angin Lapisan Bawah)** yang sedang aktif di wilayah Indonesia, berdasarkan analisis klimatologis dan posisi matahari.

> Warna garis dan simbol merupakan ilustrasi, bukan data operasional real-time.
""")

# Peta dasar Indonesia
m = folium.Map(location=[-2.5, 117], zoom_start=5, tiles="CartoDB positron")

# Ilustrasi posisi ITCZ (asumsi di sekitar ekuator ±5°LS - 5°LU)
folium.PolyLine(
    locations=[[-2, 95], [-2, 141]],
    color='orange',
    weight=4,
    tooltip="Perkiraan Jalur ITCZ"
).add_to(m)

# Belokan angin BBLJ (asumsi di selatan Jawa ke Kalimantan)
folium.PolyLine(
    locations=[[-8, 110], [0, 117]],
    color='blue',
    dash_array="10",
    tooltip="Ilustrasi Belokan Angin BBLJ"
).add_to(m)

# Penanda kota-kota utama
kota = {
    "Jakarta": [-6.2, 106.8],
    "Surabaya": [-7.25, 112.75],
    "Makassar": [-5.1, 119.5],
    "Pontianak": [0.0, 109.3],
    "Jayapura": [-2.5, 140.7]
}
for nama, loc in kota.items():
    folium.Marker(location=loc, tooltip=nama, icon=folium.Icon(color="gray")).add_to(m)

# Tampilkan peta di Streamlit
st_data = st_folium(m, width=1000, height=550)

st.caption("📝 Posisi hanya perkiraan untuk edukasi, bukan produk operasional BMKG.")
