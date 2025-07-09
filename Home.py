# File: Home.py

import streamlit as st
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Skala Atmosfer Aktif", layout="wide")
st.title("🌀 **SKALA ATMOSFER AKTIF SAAT INI**")
st.markdown("**Editor: Ferri Kusuma (STMKG/M8TB_14.22.0003)**")

col1, col2 = st.columns([1.5, 1.0])

with col1:
    st.markdown("### 🏩 Masukkan Nama Kota")
    st.markdown("_Atau klik lokasi di peta untuk deteksi otomatis_ ✨")

    kota_input = st.text_input(" ", "Malang").strip().title()
    geolocator = Nominatim(user_agent="geoapi")

    # Inisialisasi lat-lon dari klik peta
    if 'clicked_latlon' not in st.session_state:
        st.session_state.clicked_latlon = None

    kota = kota_input
    location = None
    lat, lon = -7.98, 112.63  # default Malang

    if kota_input:
        try:
            location = geolocator.geocode(kota_input)
            lat, lon = location.latitude, location.longitude
        except GeocoderTimedOut:
            st.warning("🌐 Tidak dapat mengakses layanan geolokasi. Silakan lanjut dengan input manual.")
        except:
            location = None
    elif st.session_state.clicked_latlon:
        lat, lon = st.session_state.clicked_latlon
        try:
            location = geolocator.reverse((lat, lon), timeout=10)
            kota = location.raw.get('address', {}).get('city', 'Tidak Dikenali')
        except:
            kota = "Tidak Dikenali"

    if kota:
        st.markdown(f"📍 **Kota yang dipilih:** `{kota}`")

    # PETA INTERAKTIF
    st.markdown("### 🗌 Klik Lokasi Kota di Peta")
    m = folium.Map(location=[lat, lon], zoom_start=5)
    folium.Marker([lat, lon], tooltip=kota, icon=folium.Icon(color='blue')).add_to(m)
    folium.Circle(radius=300000, location=[lat, lon], color="cyan", fill=True, fill_opacity=0.1).add_to(m)
    map_data = st_folium(m, height=350, width=700)

    # Simpan klik
    if map_data.get("last_clicked"):
        st.session_state.clicked_latlon = (
            map_data["last_clicked"]["lat"],
            map_data["last_clicked"]["lng"]
        )

    # ENSO, IOD, MJO (Dummy sementara)
    st.markdown("### 🌍 Indeks Atmosfer Global Saat Ini")
    enso_index = -0.6  # dari NOAA misal
    iod_index = -0.3   # dari BOM
    mjo_phase = 4
    mjo_amp = 1.3

    enso_status = "La Niña" if enso_index <= -0.5 else "El Niño" if enso_index >= 0.5 else "Netral"
    iod_status = "Negatif" if iod_index <= -0.4 else "Positif" if iod_index >= 0.4 else "Netral"
    mjo_status = f"Fase {mjo_phase} (Aktif)" if mjo_amp >= 1 else "Lemah / Tidak Aktif"

    st.markdown(f"#### 🌀 ENSO Index: `{enso_index}` → **{enso_status}**")
    st.markdown(f"#### 🌊 IOD Index: `{iod_index}` → **{iod_status}**")
    st.markdown(f"#### 🌧️ MJO: `{mjo_amp}` → **{mjo_status}**")

    # Durasi Fenomena
    st.markdown("### ⏱️ Durasi Skala Atmosfer Aktif")
    skala_durasi = {
        "MJO Fase 4": ("2025-07-01", "2025-07-10"),
        "IOD Negatif": ("2025-06-20", "2025-08-15"),
        "La Niña": ("2025-06-15", "2025-08-31"),
        "Gelombang Kelvin": ("2025-07-05", "2025-07-08"),
    }
    for skala, (mulai, selesai) in skala_durasi.items():
        mulai_fmt = datetime.strptime(mulai, "%Y-%m-%d").strftime("%d %B %Y")
        selesai_fmt = datetime.strptime(selesai, "%Y-%m-%d").strftime("%d %B %Y")
        st.markdown(f"- ⏳ **{skala}** → *{mulai_fmt} s.d. {selesai_fmt}*")

    st.markdown("### 📈 Grafik Timeline Skala Atmosfer")
    df_durasi = [
        {"Skala": nama, "Mulai": datetime.strptime(start, "%Y-%m-%d"), "Selesai": datetime.strptime(end, "%Y-%m-%d")}
        for nama, (start, end) in skala_durasi.items()
    ]
    df = pd.DataFrame(df_durasi)
    fig = px.timeline(df, x_start="Mulai", x_end="Selesai", y="Skala", color="Skala",
                      title="📈 Timeline Pengaruh Skala Atmosfer")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=40, b=40),
        xaxis_title="Tanggal",
        yaxis_title="Skala Atmosfer",
        plot_bgcolor="#f9f9f9"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    wilayah_dipengaruhi = ["Malang", "Surabaya", "Sidoarjo", "Jember"]
    if kota in wilayah_dipengaruhi:
        st.success("✅ Wilayah ini sedang dipengaruhi oleh:")
        st.markdown("""
        - 🌐 **MJO aktif fase 4**
        - 🌊 **IOD negatif**
        - 💧 **La Niña ringan**
        - 🌬️ **Kelvin Wave**
        """)
    else:
        st.info("ℹ️ Tidak ada skala atmosfer signifikan yang terdeteksi saat ini.")

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
