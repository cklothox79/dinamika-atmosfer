import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import datetime
from geopy.geocoders import Nominatim

# Konfigurasi halaman
st.set_page_config(page_title="Skala Atmosfer Aktif", layout="wide")
st.title("🌀 SKALA ATMOSFER AKTIF SAAT INI")
st.markdown("**Editor: Ferri Kusuma (STMKG/M8TB_14.22.0003)**")

# Input nama kota
st.markdown("### 🏙️ Masukkan Nama Kota")
kota = st.text_input(" ", "Malang").strip().title()

if kota:
    st.markdown(f"📍 **Kota yang dipilih:** `{kota}`")

    # Geolokasi
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(kota)

    if location:
        lat, lon = location.latitude, location.longitude

        # Peta lokasi
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

        # Peta ditampilkan lebih ringkas (compact)
        st_folium(m, width=700, height=350)
        st.markdown("<div style='margin-top: -30px'></div>", unsafe_allow_html=True)

        # Indeks ENSO & IOD (simulasi)
        st.markdown("### 🌍 **Indeks Atmosfer Global Saat Ini**")

        enso_index = -0.7
        iod_index = -0.4

        if enso_index >= 0.5:
            enso_status = "El Niño"
            color_enso = "orange"
        elif enso_index <= -0.5:
            enso_status = "La Niña"
            color_enso = "blue"
        else:
            enso_status = "Netral"
            color_enso = "gray"

        if iod_index >= 0.4:
            iod_status = "Positif"
            color_iod = "red"
        elif iod_index <= -0.4:
            iod_status = "Negatif"
            color_iod = "blue"
        else:
            iod_status = "Netral"
            color_iod = "gray"

        st.markdown(f"""
        #### 🌀 ENSO Index: `{enso_index}` → <span style='color:{color_enso}'><b>{enso_status}</b></span>  
        #### 🌊 IOD Index: `{iod_index}` → <span style='color:{color_iod}'><b>{iod_status}</b></span>
        """, unsafe_allow_html=True)

        st.caption("📈 Nilai indeks adalah simulasi dan dapat diganti dengan data real-time (NOAA, BOM, dll).")

        st.divider()

        # Deteksi wilayah pengaruh
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

    else:
        st.error("❗ Kota tidak ditemukan. Mohon cek kembali ejaannya.")
else:
    st.warning("Silakan masukkan nama kota terlebih dahulu.")
