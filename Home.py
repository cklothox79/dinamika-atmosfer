# File: Home.py (versi modifikasi UI)

import streamlit as st
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import folium
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Skala Atmosfer Aktif", layout="wide")

st.markdown("<h1 style='color:#1E90FF; font-weight:bold;'>🌀 SKALA ATMOSFER AKTIF SAAT INI</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:16px;'>Editor: <strong>Ferri Kusuma (STMKG/M8TB_14.22.0003)</strong></p>", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1.0])

with col1:
    st.markdown("### 🏩 Masukkan Nama Kota")
    st.markdown("_Atau klik lokasi di peta untuk deteksi otomatis_ ✨")

    kota_input = st.text_input(" ", "Malang").strip().title()
    geolocator = Nominatim(user_agent="geoapi")

    if 'clicked_latlon' not in st.session_state:
        st.session_state.clicked_latlon = None

    kota = kota_input
    location = None

    if kota_input:
        try:
            location = geolocator.geocode(kota_input)
        except:
            location = None
            st.warning("🌐 Tidak dapat mengakses layanan geolokasi. Silakan lanjut dengan input manual.")
    elif st.session_state.clicked_latlon:
        lat_click, lon_click = st.session_state.clicked_latlon
        try:
            location = geolocator.reverse((lat_click, lon_click), timeout=10)
            kota = location.raw.get('address', {}).get('city', 'Tidak Dikenali')
        except:
            location = None
            kota = "Tidak Dikenali"
            st.warning("🌐 Deteksi lokasi gagal. Silakan ketik nama kota secara manual.")

    if kota:
        st.markdown(f"📍 <b>Kota yang dipilih:</b> <code>{kota}</code>", unsafe_allow_html=True)

    if location:
        lat, lon = location.latitude, location.longitude

        st.markdown("### 🌍 Lokasi Kota di Peta")
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon], tooltip=kota, icon=folium.Icon(color='blue')).add_to(m)
        folium.Circle(radius=400000, location=[lat, lon], color="cyan", fill=True, fill_opacity=0.05).add_to(m)
        components.html(m._repr_html_(), height=350, width=700)

        # 🌍 Indeks Atmosfer
        st.markdown("### 🌍 <b>Indeks Atmosfer Global Saat Ini</b>", unsafe_allow_html=True)
        enso_index, iod_index = -0.7, -0.4
        enso_status = "La Niña" if enso_index <= -0.5 else "El Niño" if enso_index >= 0.5 else "Netral"
        iod_status = "Negatif" if iod_index <= -0.4 else "Positif" if iod_index >= 0.4 else "Netral"

        def badge(text, color):
            return f"<span style='background-color:{color}; color:white; padding:2px 8px; border-radius:8px;'>{text}</span>"

        st.markdown(f"#### 🌀 ENSO Index: `{enso_index}` → {badge(enso_status, '#007BFF' if enso_status=='La Niña' else '#FF5733' if enso_status=='El Niño' else '#AAAAAA')}", unsafe_allow_html=True)
        st.markdown(f"#### 🌊 IOD Index: `{iod_index}` → {badge(iod_status, '#0E9AA7' if iod_status=='Negatif' else '#FF9F1C' if iod_status=='Positif' else '#AAAAAA')}", unsafe_allow_html=True)

        # ⏱️ Durasi Aktif
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
            st.markdown(f"- ⏳ <b>{skala}</b> → <i>{mulai_fmt} s.d. {selesai_fmt}</i>", unsafe_allow_html=True)

        # 📈 Grafik Timeline
        st.markdown("### 📈 Grafik Timeline Skala Atmosfer")
        df_durasi = [
            {"Skala": nama, "Mulai": datetime.strptime(start, "%Y-%m-%d"), "Selesai": datetime.strptime(end, "%Y-%m-%d")}
            for nama, (start, end) in skala_durasi.items()
        ]
        df = pd.DataFrame(df_durasi)
        fig = px.timeline(df, x_start="Mulai", x_end="Selesai", y="Skala", color="Skala", hover_name="Skala",
                          title="📈 Grafik Timeline Skala Atmosfer")
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            height=450, width=950,
            margin=dict(l=10, r=10, t=40, b=40),
            xaxis_title="Tanggal", yaxis_title="Skala Atmosfer",
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

# Panel Edukasi Tetap
with col2:
    st.markdown("<h4 style='color:#444;'>📘 Penjelasan Skala Atmosfer</h4>", unsafe_allow_html=True)

    with st.expander("🌌 Skala Global"):
        st.markdown("- **El Niño / La Niña**: Gangguan suhu laut Pasifik, pengaruh besar terhadap musim hujan Indonesia.\n- **IOD**: Anomali suhu Samudra Hindia. Positif = kering, Negatif = basah.\n- **MJO**: Gangguan konvektif bergerak ke timur, memicu hujan fase tertentu.")

    with st.expander("🌍 Skala Regional"):
        st.markdown("- **Gelombang Kelvin**: Gelombang tropis memicu hujan sore-malam.\n- **BBLJ**: Belokan angin di lapisan rendah, penyebab konvergensi.\n- **ITCZ**: Zona pertemuan angin tropis, pemicu hujan lebat.")

    with st.expander("🧽 Skala Lokal"):
        st.markdown("- **Angin Lembah–Gunung**: Pola harian, memicu awan orografis.\n- **Konvergensi Mikro**: Perbedaan suhu mikro, efek pemanasan lokal.\n- **Efek Urban**: Kota panas memicu awan konvektif & hujan petir.")

    st.caption("📚 Panel informasi tetap. Cocok untuk edukasi publik & siswa cuaca.")
