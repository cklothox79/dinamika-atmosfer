import streamlit as st
import requests
import re

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# Fungsi ambil data ENSO dari NOAA: oni.ascii.txt
@st.cache_data
def fetch_enso():
    try:
        url = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
        r = requests.get(url, timeout=10)
        lines = r.text.strip().split('\n')
        data = []
        for line in lines:
            parts = line.split()
            if len(parts) == 3 and parts[0].isdigit():
                y, m, val = int(parts[0]), int(parts[1]), float(parts[2])
                data.append((y, m, val))
        if not data:
            return None
        _, _, oni_val = data[-1]
        if oni_val >= 0.5:
            return "El Niño"
        elif oni_val <= -0.5:
            return "La Niña"
        else:
            return "Netral"
    except:
        return None

# Fungsi ambil data IOD dari halaman resmi BOM
@st.cache_data
def fetch_iod():
    try:
        url = "https://www.bom.gov.au/climate/iod/"
        r = requests.get(url, timeout=10)
        match = re.search(r"IOD index.*?([-]?\d+\.\d+)", r.text)
        if not match:
            return "Netral"
        iod_val = float(match.group(1))
        return "IOD Positif" if iod_val >= 0.4 else "IOD Negatif" if iod_val <= -0.4 else "Netral"
    except:
        return None

# Input kota
st.markdown("### 📍 Masukkan Nama Kota")
kota = st.text_input("Contoh: Malang, Bandung, Jakarta", key="lokasi_input")

# Status Global
st.markdown("### 🌊 Status Global: ENSO & IOD (Real‑Time)")
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

# Dampak skala terhadap kota jika kota diinput
if kota:
    st.markdown("---")
    st.markdown(f"### 📌 Dampak Skala Atmosfer terhadap Kota: `{kota}`")
    if fase_enso == "El Niño":
        st.markdown("🔴 **El Niño** menyebabkan pengurangan hujan → potensi suhu panas dan kekeringan.")
    elif fase_enso == "La Niña":
        st.markdown("🔵 **La Niña** meningkatkan potensi hujan tinggi dan banjir lokal.")
    else:
        st.markdown("⚪ ENSO Netral — faktor MJO dan lokal lebih dominan.")
    if fase_iod == "IOD Positif":
        st.markdown("🟠 **IOD Positif** → cuaca lebih kering di barat Indonesia.")
    elif fase_iod == "IOD Negatif":
        st.markdown("🔵 **IOD Negatif** → peningkatan hujan di barat/selatan Indonesia.")
    else:
        st.markdown("⚪ IOD Netral — tidak berdampak signifikan saat ini.")

# Edukasi skala atmosfer
with st.expander("🎓 Penjelasan Skala Atmosfer (Klik untuk lihat)", expanded=True):
    st.markdown("### 🌀 ENSO (El Niño–Southern Oscillation)")
    st.markdown("- El Niño: laut Pasifik hangat → curah hujan turun.")
    st.markdown("- La Niña: laut Pasifik dingin → curah hujan meningkat.")
    st.markdown("### 🌊 IOD (Indian Ocean Dipole)")
    st.markdown("- IOD Positif: barat Hindia hangat → musim kering.")
    st.markdown("- IOD Negatif: timur Hindia hangat → curah hujan meningkat.")
    st.markdown("### ☁️ MJO")
    st.markdown("- Gelombang konveksi tropis yang memengaruhi hujan dalam 1–2 minggu ke depan.")
    st.markdown("### 🌐 Gelombang Kelvin & Rossby")
    st.markdown("- Gelombang atmosfer tropis yang pengaruhi tekanan, angin, dan curah hujan.")

# Animasi ENSO
st.markdown("### 🌊 Animasi ENSO - Sumber: BOM Australia")
st.image("https://www.bom.gov.au/archive/oceanography/ocean_analyse/IDYOC002/IDYOC002.gif",
         use_container_width=True)
