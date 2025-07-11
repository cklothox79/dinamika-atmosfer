import streamlit as st
import requests
import pandas as pd
import re

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

@st.cache_data
def fetch_enso():
    try:
        url = "https://psl.noaa.gov/data/correlation/oni.data"
        r = requests.get(url, timeout=10)
        lines = r.text.splitlines()
        data = []
        for line in lines:
            if line and line[:4].isdigit():
                year = int(line[:4])
                vals = [float(x) for x in line[5:].split()]
                for i, val in enumerate(vals):
                    data.append((year, i+1, val))
        latest = data[-1][2]
        if latest >= 0.5: return "El Niño"
        elif latest <= -0.5: return "La Niña"
        else: return "Netral"
    except:
        return None

@st.cache_data
def fetch_iod():
    try:
        url = "https://www.bom.gov.au/climate/iod/"
        r = requests.get(url, timeout=10)
        m = re.search(r"IOD index.*?([-]?\d+\.\d+)", r.text)
        return ("IOD Positif" if (iod_val := float(m.group(1))) >= 0.4
                else "IOD Negatif" if iod_val <= -0.4 else "Netral") if m else "Netral"
    except:
        return None

st.markdown("### 📍 Masukkan Nama Kota")
kota = st.text_input("Contoh: Malang, Bandung, Jakarta")

st.markdown("### 🌊 Status Global: ENSO & IOD (Real‑Time)")
fase_enso = fetch_enso()
fase_iod = fetch_iod()

if isinstance(fase_enso, str): st.success(f"🔴 Fase ENSO: **{fase_enso}**")
else: st.warning("❌ Gagal memuat data ENSO.")

if isinstance(fase_iod, str): st.success(f"🟠 Fase IOD: **{fase_iod}**")
else: st.warning("❌ Gagal memuat data IOD.")

if kota:
    st.markdown("---")
    st.markdown(f"### 📌 Dampak Skala untuk Kota: `{kota}`")
    if fase_enso=="El Niño": st.markdown("🔴 Potensi kekeringan tinggi")
    elif fase_enso=="La Niña": st.markdown("🔵 Potensi hujan tinggi / banjir")
    else: st.markdown("⚪ ENSO Netral — pengaruh lokal lebih dominan")
    if fase_iod=="IOD Positif": st.markdown("🟠 Cuaca lebih kering di barat")
    elif fase_iod=="IOD Negatif": st.markdown("🔵 Potensi hujan meningkat")
    else: st.markdown("⚪ IOD Netral")

# 📺 Fallback visual: edukasi video atau grafik
st.markdown("### 🌊 Visual ENSO (fallback)")
st.video("https://www.youtube.com/watch?v=dzat16LMtQk")
