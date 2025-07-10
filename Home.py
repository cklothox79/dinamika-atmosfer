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

    # Inisialisasi sesi
    if 'clicked_latlon' not in st.session_state:
        st.session_state.clicked_latlon = None

    # Input nama kota
    kota_input = st.text_input("Masukkan nama kota", "Malang").strip().title()
    kota = kota_input
    location = None

    # Geocoding dari input kota
    if kota_input:
        try:
            location = geolocator.geocode(kota_input)
        except GeocoderTimedOut:
            st.warning("🌐 Waktu akses habis. Silakan coba lagi.")
        except:
            st.warning("🌐 Tidak dapat mengakses layanan geolokasi.")

    # Reverse geocoding dari klik peta
    elif st.session_state.clicked_latlon:
        lat_click, lon_click = st.session_state.clicked_latlon
        try:
            location = geolocator.reverse((lat_click, lon_click), timeout=10)
            kota = location.raw.get('address', {}).get('city', 'Tidak Dikenali')
        except:
            kota = "Tidak Dikenali"
            st.warning("🌐 Deteksi lokasi gagal.")

    if kota:
        st.markdown(f"📍 **Kota yang dipilih:** `{kota}`")

    if location:
        lat, lon = location.latitude, location.longitude

        st.markdown("### 🗌 Lokasi Kota di Peta")
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon], tooltip=kota, icon=folium.Icon(color='blue')).add_to(m)
        folium.Circle(radius=400000, location=[lat, lon], color="cyan", fill=True, fill_opacity=0.05).add_to(m)
        map_html = m._repr_html_()
        components.html(map_html, height=350, width=700)

        # ✅ Data ENSO real-time dari GitHub CSV
        def ambil_enso_github():
            try:
                url = "https://raw.githubusercontent.com/ahuang11/oni/master/oni.csv"
                df = pd.read_csv(url)
                return float(df.iloc[-1]["anom_c"])
            except:
                return None

        def ambil_iod_dummy():
            return -0.4  # bisa diganti nanti dengan real-time

        enso_index = ambil_enso_github()
        iod_index = ambil_iod_dummy()

        st.markdown("### 🌍 Indeks Atmosfer Global Saat Ini")
        if enso_index is None:
            st.error("❌ Gagal memuat data ENSO.")
        else:
            enso_status = "La Niña" if enso_index <= -0.5 else "El Niño" if enso_index >= 0.5 else "Netral"
            st.markdown(f"#### 🌀 ENSO Index: `{enso_index:.2f}` → **{enso_status}**")

        iod_status = "Negatif" if iod_index <= -0.4 else "Positif" if iod_index >= 0.4 else "Netral"
        st.markdown(f"#### 🌊 IOD Index: `{iod_index}` → **{iod_status}**")

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
                          title="📈 Grafik Timeline Skala Atmosfer")
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            height=450,
            width=950,
            margin=dict(l=10, r=10, t=40, b=40),
            xaxis_title="Tanggal",
            yaxis_title="Skala Atmosfer",
            plot_bgcolor="#f9f9f9"
        )
        st.plotly_chart(fig, use_container_width=False)

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
    else:
        st.warning("⚠️ Data lokasi belum tersedia. Silakan isi nama kota atau klik lokasi di peta.")

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
