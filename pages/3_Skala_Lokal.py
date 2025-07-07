# File: pages/3_Skala_Lokal.py

import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Skala Lokal", layout="wide")
st.title("🧭 Skala Atmosfer Lokal")

col1, col2 = st.columns([1.5, 1.2])

with col1:
    st.markdown("""
    Fenomena skala lokal memengaruhi wilayah kecil seperti satu kabupaten atau kota. Dampaknya bisa sangat signifikan dalam waktu singkat.

    ### 📌 Fenomena Umum
    - **Angin Lembah–Gunung**: Sirkulasi angin harian akibat perbedaan suhu siang–malam di daerah pegunungan. Umumnya memicu awan konvektif di sore hari.
    - **Konvergensi Mikro**: Terjadi karena perbedaan suhu lokal darat-laut, bisa memicu pembentukan awan dan hujan lokal.
    - **Efek Urban**: Kota besar menyerap panas, menyebabkan suhu tinggi dan potensi pembentukan awan hujan serta petir.

    Berikut ini visualisasi lokasi-lokasi representatif untuk fenomena tersebut di wilayah Jawa Timur:
    """)

    # Peta Interaktif
    m = folium.Map(location=[-7.5, 112.5], zoom_start=8, tiles="cartodbpositron")

    # Titik Efek Urban
    folium.Marker(
        location=[-7.2575, 112.7521],  # Surabaya
        tooltip="Efek Urban: Surabaya",
        icon=folium.Icon(color="red", icon="cloud")
    ).add_to(m)

    # Titik Angin Lembah–Gunung
    folium.Marker(
        location=[-7.9467, 112.6150],  # Kota Batu
        tooltip="Angin Lembah–Gunung: Batu",
        icon=folium.Icon(color="green", icon="flag")
    ).add_to(m)

    # Titik Konvergensi Mikro
    folium.Marker(
        location=[-7.5450, 112.2330],  # Gresik pinggir laut
        tooltip="Konvergensi Mikro: Gresik",
        icon=folium.Icon(color="blue", icon="tint")
    ).add_to(m)

    st_folium(m, height=450, width=700)

with col2:
    st.markdown("### 📘 Penjelasan Ringkas")
    st.markdown("""
    #### 🌇 Efek Urban
    - Kota besar seperti Surabaya memicu panas berlebih → udara naik → awan konvektif → hujan lokal atau petir.

    #### ⛰️ Angin Lembah–Gunung
    - Siang: angin naik ke pegunungan → awan berkembang
    - Malam: angin turun → potensi kabut/awan rendah

    #### 🌬️ Konvergensi Mikro
    - Perbedaan suhu laut dan darat (misal di Gresik) menciptakan pertemuan angin kecil → potensi awan hujan lokal

    👀 Lokasi di peta hanyalah contoh. Fenomena ini bisa terjadi di banyak tempat lain di Indonesia.
    """)
    st.caption("🧠 Disusun oleh Ferri Kusuma (STMKG) untuk edukasi publik cuaca dan atmosfer lokal.")
