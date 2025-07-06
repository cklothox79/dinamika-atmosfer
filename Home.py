import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Skala Atmosfer Aktif", layout="wide")
st.title("🌀 SKALA ATMOSFER AKTIF SAAT INI")
st.markdown("**Editor: Ferri Kusuma (STMKG/M8TB_14.22.0003)**")

st.markdown("### 🏙️ Masukkan Nama Kota")
kota = st.text_input(" ", "Malang").strip().title()

if kota:
    st.markdown(f"📍 **Kota yang dipilih:** `{kota}`")

    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(kota)

    if location:
        lat, lon = location.latitude, location.longitude

        st.markdown("### 🗺️ Lokasi Kota di Peta")
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon], tooltip=kota, icon=folium.Icon(color='blue')).add_to(m)
        folium.Circle(
            radius=400000,
            location=[lat, lon],
            color="cyan",
            fill=True,
            fill_opacity=0.05,
            popup="Zona pengaruh atmosfer",
        ).add_to(m)
        st_folium(m, width=700, height=450)

        # --- Contoh Deteksi Skala Atmosfer ---
        wilayah_dipengaruhi = ["Malang", "Surabaya", "Sidoarjo", "Jember"]
        if kota in wilayah_dipengaruhi:
            st.success("✅ Wilayah ini sedang dipengaruhi oleh:")
            st.markdown("""
            - 🌐 **MJO aktif fase 4** (potensi hujan meningkat)
            - 🌊 **IOD negatif** (kondisi lebih basah dari normal)
            - 💧 **La Niña ringan** (penambahan curah hujan)
            - 🌬️ **Kelvin Wave** (hujan konvektif sore-malam)
            """)
        else:
            st.info("ℹ️ Tidak ada skala atmosfer signifikan yang terdeteksi memengaruhi wilayah ini saat ini.")

        st.caption("📡 Data bersifat simulasi. Versi real-time akan terhubung ke API BMKG/NOAA.")
    else:
        st.error("❗ Kota tidak ditemukan. Mohon cek kembali ejaannya.")
else:
    st.warning("Silakan masukkan nama kota terlebih dahulu.")
