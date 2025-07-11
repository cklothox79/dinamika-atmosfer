import streamlit as st
import requests
import re

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

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

@st.cache_data
def fetch_iod():
    try:
        url = "https://www.bom.gov.au/climate/iod/"
        r = requests.get(url, timeout=10)
        m = re.search(r"IOD index.*?([-]?\d+\.\d+)", r.text)
        if not m:
            return "Netral"
        iod = float(m.group(1))
        return ("IOD Positif" if iod>=0.4 else "IOD Negatif" if iod<=-0.4 else "Netral")
    except:
        return None

st.markdown("### 📍 Masukkan Nama Kota")
kota = st.text_input("Contoh: Malang, Bandung, Jakarta")

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
        st.markdown("⚪ IOD Netral — tidak berdampak signifikan.")

with st.expander("🎓 Penjelasan Skala Atmosfer", expanded=True):
    st.markdown("### 🌀 ENSO (El Niño–Southern Oscillation)")
    st.markdown("- El Niño: laut Pasifik timur-tengah lebih hangat → pengurangan hujan.")
    st.markdown("- La Niña: laut lebih dingin → hujan melimpah.")
    st.markdown("### 🌊 IOD (Indian Ocean Dipole)")
    st.markdown("- IOD Positif: barat Hindia hangat → musim kemarau lebih kering.")
    st.markdown("- IOD Negatif: timur Hindia hangat → hujan meningkat.")
    st.markdown("### ☁️ MJO & Gelombang Kelvin-Rossby")
    st.markdown("- Didominasi dinamika lokal dan tropis jangka pendek.")

st.markdown("### 🌊 Visual Pendukung (jika perlu grafik atau video)")
