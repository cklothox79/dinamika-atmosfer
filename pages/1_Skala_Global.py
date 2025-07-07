# File: pages/1_Skala_Global.py

import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Skala Global", layout="wide")
st.title("🌐 Skala Atmosfer Global")

col1, col2 = st.columns([1.6, 1.0])

with col1:
    st.markdown("""
    Fenomena global adalah dinamika atmosfer dan laut yang memengaruhi iklim secara luas, termasuk Indonesia.

    ### 📌 Tiga Fenomena Utama
    - **El Niño / La Niña** → perubahan suhu permukaan laut di Samudra Pasifik tengah–timur (zona Nino 3.4)
    - **IOD (Indian Ocean Dipole)** → anomali suhu laut di Samudra Hindia tropis
    - **MJO (Madden Julian Oscillation)** → gangguan konvektif tropis yang bergerak dari barat ke timur

    Peta berikut menampilkan wilayah penting seperti zona **Nino 3.4**, lokasi pengamatan IOD, dan garis khatulistiwa.
    """)

    # Peta Interaktif
    m = folium.Map(location=[0, -140], zoom_start=2, tiles="cartodbpositron")

    # Area Nino 3.4 (5N–5S, 170W–120W)
    bounds = [[5, -170], [-5, -120]]  # lat, lon
    folium.Rectangle(
        bounds=bounds,
        color='blue',
        fill=True,
        fill_opacity=0.4,
        tooltip="Zona Nino 3.4 (5°N–5°S, 170°W–120°W)"
    ).add_to(m)

    # Lokasi pengamatan IOD (Samudra Hindia)
    folium.Marker(
        location=[0, 75],
        tooltip="Samudra Hindia (IOD)",
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(m)

    # Garis khatulistiwa
    folium.PolyLine(
        locations=[[0, -180], [0, 180]],
        color="black",
        weight=1,
        tooltip="Khatulistiwa"
    ).add_to(m)

    st_folium(m, height=450, width=750)

with col2:
    st.markdown("### 📘 Penjelasan Mudah Dipahami")
    st.markdown("""
    #### 🔄 El Niño & La Niña
    - **Nino 3.4** adalah wilayah pemantauan utama suhu laut di Pasifik.
    - Suhu di atas normal → **El Niño** → kering di Indonesia.
    - Suhu di bawah normal → **La Niña** → hujan meningkat.

    #### 🌊 IOD (Indian Ocean Dipole)
    - Suhu laut barat Indonesia < atau > Samudra Hindia barat.
    - **Positif** → kering, **Negatif** → basah.

    #### 🌐 MJO
    - Gangguan awan bergerak dari barat ke timur.
    - Jika aktif di wilayah Indonesia → hujan meningkat.

    🌍 Semua fenomena ini saling memengaruhi dan berperan besar terhadap musim & cuaca kita.
    """)
    st.caption("📡 Disusun oleh Ferri Kusuma (STMKG) untuk edukasi masyarakat umum.")
    # Tambahkan ini setelah st.title(...) atau di bagian paling bawah

st.markdown("### 🌊 Visualisasi Perbandingan El Niño dan La Niña")
st.image(
    "https://files.oaiusercontent.com/file-1IfOf1Wjj0mWzU5hnBP6NELe?se=2025-07-07T16%3A30%3A00Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/jpeg&sig=LgE9yKTVN7O8DxRl7Es3UKp+XkSyxBM2RSkAXZRHg6s%3D",
    caption="Perbandingan kondisi atmosfer dan laut pada El Niño vs La Niña.",
    use_column_width=True
)

