import streamlit as st
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Skala Atmosfer Aktif", layout="wide")
st.title("🌀 SKALA ATMOSFER AKTIF SAAT INI")
st.markdown("**Editor: Ferri Kusuma (STMKG/M8TB_14.22.0003)**")

col1, col2 = st.columns([1.5, 1.0])

with col1:
    st.markdown("### 🏩 Masukkan Nama Kota")
    st.markdown("_Atau klik lokasi di peta untuk deteksi otomatis_ ✨")

    if 'kota' not in st.session_state:
        st.session_state.kota = "Malang"

    geolocator = Nominatim(user_agent="geoapi")

    # Peta Interaktif (klik)
    m = folium.Map(location=[-7.98, 112.63], zoom_start=5)
    folium.Marker(location=[-7.98, 112.63], tooltip="Klik lokasi").add_to(m)
    folium.LatLngPopup().add_to(m)
    output = st_folium(m, height=350, width=700, returned_objects=["last_clicked"])

    # Deteksi Klik
    if output["last_clicked"] is not None:
        lat_click = output["last_clicked"]["lat"]
        lon_click = output["last_clicked"]["lng"]
        try:
            loc = geolocator.reverse((lat_click, lon_click), timeout=10)
            kota_dari_klik = loc.raw.get("address", {}).get("city", None) or loc.raw.get("address", {}).get("town", None)
            if kota_dari_klik:
                st.session_state.kota = kota_dari_klik.title()
        except GeocoderTimedOut:
            pass

    # Input manual kota (sinkron ke session)
    kota = st.text_input(" ", st.session_state.kota).strip().title()
    st.session_state.kota = kota

    if kota:
        st.markdown(f"📍 **Kota yang dipilih:** `{kota}`")

        location = geolocator.geocode(kota)
        if location:
            lat, lon = location.latitude, location.longitude

            # 🌐 Informasi Lokasi Tambahan
            reverse_loc = geolocator.reverse((lat, lon), language='id')
            address = reverse_loc.raw.get("address", {})
            provinsi = address.get("state", "Tidak Diketahui")
            negara = address.get("country", "Tidak Diketahui")

            st.markdown("### 🧭 Informasi Lokasi Lengkap")
            st.markdown(f"- 🏙️ **Provinsi:** `{provinsi}`")
            st.markdown(f"- 🗺️ **Negara:** `{negara}`")
            st.markdown(f"- 📍 **Koordinat:** `{lat:.3f}, {lon:.3f}`")
            st.markdown(f"- 🔗 [Lihat di Google Maps](https://www.google.com/maps?q={lat},{lon})")

            st.markdown("### 🌍 Indeks Atmosfer Global Saat Ini")
            enso_index, iod_index = -0.7, -0.4
            enso_status = "La Niña" if enso_index <= -0.5 else "El Niño" if enso_index >= 0.5 else "Netral"
            iod_status = "Negatif" if iod_index <= -0.4 else "Positif" if iod_index >= 0.4 else "Netral"
            st.markdown(f"#### 🌀 ENSO Index: `{enso_index}` → **{enso_status}**")
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
            st.error("❗ Kota tidak ditemukan.")
    else:
        st.warning("Silakan masukkan nama kota atau klik lokasi pada peta.")

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
