import streamlit as st
import requests
import re
import pandas as pd

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# =============================
# Fungsi Data ENSO (dari GitHub CSV)
# =============================
@st.cache_data
def fetch_enso():
    try:
        url = "https://raw.githubusercontent.com/hadiningrat29/dinamika-atmosfer-data/main/oni_realtime.csv"
        df = pd.read_csv(url)
        if df.empty:
            return "Netral"
        last_val = df["anomalia"].dropna().iloc[-1]
        if last_val >= 0.5:
            return "El Niño"
        elif last_val <= -0.5:
            return "La Niña"
        else:
            return "Netral"
    except:
        return "Netral"

# =============================
# Fungsi Data IOD (web scraping BOM)
# =============================
@st.cache_data
def fetch_iod():
    try:
        url = "https://www.bom.gov.au/climate/iod/"
        r = requests.get(url, timeout=10)
        m = re.search(r"IOD index.*?([-]?\d+\.\d+)", r.text)
        if not m:
            return "Netral"
        iod_val = float(m.group(1))
        if iod_val >= 0.4:
            return "IOD Positif"
        elif iod_val <= -0.4:
            return "IOD Negatif"
        else:
            return "Netral"
    except:
        return "Netral"

# =============================
# Fungsi Data MJO
# =============================
@st.cache_data
def fetch_mjo():
    try:
        url = "https://www.bom.gov.au/climate/mjo/graphics/rmm.74toRealtime.txt"
        r = requests.get(url, timeout=10)
        lines = r.text.strip().split('\n')
        data = [line for line in lines if line and len(line.split()) >= 5]
        if not data:
            return "Tidak aktif"
        last = data[-1].split()
        phase = int(float(last[3]))
        amp = float(last[4])
        if amp < 1.0:
            return "Tidak aktif"
        return f"Fase {phase}"
    except:
        return "Tidak aktif"

# =============================
# Input Lokasi
# =============================
st.markdown("### 📍 Masukkan Nama Kota")
kota = st.text_input("Contoh: Malang, Bandung, Jakarta", key="lokasi_input")

if kota:
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # =============================
    # Skala Global: ENSO & IOD
    # =============================
    with col1:
        st.subheader("🌐 Skala Global")
        fase_enso = fetch_enso()
        fase_iod = fetch_iod()

        if isinstance(fase_enso, str):
            st.success(f"🔴 Fase ENSO: **{fase_enso}**")
        else:
            st.warning("❌ Gagal memuat data ENSO.")

        if isinstance(fase_iod, str):
            st.success(f"🟠 Fase IOD: **{fase_iod}**")
        else:
            st.warning("❌ Gagal memuat data IOD.")

    # =============================
    # Skala Regional: MJO (sementara)
    # =============================
    with col2:
        st.subheader("🗺️ Skala Regional")
        fase_mjo = fetch_mjo()
        if isinstance(fase_mjo, str):
            st.success(f"☁️ MJO Saat Ini: **{fase_mjo}**")
        else:
            st.warning("⚠️ Gagal memuat data MJO.")

        st.info("📡 Data Rossby dan ITCZ akan segera tersedia.")

    # =============================
    # Skala Lokal
    # =============================
    with col3:
        st.subheader(f"🏙️ Skala Lokal: {kota.title()}")
        if fase_enso == "El Niño":
            st.markdown("🔴 El Niño: potensi kekeringan tinggi.")
        elif fase_enso == "La Niña":
            st.markdown("🔵 La Niña: potensi hujan tinggi / banjir.")
        else:
            st.markdown("⚪ ENSO Netral — faktor lokal lebih berperan.")

        if fase_iod == "IOD Positif":
            st.markdown("🟠 IOD Positif: cuaca lebih kering di barat.")
        elif fase_iod == "IOD Negatif":
            st.markdown("🔵 IOD Negatif: potensi hujan meningkat.")
        else:
            st.markdown("🟣 IOD Netral — tidak berdampak signifikan.")

# =============================
# Footer Info
# =============================
st.markdown("---")
st.caption("Versi awal pembagian skala global, regional, dan lokal. Data regional akan ditambahkan lebih lanjut.")
