import streamlit as st
from datetime import datetime
from geopy.geocoders import Nominatim
import folium
import streamlit.components.v1 as components

st.set_page_config(page_title="Skala Atmosfer Aktif", layout="wide")
st.title("🌀 SKALA ATMOSFER AKTIF SAAT INI")
st.markdown("**Editor: Ferri Kusuma (STMKG/M8TB_14.22.0003)**")

# Input nama kota
st.markdown("### 🏙️ Masukkan Nama Kota")
kota = st.text_input(" ", "Malang").strip().title()

if kota:
    st.markdown(f"📍 **Kota yang dipilih:** `{kota}`")

    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(kota)

    if location:
        lat, lon = location.latitude, location.longitude

        st.markdown("### 🗺️ Lokasi Kota di Peta")
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon], tooltip=kota, icon=folium.Icon(color='blue')).add_to(m)
        folium.Circle(
            radius=400000,
            location=[lat, lon],
            color="cyan",
            fill=True,
            fill_opacity=0.05,
            popup="Zona pengaruh atmosfer",
        ).add_to(m)

        # Peta tampil dengan iframe agar ringkas
        map_html = m._repr_html_()
        components.html(map_html, height=350, width=700)

        # Indeks ENSO & IOD
        st.markdown("### 🌍 **Indeks Atmosfer Global Saat Ini**")

        enso_index = -0.7
        iod_index = -0.4

        if enso_index >= 0.5:
            enso_status = "El Niño"
            color_enso = "orange"
        elif enso_index <= -0.5:
            enso_status = "La Niña"
            color_enso = "blue"
        else:
            enso_status = "Netral"
            color_enso = "gray"

        if iod_index >= 0.4:
            iod_status = "Positif"
            color_iod = "red"
        elif iod_index <= -0.4:
            iod_status = "Negatif"
            color_iod = "blue"
        else:
            iod_status = "Netral"
            color_iod = "gray"

        st.markdown(f"""
        #### 🌀 ENSO Index: `{enso_index}` → <span style='color:{color_enso}'><b>{enso_status}</b></span>  
        #### 🌊 IOD Index: `{iod_index}` → <span style='color:{color_iod}'><b>{iod_status}</b></span>
        """, unsafe_allow_html=True)

        st.caption("📈 Nilai indeks adalah simulasi dan dapat diganti dengan data real-time (NOAA, BOM, dll).")

        st.divider()

        # --- DURASI SKALA ---
        st.markdown("### ⏱️ **Durasi Skala Atmosfer Aktif**")

        skala_durasi = {
            "MJO Fase 4": ("2025-07-01", "2025-07-10"),
            "IOD Negatif": ("2025-06-20", "2025-08-15"),
            "La Niña": ("2025-06-15", "2025-08-31"),
            "Gelombang Kelvin": ("2025-07-05", "2025-07-08"),
        }

        for skala, (mulai, selesai) in skala_durasi.items():
            mulai_fmt = datetime.strptime(mulai, "%Y-%m-%d").strftime("%d %B %Y")
            selesai_fmt = datetime.strptime(selesai, "%Y-%m-%d").strftime("%d %B %Y")
            st.markdown(f"- ⏳ **{skala}** → *{mulai_fmt} sampai {selesai_fmt}*")

        st.caption("🕒 Perkiraan durasi simulasi. Gunakan data resmi untuk akurasi maksimal.")

        st.divider()

        # Deteksi skala regional aktif
        wilayah_dipengaruhi = ["Malang", "Surabaya", "Sidoarjo", "Jember"]
        if kota in wilayah_dipengaruhi:
            st.success("✅ Wilayah ini sedang dipengaruhi oleh:")
            st.markdown("""
            - 🌐 **MJO aktif fase 4** (potensi hujan meningkat)
            - 🌊 **IOD negatif** (kondisi lebih basah dari normal)
            - 💧 **La Niña ringan** (penambahan curah hujan)
            - 🌬️ **Kelvin Wave** (hujan konvektif sore-malam)
            """)
        else:
            st.info("ℹ️ Tidak ada skala atmosfer signifikan yang terdeteksi memengaruhi wilayah ini saat ini.")

        st.divider()

        # Skala lokal
        st.markdown("### 🧭 **Skala Atmosfer Lokal yang Mungkin Aktif**")

        skala_lokal = []

        if kota in ["Malang", "Batu", "Boyolali", "Garut"]:
            skala_lokal += [
                "🌄 Angin Lembah–Gunung *(aktif pagi & malam)*",
                "🌬️ BBLJ *(belokan angin lapisan rendah)*",
                "🌊 Gelombang Kelvin *(hujan sore/malam)*"
            ]
        elif kota in ["Surabaya", "Sidoarjo", "Jakarta", "Bekasi"]:
            skala_lokal += [
                "🌬️ BBLJ *(konvergensi lokal & panas kota)*",
                "🔁 Konvergensi Lokal *(angin darat–laut)*"
            ]
        else:
            skala_lokal += [
                "🌬️ Proses Lokal *(BBLJ, konvergensi mikro)*",
                "☁️ Awan lokal akibat pemanasan permukaan"
            ]

        for skala in skala_lokal:
            st.markdown(f"- ✅ {skala}")

        st.caption("📌 Skala lokal disimulasikan berdasarkan lokasi dan musim.")

    else:
        st.error("❗ Kota tidak ditemukan. Mohon cek kembali ejaannya.")
else:
    st.warning("Silakan masukkan nama kota terlebih dahulu.")
