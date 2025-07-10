# File: Home.py

import streamlit as st
from datetime import datetime
from geopy.geocoders import Nominatim
import folium
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Skala Atmosfer Aktif", layout="wide")
st.title("🌀 SKALA ATMOSFER AKTIF SAAT INI")
st.markdown("**Editor: Ferri Kusuma (STMKG/M8TB_14.22.0003)**")

col1, col2 = st.columns([1.5, 1.0])

# =====================
# 📍 INPUT KOTA & PETA
# =====================
with col1:
    st.markdown("### 🏩 Masukkan Nama Kota")
    st.markdown("_Atau klik lokasi di peta untuk deteksi otomatis_ ✨")

    kota_input = st.text_input("Nama Kota", "Malang").strip().title()
    geolocator = Nominatim(user_agent="geoapi")
    kota = kota_input
    location = None

    if 'clicked_latlon' not in st.session_state:
        st.session_state.clicked_latlon = None

    if kota_input:
        try:
            location = geolocator.geocode(kota_input)
        except:
            st.warning("🌐 Tidak dapat mengakses layanan geolokasi.")

    elif st.session_state.clicked_latlon:
        lat_click, lon_click = st.session_state.clicked_latlon
        try:
            location = geolocator.reverse((lat_click, lon_click), timeout=10)
            kota = location.raw.get('address', {}).get('city', 'Tidak Dikenali')
        except:
            st.warning("🌐 Deteksi lokasi gagal.")

    if kota:
        st.markdown(f"📍 **Kota yang dipilih:** `{kota}`")

    if location:
        lat, lon = location.latitude, location.longitude
        st.markdown("### 🗺️ Lokasi Kota di Peta")
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon], tooltip=kota, icon=folium.Icon(color='blue')).add_to(m)
        folium.Circle(radius=400000, location=[lat, lon], color="cyan", fill=True, fill_opacity=0.05).add_to(m)
        components.html(m._repr_html_(), height=360, width=700)

# ==============================
# 🌍 DATA ENSO & IOD REAL-TIME
# ==============================
    def get_enso_index():
        try:
            url = "https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php"
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text()
            lines = text.splitlines()
            for line in lines[::-1]:
                if "202" in line and "-9" not in line:
                    nilai = line.strip().split()[-1]
                    return float(nilai)
        except:
            return None

    def get_iod_index():
        try:
            url = "https://www.bom.gov.au/climate/enso/"
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text()
            for line in text.splitlines():
                if "Latest IOD index value" in line:
                    for word in line.split():
                        try:
                            return float(word)
                        except:
                            continue
        except:
            return None

    enso_index = get_enso_index()
    iod_index = get_iod_index()

    enso_status = "La Niña" if enso_index is not None and enso_index <= -0.5 else "El Niño" if enso_index and enso_index >= 0.5 else "Netral"
    iod_status = "Negatif" if iod_index is not None and iod_index <= -0.4 else "Positif" if iod_index and iod_index >= 0.4 else "Netral"

    st.markdown("### 🌐 Indeks Atmosfer Global Saat Ini")
    if enso_index is not None:
        st.markdown(f"🌊 **ENSO Index:** `{enso_index}` → **{enso_status}**")
    else:
        st.warning("Gagal memuat data ENSO.")

    if iod_index is not None:
        st.markdown(f"🌊 **IOD Index:** `{iod_index}` → **{iod_status}**")
    else:
        st.warning("Gagal memuat data IOD.")

# ===================================
# ⏱️ DURASI AKTIF SKALA ATMOSFER
# ===================================
    st.markdown("### ⏱️ Durasi Skala Atmosfer Aktif")
    skala_durasi = {
        "MJO Fase 4": ("2025-07-01", "2025-07-10"),
        "IOD " + iod_status: ("2025-06-20", "2025-08-15"),
        "ENSO " + enso_status: ("2025-06-15", "2025-08-31"),
        "Gelombang Kelvin": ("2025-07-05", "2025-07-08"),
    }
    for skala, (mulai, selesai) in skala_durasi.items():
        mulai_fmt = datetime.strptime(mulai, "%Y-%m-%d").strftime("%d %B %Y")
        selesai_fmt = datetime.strptime(selesai, "%Y-%m-%d").strftime("%d %B %Y")
        st.markdown(f"- ⏳ **{skala}** → *{mulai_fmt} s.d. {selesai_fmt}*")

# =======================
# 📈 GRAFIK TIMELINE
# =======================
    st.markdown("### 📈 Grafik Timeline Skala Atmosfer")
    df_durasi = [
        {"Skala": nama, "Mulai": datetime.strptime(start, "%Y-%m-%d"), "Selesai": datetime.strptime(end, "%Y-%m-%d")}
        for nama, (start, end) in skala_durasi.items()
    ]
    df = pd.DataFrame(df_durasi)
    fig = px.timeline(df, x_start="Mulai", x_end="Selesai", y="Skala", color="Skala", title="📈 Timeline Aktivitas Skala Atmosfer")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=450, width=950, margin=dict(l=10, r=10, t=40, b=40))
    st.plotly_chart(fig, use_container_width=False)

# =====================
# ✅ DETEKSI PENGARUH
# =====================
    st.divider()
    wilayah_dipengaruhi = ["Malang", "Surabaya", "Sidoarjo", "Jember"]
    if kota in wilayah_dipengaruhi:
        st.success("✅ Wilayah ini sedang dipengaruhi oleh:")
        st.markdown(f"""
        - 🌐 **MJO aktif fase 4**
        - 🌊 **IOD {iod_status}**
        - 🌊 **ENSO {enso_status}**
        - 🌬️ **Kelvin Wave**
        """)
    else:
        st.info("ℹ️ Tidak ada skala atmosfer signifikan yang terdeteksi saat ini.")

# =====================
# 📘 PANEL PENJELASAN
# =====================
with col2:
    st.markdown("### 📘 Penjelasan Skala Atmosfer")
    st.markdown("#### 🌌 Skala Global")
    st.markdown("""
    - **El Niño / La Niña**: Gangguan suhu laut Pasifik, pengaruh besar terhadap musim hujan Indonesia.
    - **IOD**: Anomali suhu Samudra Hindia. Positif = kering, Negatif = basah.
    - **MJO**: Gangguan konvektif bergerak ke timur, memicu hujan fase tertentu.
    """)
    st.markdown("#### 🌍 Skala Regional")
    st.markdown("""
    - **Gelombang Kelvin**: Gelombang tropis memicu hujan sore-malam.
    - **BBLJ**: Belokan angin di lapisan rendah, penyebab konvergensi.
    - **ITCZ**: Zona pertemuan angin tropis, pemicu hujan lebat.
    """)
    st.markdown("#### 🧽 Skala Lokal")
    st.markdown("""
    - **Angin Lembah–Gunung**: Pola harian, memicu awan orografis.
    - **Konvergensi Mikro**: Perbedaan suhu mikro, efek pemanasan lokal.
    - **Efek Urban**: Kota panas memicu awan konvektif & hujan petir.
    """)
    st.caption("📚 Panel informasi tetap. Cocok untuk edukasi publik & siswa cuaca.")
