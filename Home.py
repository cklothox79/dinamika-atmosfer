import streamlit as st
import requests
import re

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# ===============================
# Fungsi Ambil Data ENSO (ONI)
# ===============================
@st.cache_data

def fetch_enso():
    try:
        url = "https://psl.noaa.gov/data/correlation/oni.data"
        r = requests.get(url, timeout=10)
        lines = r.text.splitlines()[1:]
        data = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 13 and parts[0].isdigit():
                year = int(parts[0])
                for i, val in enumerate(parts[1:]):
                    try:
                        oni = float(val)
                        data.append((year, i+1, oni))
                    except:
                        continue
        if not data:
            return None
        _, _, latest = data[-1]
        if latest >= 0.5:
            return "El Niño"
        elif latest <= -0.5:
            return "La Niña"
        else:
            return "Netral"
    except:
        return None

# ===============================
# Fungsi Ambil Data IOD
# ===============================
@st.cache_data

def fetch_iod():
    try:
        url = "https://www.bom.gov.au/climate/iod/"
        r = requests.get(url, timeout=10)
        m = re.search(r"IOD index.*?([-]?\d+\.\d+)", r.text)
        if not m:
            return "Netral"
        iod = float(m.group(1))
        return ("IOD Positif" if iod >= 0.4 else "IOD Negatif" if iod <= -0.4 else "Netral")
    except:
        return None

# ===============================
# Input Kota
# ===============================
st.markdown("### 📍 Masukkan Nama Kota")
kota = st.text_input("Contoh: Malang, Bandung, Jakarta")

# ===============================
# Status Global (ENSO & IOD)
# ===============================
st.markdown("### 🌐 Status Global Atmosfer")
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

# ===============================
# Dampak Skala Global ke Kota
# ===============================
if kota:
    st.markdown("---")
    st.markdown(f"### 📌 Dampak Skala Atmosfer terhadap Kota: `{kota}`")
    if fase_enso == "El Niño":
        st.markdown("🔴 Potensi kekeringan tinggi.")
    elif fase_enso == "La Niña":
        st.markdown("🔵 Potensi hujan/banjir tinggi.")
    else:
        st.markdown("⚪ ENSO Netral — pengaruh lokal mendominasi.")

    if fase_iod == "IOD Positif":
        st.markdown("🟠 Cuaca lebih kering di barat.")
    elif fase_iod == "IOD Negatif":
        st.markdown("🔵 Potensi hujan meningkat.")
    else:
        st.markdown("🟣 IOD Netral — tidak berdampak signifikan.")

# ===============================
# Placeholder untuk Regional & Lokal
# ===============================
st.markdown("---")
st.markdown("### 🌎 Status Regional Atmosfer (dalam pengembangan)")
st.info("📡 Data skala regional akan menampilkan MJO, angin, tekanan dll berdasarkan wilayah Asia Tenggara.")

st.markdown("---")
st.markdown("### 🏙️ Status Lokal Atmosfer (dalam pengembangan)")
st.info("🌧️ Akan memuat prakiraan berbasis kota dan pengaruh gelombang atmosfer lokal seperti konvergensi & urban effect.")

# ===============================
# Navigasi Edukasi
# ===============================
st.markdown("---")
st.markdown("📘 Lihat penjelasan lengkap di halaman **Edukasi Skala Atmosfer** pada menu samping.")
