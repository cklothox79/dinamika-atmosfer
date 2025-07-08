# File: modules/skala_global/visualisasi_nino34.py

import streamlit as st

def app():
    st.title("📍 Visualisasi Area Niño 3.4")

    st.markdown("""
    Area **Niño 3.4** berada di Samudra Pasifik tropis (5°LU–5°LS, 120°BB–170°BB).  
    Gambar di bawah memperlihatkan kotak yang menandai area tersebut, lengkap dengan animasi SST untuk El Niño dan La Niña.
    """)

    st.image(
        "https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/nino34_box.png",
        caption="🍃 SST Anomali dan kotak Niño 3.4",
        use_container_width=True
    )

    st.markdown("""
    - Kotak putih menunjukkan **zona Niño 3.4**.
    - Warna **merah/oranye**: suhu laut di atas rata-rata (El Niño).
    - Warna **biru**: suhu laut lebih dingin (La Niña).
    """)

    st.info("Animasi bergerak SST tersedia di versi lengkap, ini untuk ilustrasi awal.")
