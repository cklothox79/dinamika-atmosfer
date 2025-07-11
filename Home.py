import streamlit as st
import requests
import pandas as pd
import re

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# ========================================
# ✅ Real-Time ENSO dari PSL NOAA
@st.cache_data
def fetch_enso():
    try:
        url = "https://psl.noaa.gov/data/correlation/oni.data"
        r = requests.get(url, timeout=10)
        lines = r.text.strip().split('\n')
        data = []
        for line in lines:
            if line[:4].isdigit():
                year = int(line[:4])
                monthly_vals = [float(x) for x in line[5:].split()]
                for i, val in enumerate(monthly_vals):
                    data.append((year, i + 1, val))
        if not data:
            return None
        _, _, latest_oni = data[-1]
        if latest_oni >= 0.5:
            return "El Niño"
        elif latest_oni <= -0.5:
            return "La Niña"
        else:
            return "Netral"
    except:
        return None

# ✅ Real-Time IOD
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

# ========================================
# Input kota
st.markdown("### 📍 Masukkan Nama Kota")
kota = st.text_input("Contoh: Malang, Bandung, Jakarta", key="lokasi_input")

# ========================================
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

# ========================================
# Dampak jika kota diisi
if kota:
    st.markdown("---")
    st.markdown(f"### 📌 Dampak Skala Atmosfer terhadap Kota: `{kota}`")
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
        st.markdown("⚪ IOD Netral — tidak berdampak signifikan saat ini.")

# ========================================
# Edukasi dan Animasi
with st.expander("🎓 Penjelasan Skala Atmosfer", expanded=True):
    st.markdown("### 🌀 ENSO (El Niño–Southern Oscillation)")
    st.markdown("- **El Niño**: Pemanasan suhu laut Pasifik → kekeringan di Indonesia.")
    st.markdown("- **La Niña**: Pendinginan suhu laut Pasifik → curah hujan meningkat.")

    st.markdown("### 🌊 IOD (Indian Ocean Dipole)")
    st.markdown("- **IOD Positif**: Samudra Hindia barat lebih hangat → Indonesia lebih kering.")
    st.markdown("- **IOD Negatif**: Samudra Hindia timur lebih hangat → curah hujan meningkat.")

    st.markdown("### ☁️ MJO (Madden-Julian Oscillation)")
    st.markdown("- Gelombang konveksi tropis → memengaruhi hujan mingguan.")

    st.markdown("### 🌐 Gelombang Kelvin dan Rossby")
    st.markdown("- Gelombang atmosfer skala besar → memengaruhi tekanan & hujan.")

st.image(
    "https://www.bom.gov.au/archive/oceanography/ocean_analyse/IDYOC002/IDYOC002.gif",
    use_container_width=True,
    caption="🌊 Animasi ENSO - Sumber: BOM Australia"
)
