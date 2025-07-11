import streamlit as st
import requests

st.set_page_config(page_title="Dinamika Atmosfer - Halaman Utama", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# ================================
# Fungsi Ambil Data ENSO (ONI)
# ================================
@st.cache_data
def fetch_enso():
    try:
        url = "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.txt"
        r = requests.get(url)
        lines = r.text.strip().split('\n')[1:]
        data = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 13:
                year = parts[0]
                vals = parts[1:]
                for idx, val in enumerate(vals):
                    try:
                        oni = float(val)
                    except:
                        continue
                    # gunakan label bulan
                    month_labels = ['DJF','JFM','FMA','MAM','AMJ','MJJ','JJA','JAS','ASO','SON','OND','NDJ']
                    tri = month_labels[idx]
                    data.append((int(year), tri, oni))
        if not data:
            return None
        year, tri, oni = data[-1]
        if oni >= 0.5:
            return "El Niño"
        elif oni <= -0.5:
            return "La Niña"
        else:
            return "Netral"
    except:
        return None

# ================================
# Fungsi Ambil Data IOD
# ================================
@st.cache_data
def fetch_iod():
    try:
        url = "https://www.bom.gov.au/climate/enso/indices/archive/iod.txt"
        r = requests.get(url)
        lines = r.text.strip().split('\n')
        data = []
        for line in lines:
            if line and line[0].isdigit():
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        y = int(parts[0])
                        m = int(parts[1])
                        val = float(parts[2])
                    except:
                        continue
                    data.append((y, m, val))
        if not data:
            return None
        y, m, iod_val = data[-1]
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
# Status ENSO & IOD Real-Time
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
# Edukasi Skala Atmosfer
# ================================
with st.expander("🎓 Penjelasan Skala Atmosfer (Klik untuk lihat)", expanded=True):
    st.markdown("### 🌀 ENSO (El Niño–Southern Oscillation)")
    st.markdown("- **El Niño**: Pemanasan suhu laut Pasifik timur dan tengah → mengurangi hujan di Indonesia.")
    st.markdown("- **La Niña**: Pendinginan suhu laut Pasifik → meningkatkan hujan di Indonesia.")

    st.markdown("### 🌊 IOD (Indian Ocean Dipole)")
    st.markdown("- **IOD Positif**: Samudra Hindia barat lebih hangat → musim kemarau lebih kering.")
    st.markdown("- **IOD Negatif**: Samudra Hindia timur lebih hangat → hujan meningkat di wilayah barat Indonesia.")

    st.markdown("### ☁️ MJO (Madden-Julian Oscillation)")
    st.markdown("- Gelombang konveksi tropis yang berpindah dari barat ke timur.")
    st.markdown("- Memengaruhi hujan 1–2 minggu ke depan tergantung fase dan lokasi.")

    st.markdown("### 🌐 Gelombang Kelvin dan Rossby")
    st.markdown("- Gelombang atmosfer tropis yang berperan dalam pola tekanan, angin, dan hujan.")

# ================================
# Animasi ENSO (Opsional)
# ================================
st.markdown("### 🌊 Animasi ENSO - Sumber: BOM Australia")
st.image("https://www.bom.gov.au/archive/oceanography/ocean_analyse/IDYOC002/IDYOC002.gif", use_container_width=True)

# ================================
# Catatan Lokasi (Opsional)
# ================================
if kota:
    st.markdown(f"---\n📌 **Informasi ini ditujukan untuk kota: `{kota}`**\nSilakan jelajahi halaman lainnya untuk melihat pengaruh skala atmosfer terhadap kota ini.")
