# File: Home.py

import streamlit as st
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import folium
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Skala Atmosfer Aktif", layout="wide")
st.title("🌀 SKALA ATMOSFER AKTIF SAAT INI")
st.markdown("**Editor: Ferri Kusuma (STMKG/M8TB_14.22.0003)**")

col1, col2 = st.columns([1.5, 1.0])

with col1:
    st.markdown("### 🏩 Masukkan Nama Kota")
    st.markdown("_Atau klik lokasi di peta untuk deteksi otomatis_ ✨")

    geolocator = Nominatim(user_agent="geoapi")
    if 'clicked_latlon' not in st.session_state:
        st.session_state.clicked_latlon = None

    kota_input = st.text_input("Masukkan nama kota", "Malang").strip().title()
    kota = kota_input
    location = None

    if kota_input:
        try:
            location = geolocator.geocode(kota_input)
        except GeocoderTimedOut:
            st.warning("🌐 Akses geolokasi timeout, coba lagi.")
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
        folium.Marker(
            [lat, lon],
            tooltip=kota,
            popup=folium.Popup("Lokasi yang Anda pilih akan dianalisis terhadap pengaruh skala atmosfer.", max_width=300),
            icon=folium.Icon(color='blue')
        ).add_to(m)

        folium.Circle(radius=400000, location=[lat, lon], color="cyan", fill=True, fill_opacity=0.05).add_to(m)

        # Tambahkan tooltip edukatif: posisi Khatulistiwa dan zona MJO aktif
        folium.Marker(
            location=[0, 110],
            icon=folium.DivIcon(html='<div style="font-size: 10pt; color: red;">🌍 Khatulistiwa</div>')
        ).add_to(m)

        folium.Circle(
            location=[-5, 120],
            radius=1000000,
            color="orange",
            fill=True,
            fill_opacity=0.2,
            tooltip="Perkiraan zona aktif MJO dan Gelombang Kelvin"
        ).add_to(m)

        components.html(m._repr_html_(), height=350, width=700)

        # Ambil ENSO dari GitHub CSV
        def ambil_enso():
            try:
                df = pd.read_csv("https://raw.githubusercontent.com/ahuang11/oni/master/oni.csv")
                return float(df.iloc[-1]["anom_c"])
            except:
                return None

        # Ambil IOD dari NOAA PSL CSV
        def ambil_iod():
            try:
                df = pd.read_csv("https://psl.noaa.gov/data/timeseries/month/data/dmi.had.long.csv", names=["date","DMI"], comment='#')
                return float(df.dropna().iloc[-1]["DMI"])
            except:
                return None

        enso_index = ambil_enso()
        iod_index = ambil_iod()

        st.markdown("### 🌍 Indeks Atmosfer Global Saat Ini")
        if enso_index is None:
            st.error("❌ Gagal memuat data ENSO.")
        else:
            enso_status = "La Niña" if enso_index <= -0.5 else "El Niño" if enso_index >= 0.5 else "Netral"
            st.markdown(f"#### 🌀 ENSO Index: `{enso_index:.2f}` → **{enso_status}**")
        if iod_index is None:
            st.error("❌ Gagal memuat data IOD.")
        else:
            iod_status = "Negatif" if iod_index <= -0.4 else "Positif" if iod_index >= 0.4 else "Netral"
            st.markdown(f"#### 🌊 IOD Index: `{iod_index:.2f}` → **{iod_status}**")

        st.markdown("### ⏱️ Durasi Skala Atmosfer Aktif")
        skala_durasi = {
            "MJO Fase Aktif": ("2025-07-01", "2025-07-10"),
            f"IOD {iod_status}": ("2025-06-20", "2025-08-15"),
            f"ENSO {enso_status}": ("2025-06-15", "2025-08-31"),
            "Gelombang Kelvin": ("2025-07-05", "2025-07-08"),
        }
        for skala, (mulai, selesai) in skala_durasi.items():
            mulai_fmt = datetime.strptime(mulai, "%Y-%m-%d").strftime("%d %B %Y")
            selesai_fmt = datetime.strptime(selesai, "%Y-%m-%d").strftime("%d %B %Y")
            st.markdown(f"- ⏳ **{skala}** → *{mulai_fmt} s.d. {selesai_fmt}*")

        st.markdown("### 📈 Grafik Timeline Skala Atmosfer")
        df2 = pd.DataFrame([
            {"Skala": nama, "Mulai": datetime.strptime(start, "%Y-%m-%d"), "Selesai": datetime.strptime(end, "%Y-%m-%d")}
            for nama, (start, end) in skala_durasi.items()
        ])
        fig = px.timeline(df2, x_start="Mulai", x_end="Selesai", y="Skala", color="Skala",
                          title="📈 Timeline Aktivitas Skala Atmosfer")
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(height=450, width=950, margin=dict(l=10,r=10,t=40,b=40))
        st.plotly_chart(fig, use_container_width=False)

        st.divider()
        wilayah = ["Malang", "Surabaya", "Sidoarjo", "Jember"]
        if kota in wilayah:
            st.success("✅ Wilayah ini sedang dipengaruhi oleh:")
            st.markdown(f"- 🌐 MJO aktif\n- 🌊 IOD {iod_status}\n- 🌀 ENSO {enso_status}\n- 🌬️ Gelombang Kelvin")
        else:
            st.info("ℹ️ Tidak ada skala atmosfer signifikan.")

    else:
        st.warning("⚠️ Data lokasi belum tersedia. Ketik kota atau klik peta.")

with col2:
    st.markdown("### 📘 Penjelasan Skala Atmosfer")
    st.markdown("#### 🌌 Skala Global")
    st.markdown("""
    - **El Niño / La Niña**: Gangguan suhu laut Pasifik, memengaruhi pola hujan Indonesia.
    - **IOD**: Perbedaan suhu laut Hindia; negatif = lebih basah di Indonesia.
    - **MJO**: Gelombang atmosfer tropis, naik dan turun memicu hujan sementara.
    """)
    st.markdown("#### 🌍 Skala Regional")
    st.markdown("""
    - **Gelombang Kelvin**: Dorongan ke atas di atmosfir tropis → hujan sore/malam.
    - **BBLJ**: Angin rendah membelok → konvergensi lokal & awan.
    - **ITCZ**: Daerah pertemuan angin tropis, tempat awan tebar.
    """)
    st.markdown("#### 🧽 Skala Lokal")
    st.markdown("""
    - **Angin Lembah–Gunung**: Pola harian, awan terbentuk di gunung.
    - **Konvergensi Mikro**: Titik lokal pemanasan & angin bertemu.
    - **Efek Urban**: Kota panas memicu hujan lokal & petir.
    """)
    st.caption("📚 Cocok untuk edukasi publik & siswa cuaca.")
