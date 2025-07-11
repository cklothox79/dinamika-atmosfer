import streamlit as st
import requests
import re
import pandas as pd

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# =============================
# Fungsi ENSO dari CSV GitHub
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
# Fungsi IOD (dari BOM)
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
# Fungsi MJO dari BOM
# =============================
@st.cache_data
def fetch_mjo():
    try:
        url = "https://www.bom.gov.au/climate/mjo/graphics/rmm.74toRealtime.txt"
        res = requests.get(url, timeout=10)
        lines = res.text.strip().split("\n")
        lines = [l for l in lines if l and l[0].isdigit()]
        last = lines[-1].split()
        phase = int(float(last[3]))
        amp = float(last[4])
        if amp >= 1.0:
            return f"Fase {phase} (aktif)"
        else:
            return "Tidak aktif"
    except:
        return "Tidak tersedia"

# =============================
# Fungsi ITCZ dari CSV GitHub
# =============================
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
# Fungsi Rossby (deskripsi)
# =============================
@st.cache_data
def fetch_rossby():
    return "sedang diamati. Gelombang ini memengaruhi cuaca 10–20 hari dan tekanan atmosfer menengah-latitud."

# =============================
# Fungsi NDVI per Kota
# =============================
@st.cache_data
def fetch_ndvi(kota):
    try:
        url = "https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/refs/heads/main/ndvi_kota_besar_indo_jun2024.csv"
        df = pd.read_csv(url)
        row = df[df['KOTA'].str.lower() == kota.lower()]
        if row.empty:
            return "🌿 NDVI tidak tersedia untuk kota ini."
        val = float(row["mean"].values[0])
        if val < 0.2:
            return f"🌿 NDVI {val:.2f} — tutupan vegetasi rendah"
        elif val < 0.4:
            return f"🌿 NDVI {val:.2f} — sedang"
        else:
            return f"🌿 NDVI {val:.2f} — hijau tinggi"
    except:
        return "🌿 NDVI tidak tersedia"

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
    with col2:
        st.subheader("🗺️ Skala Regional")
        fase_mjo = fetch_mjo()
        if isinstance(fase_mjo, str):
            st.success(f"☁️ MJO Saat Ini: **{fase_mjo}**")
        else:
            st.warning("⚠️ Gagal memuat data MJO.")

        rossby = fetch_rossby()
        itcz = fetch_itcz()

        st.info(f"🌐 Gelombang Rossby: {rossby}")
        st.info(f"🌧️ Posisi ITCZ: {itcz}")

    # =============================
    # Skala Lokal
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

        # NDVI dari CSV
        ndvi_info = fetch_ndvi(kota)
        st.markdown(ndvi_info)

# =============================
# Footer Info
# =============================
st.markdown("---")
st.caption("Versi awal pembagian skala global, regional, dan lokal. Data regional akan ditambahkan lebih lanjut.")
