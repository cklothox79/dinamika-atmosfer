import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import pandas as pd
from io import StringIO

st.set_page_config(page_title="Peta Dampak Skala Atmosfer", layout="wide")
st.title("🗺️ Peta Dampak Skala Atmosfer")

st.markdown("""
Halaman ini menampilkan **wilayah-wilayah Indonesia** yang sedang dipengaruhi oleh fenomena atmosfer besar seperti **ENSO & IOD** berdasarkan data real-time.

🧭 Warna wilayah:
- 🔴 El Niño → Wilayah terdampak kekeringan
- 🔵 La Niña → Wilayah terdampak hujan ekstrem
- 🟠 IOD Positif → Pengeringan barat Indonesia
- 🟢 IOD Negatif → Peningkatan hujan di Sumatra/Jawa
""")

# =====================================
# Fungsi Ambil Data ENSO & IOD
# =====================================
def fetch_enso():
    try:
        url = "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.txt"
        res = requests.get(url)
        lines = res.text.strip().split('\n')[1:]
        df = pd.read_csv(StringIO('\n'.join(lines)), delim_whitespace=True)
        oni = df.iloc[-1].iloc[-1]
        if oni >= 0.5:
            return "El Niño"
        elif oni <= -0.5:
            return "La Niña"
        else:
            return "Netral"
    except:
        return None

def fetch_iod():
    try:
        url = "https://www.bom.gov.au/climate/enso/indices/archive/iod.txt"
        res = requests.get(url)
        lines = res.text.strip().split('\n')
        data = [l for l in lines if l and l[0].isdigit()]
        df = pd.read_csv(StringIO('\n'.join(data)), delim_whitespace=True)
        iod = df.iloc[-1]['IOD']
        if iod >= 0.4:
            return "IOD Positif"
        elif iod <= -0.4:
            return "IOD Negatif"
        else:
            return "Netral"
    except:
        return None

# =====================================
# Data Wilayah Dampak Berdasarkan Fase
# =====================================
wilayah_dampak = {
    "El Niño": [
        {"nama": "NTT", "lat": -9.3, "lon": 124.0, "warna": "red"},
        {"nama": "NTB", "lat": -8.6, "lon": 117.5, "warna": "red"},
        {"nama": "Jawa Timur", "lat": -7.5, "lon": 112.5, "warna": "red"},
    ],
    "La Niña": [
        {"nama": "Kalimantan Tengah", "lat": -1.5, "lon": 113.9, "warna": "blue"},
        {"nama": "Sulawesi Selatan", "lat": -4.0, "lon": 120.2, "warna": "blue"},
        {"nama": "Papua", "lat": -4.2, "lon": 138.0, "warna": "blue"},
    ],
    "IOD Positif": [
        {"nama": "Sumatra Barat", "lat": -0.9, "lon": 100.3, "warna": "orange"},
        {"nama": "Banten", "lat": -6.1, "lon": 106.2, "warna": "orange"},
    ],
    "IOD Negatif": [
        {"nama": "Jawa Tengah", "lat": -7.2, "lon": 110.4, "warna": "green"},
        {"nama": "Kalimantan Barat", "lat": 0.1, "lon": 109.3, "warna": "green"},
    ],
}

# =====================================
# Ambil Data Real-time
# =====================================
fase_enso = fetch_enso()
fase_iod = fetch_iod()

st.markdown(f"**Fase ENSO saat ini:** `{fase_enso or 'Gagal memuat'}`")
st.markdown(f"**Fase IOD saat ini:** `{fase_iod or 'Gagal memuat'}`")

# =====================================
# Bangun Peta Dampak
# =====================================
m = folium.Map(location=[-2.5, 118.0], zoom_start=5)

if fase_enso and fase_enso != "Netral":
    for w in wilayah_dampak.get(fase_enso, []):
        folium.CircleMarker(
            location=[w["lat"], w["lon"]],
            radius=10,
            color=w["warna"],
            fill=True,
            fill_opacity=0.7,
            popup=f"{w['nama']} ({fase_enso})"
        ).add_to(m)

if fase_iod and fase_iod != "Netral":
    for w in wilayah_dampak.get(fase_iod, []):
        folium.CircleMarker(
            location=[w["lat"], w["lon"]],
            radius=10,
            color=w["warna"],
            fill=True,
            fill_opacity=0.7,
            popup=f"{w['nama']} ({fase_iod})"
        ).add_to(m)

st_data = st_folium(m, width=900, height=550)

# =====================================
# Perkiraan Waktu Dampak
# =====================================
st.markdown("### ⏳ Perkiraan Waktu Dampak")

if fase_enso == "El Niño":
    st.info("🔴 El Niño diperkirakan berdampak dari **Agustus hingga Oktober 2025**.")
elif fase_enso == "La Niña":
    st.info("🔵 La Niña diperkirakan berlangsung antara **Juli hingga September 2025**.")
elif fase_enso == "Netral":
    st.info("ℹ️ ENSO saat ini dalam fase netral, **tidak berdampak signifikan**.")

if fase_iod == "IOD Positif":
    st.info("🟠 IOD Positif aktif sejak **Juni 2025**, berdampak hingga Agustus.")
elif fase_iod == "IOD Negatif":
    st.info("🟢 IOD Negatif terdeteksi dan dapat memengaruhi cuaca hingga **Agustus 2025**.")
elif fase_iod == "Netral":
    st.info("ℹ️ IOD saat ini dalam fase netral, **tidak berdampak signifikan**.")
