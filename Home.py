import streamlit as st
import requests
import re
import pandas as pd

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# =============================
# Fungsi Data IOD
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
# Fungsi Data ENSO (dari GitHub CSV)
# =============================
@st.cache_data
def fetch_enso():
    try:
        url = "https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/oni_realtime.csv"
        df = pd.read_csv(url)
        last = df["anomalia"].dropna().iloc[-1]
        if last >= 0.5:
            return "El Niño"
        elif last <= -0.5:
            return "La Niña"
        else:
            return "Netral"
    except:
        return "Netral"

# =============================
# Fungsi Data MJO (placeholder)
# =============================
@st.cache_data
def fetch_mjo():
    return "Tidak aktif"

# =============================
# Fungsi Data Rossby & ITCZ
# =============================
@st.cache_data
def fetch_rossby():
    return "Belum tersedia"

@st.cache_data
def fetch_itcz():
    try:
        url = "https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/itcz_position.csv"
        df = pd.read_csv(url)
        row = df.iloc[-1]
        return f"{row['latitude']}° (data {row['tanggal']})"
    except:
        return "Tidak tersedia"

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
    # Skala Regional: MJO, Rossby, ITCZ
    # =============================
    with col2:
        st.subheader("🗺️ Skala Regional")
        fase_mjo = fetch_mjo()
        if isinstance(fase_mjo, str):
            st.success(f"☁️ MJO Saat Ini: **{fase_mjo}**")
        else:
            st.warning("⚠️ Gagal memuat data MJO.")

        rossby = fetch_rossby()
        itcz = fetch_itcz()

        st.info(f"🌐 Gelombang Rossby: {rossby} (indeks belum tersedia)")
        st.info(f"🌧️ Posisi ITCZ: {itcz}")

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
