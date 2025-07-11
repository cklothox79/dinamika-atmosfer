import streamlit as st
import requests
import re

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# =============================
# Fungsi Data ENSO
# =============================
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
        return None

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
    # Skala Regional
    # =============================
    with col2:
        st.subheader("🗺️ Skala Regional")
        st.info("(Belum terhubung - akan memuat fenomena regional seperti MJO, Gelombang Rossby, ITCZ, dll yang relevan dengan wilayah kota)")

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
# Catatan Animasi (opsional)
# =============================
st.markdown("---")
st.markdown("### 🌊 Animasi ENSO - Sumber: BOM Australia")
st.image("https://www.bom.gov.au/archive/oceanography/ocean_analyse/IDYOC002/IDYOC002.gif", use_container_width=True)

st.caption("Versi awal pembagian skala global, regional, dan lokal. Regional akan diperluas pada tahap berikutnya.")
