import streamlit as st
import requests
import pandas as pd
from io import StringIO
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Dinamika Atmosfer", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# ========================
# Fungsi Ambil Data ENSO
# ========================
def fetch_enso_data():
    url = "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        raw_text = response.text
        lines = raw_text.strip().split('\n')[1:]  # Skip header
        df = pd.read_csv(StringIO('\n'.join(lines)), delim_whitespace=True)
        last_row = df.iloc[-1]
        latest_season = last_row['SEAS']
        latest_oni = last_row.iloc[-1]

        if latest_oni >= 0.5:
            phase = "El Niño"
        elif latest_oni <= -0.5:
            phase = "La Niña"
        else:
            phase = "Netral"

        return {
            "season": latest_season,
            "oni": latest_oni,
            "phase": phase
        }
    except Exception:
        return None

# ========================
# Fungsi Ambil Data IOD
# ========================
def fetch_iod_data():
    url = "https://www.bom.gov.au/climate/enso/indices/archive/iod.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        raw = response.text
        lines = raw.strip().split('\n')
        data_lines = [line for line in lines if line and line[0].isdigit()]
        df = pd.read_csv(StringIO('\n'.join(data_lines)), delim_whitespace=True)
        last_row = df.iloc[-1]
        latest_month = f"{int(last_row['Year'])}-{int(last_row['Month']):02d}"
        latest_iod = last_row['IOD']

        if latest_iod >= 0.4:
            phase = "IOD Positif"
        elif latest_iod <= -0.4:
            phase = "IOD Negatif"
        else:
            phase = "IOD Netral"

        return {
            "date": latest_month,
            "iod": latest_iod,
            "phase": phase
        }
    except Exception:
        return None

# ================================
# Fungsi Dummy Identifikasi Skala
# ================================
def identifikasi_skala(lat, lon):
    # Nanti bisa diganti dengan logika deteksi nyata
    return {
        "ENSO": "El Niño (lemah)",
        "IOD": "Netral",
        "MJO": "Aktif (fase 3-4)",
        "Gelombang Kelvin": "Tidak Aktif",
        "Gelombang Rossby": "Aktif (fase timur)"
    }

# =============================
# PILIH LOKASI DENGAN PETA
# =============================
st.subheader("🗺️ Pilih Lokasi di Peta")

default_location = [-2.5, 117.0]  # Tengah Indonesia
m = folium.Map(location=default_location, zoom_start=5)
m.add_child(folium.LatLngPopup())  # Aktifkan klik untuk dapat latlon
map_data = st_folium(m, height=400, width=700)

clicked_latlon = None
if map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    clicked_latlon = (lat, lon)
    st.success(f"📍 Lokasi terpilih: {lat:.3f}, {lon:.3f}")

# =============================
# TAMPILKAN DATA REAL-TIME ENSO & IOD
# =============================
st.subheader("🌊 Status Global: ENSO & IOD (Real-Time)")

enso = fetch_enso_data()
iod = fetch_iod_data()

col1, col2 = st.columns(2)

with col1:
    if enso:
        st.metric(label="ENSO (ONI)", value=f"{enso['oni']:.2f}", delta=enso["phase"])
        st.caption(f"Musim: {enso['season']}")
    else:
        st.error("❌ Gagal memuat data ENSO.")

with col2:
    if iod:
        st.metric(label="IOD Index", value=f"{iod['iod']:.2f}", delta=iod["phase"])
        st.caption(f"Bulan: {iod['date']}")
    else:
        st.error("❌ Gagal memuat data IOD.")

# =============================
# IDENTIFIKASI SKALA ATMOSFER
# =============================
if clicked_latlon:
    st.subheader("🔍 Skala Atmosfer yang Aktif di Lokasi Ini")
    hasil = identifikasi_skala(lat, lon)
    for skala, status in hasil.items():
        st.write(f"- **{skala}**: {status}")
else:
    st.info("Klik lokasi di peta untuk melihat skala atmosfer yang aktif.")
