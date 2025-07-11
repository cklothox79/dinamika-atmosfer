import streamlit as st
import requests
import re

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# ========================================
@st.cache_data
def fetch_enso():
    try:
        url = "https://ftp.cpc.ncep.noaa.gov/htdocs/data/indices/oni.ascii.txt"
        r = requests.get(url, timeout=10)
        lines = r.text.strip().split('\n')
        data = []
        for line in lines:
            parts = line.split()
            if len(parts) == 3 and parts[0].isdigit():
                year, month, val = int(parts[0]), int(parts[1]), float(parts[2])
                data.append((year, month, val))
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

# Input kota
st.markdown("### 📍 Masukkan Nama Kota")
kota = st.text_input("Contoh: Malang, Bandung, Jakarta", key="lokasi_input")

# ===========================
# 🌐 Skala Global
# ===========================
st.markdown("### 🌐 Status Global: ENSO & IOD (Real‑Time)")
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
# 🗺️ Skala Regional
# ===========================
st.markdown("### 🗺️ Status Skala Regional")
st.info("Visualisasi dan analisis regional akan tersedia di halaman ini.")

# ===========================
# 🏙️ Skala Lokal
# ===========================
st.markdown("### 🏙️ Dampak Skala Atmosfer terhadap Kota")
if kota:
    st.markdown(f"📌 Kota: `{kota}`")
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
else:
    st.markdown("⌛ Masukkan nama kota untuk melihat dampaknya.")
