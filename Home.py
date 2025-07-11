import streamlit as st
import requests
import re

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# ================================
# Ambil Data ENSO (ONI) via oni.ascii.txt dari NOAA
# ================================
@st.cache_data
def fetch_enso():
    try:
        url = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
        r = requests.get(url, timeout=10)
        lines = r.text.strip().split('\n')
        data = []
        for line in lines:
            parts = line.split()
            # format: YYYY MM ONI
            if len(parts) == 3 and parts[0].isdigit():
                try:
                    year, month, val = int(parts[0]), int(parts[1]), float(parts[2])
                except:
                    continue
                data.append((year, month, val))
        if not data:
            return None
        y, m, oni = data[-1]
        if oni >= 0.5:
            return "El Niño"
        elif oni <= -0.5:
            return "La Niña"
        else:
            return "Netral"
    except:
        return None

# ================================
# Ambil Data IOD dari halaman BOM Outlook
# ================================
@st.cache_data
def fetch_iod():
    try:
        url = "https://www.bom.gov.au/climate/iod/"
        r = requests.get(url, timeout=10)
        text = r.text
        # cari pola seperti "IOD index ... −0.12 °C"
        match = re.search(r"IOD index.*?([-]?\d+\.\d+)", text)
        if not match:
            return "Netral"
        iod_val = float(match.group(1))
        if iod_val >= 0.4:
            return "IOD Positif"
        elif iod_val <= -0.4:
            return "IOD Negatif"
        else:
            return "Netral"
    except:
        return None

# ================================
# Input Lokasi
# ================================
st.markdown("### 📍 Masukkan Nama Kota")
kota = st.text_input("Contoh: Malang, Bandung, Jakarta", key="lokasi_input")

# ================================
# Status ENSO & IOD Real‑Time
# ================================
st.markdown("### 🌊 Status Global: ENSO & IOD (Real-Time)")

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

# ================================
# Dampak Skala terhadap Kota
# ================================
if kota:
    st.markdown("---")
    st.markdown(f"### 📌 Dampak Skala Atmosfer terhadap Kota: `{kota}`")
    # Dampak ENSO
    if fase_enso == "El Niño":
        st.markdown("🔴 **El Niño** dapat menurunkan curah hujan di Indonesia, termasuk kota ini. Waspadai kekeringan dan suhu tinggi.")
    elif fase_enso == "La Niña":
        st.markdown("🔵 **La Niña** meningkatkan potensi hujan tinggi dan risiko banjir.")
    else:
        st.markdown("⚪ **ENSO Netral**, faktor lain seperti MJO dominan mengatur hujan lokal.")
    # Dampak IOD
    if fase_iod == "IOD Positif":
        st.markdown("🟠 **IOD Positif** cenderung menyebabkan cuaca lebih kering di wilayah barat Indonesia.")
    elif fase_iod == "IOD Negatif":
        st.markdown("🔵 **IOD Negatif** meningkatkan potensi hujan di barat dan selatan Indonesia.")
    else:
        st.markdown("⚪ **IOD Netral**, sementara tidak berdampak dominan.")

# ================================
# Penjelasan Skala Atmosfer
# ================================
with st.expander("🎓 Penjelasan Skala Atmosfer (Klik untuk lihat)", expanded=True):
    st.markdown("### 🌀 ENSO (El Niño–Southern Oscillation)")
    st.markdown("- El Niño: laut Pasifik timur-tengah lebih hangat → curah hujan turun.")
    st.markdown("- La Niña: laut lebih dingin → curah hujan meningkat.")
    st.markdown("### 🌊 IOD (Indian Ocean Dipole)")
    st.markdown("- IOD Positif: barat hangat → musim kering.")
    st.markdown("- IOD Negatif: timur hangat → lebih banyak hujan.")
    st.markdown("### ☁️ MJO")
    st.markdown("- Gelombang konveksi tropis dengan pengaruh hujan 1–2 minggu ke depan.")
    st.markdown("### 🌐 Gelombang Kelvin & Rossby")
    st.markdown("- Gelombang atmosfer tropis yang memengaruhi tekanan, angin, dan hujan.")

# ================================
# Animasi ENSO (Opsional)
# ================================
st.markdown("### 🌊 Animasi ENSO - Sumber: BOM Australia")
st.image("https://www.bom.gov.au/archive/oceanography/ocean_analyse/IDYOC002/IDYOC002.gif",
         use_container_width=True)
