import streamlit as st
import requests
import re

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# ===========================
# Fungsi Ambil Data ENSO
# ===========================
@st.cache_data
def fetch_enso():
    try:
        url = "https://psl.noaa.gov/data/correlation/oni.data"
        res = requests.get(url, timeout=10)
        lines = res.text.strip().split("\n")
        data = []
        for line in lines[1:]:
            parts = line.strip().split()
            year = parts[0]
            values = parts[1:]
            for i, val in enumerate(values):
                try:
                    data.append(float(val))
                except:
                    pass
        if not data:
            return None
        latest = data[-1]
        if latest >= 0.5:
            return "El Niño"
        elif latest <= -0.5:
            return "La Niña"
        else:
            return "Netral"
    except:
        return None

# ===========================
# Fungsi Ambil Data IOD
# ===========================
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
        return None

# ===========================
# Input Kota
# ===========================
st.markdown("### 📍 Masukkan Nama Kota")
kota = st.text_input("Contoh: Malang, Bandung, Jakarta", key="lokasi_input")

# ===========================
# Status Global
# ===========================
st.markdown("### 🌐 Status Global: ENSO & IOD (Real-Time)")
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

# ===========================
# Dampak Skala Global (ENSO + IOD)
# ===========================
if kota:
    st.markdown("---")
    st.markdown(f"### ⭐ Dampak Skala Atmosfer terhadap Kota: `{kota.lower()}`")
    if fase_enso == "El Niño":
        st.markdown("🔴 Potensi kekeringan meningkat.")
    elif fase_enso == "La Niña":
        st.markdown("🔵 Potensi hujan/banjir tinggi.")
    else:
        st.markdown("⚪ ENSO Netral — dampak lokal lebih dominan.")

    if fase_iod == "IOD Positif":
        st.markdown("🟠 Cuaca lebih kering di wilayah barat Indonesia.")
    elif fase_iod == "IOD Negatif":
        st.markdown("🔵 Hujan meningkat di barat Indonesia.")
    else:
        st.markdown("🟣 IOD Netral — tidak berdampak signifikan.")

# ===========================
# Placeholder Skala Regional
# ===========================
st.markdown("---")
st.markdown("### 🗺️ Skala Regional")
st.info("Fitur skala regional sedang dalam pengembangan.")

# ===========================
# Placeholder Skala Lokal
# ===========================
st.markdown("### 🏙️ Skala Lokal")
st.info("Fitur skala lokal akan tersedia dalam versi selanjutnya.")
