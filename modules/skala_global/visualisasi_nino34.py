# File: modules/skala_global/visualisasi_nino34.py

import streamlit as st

def app():
    st.title("📍 Visualisasi Area Nino 3.4")

    st.markdown("""
    **Area Nino 3.4** adalah zona penting di Samudra Pasifik Tropis, tepatnya di antara garis lintang **5°LU–5°LS** dan garis bujur **170°BB–120°BB**.

    Wilayah ini digunakan sebagai acuan utama dalam mendeteksi fenomena **El Niño** dan **La Niña**, karena perubahan suhu permukaan laut di area ini sangat memengaruhi dinamika atmosfer global.
    """)

    st.image(
        "https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/el_nino_vs_la_nina.png",
        caption="Perbandingan El Niño dan La Niña",
        use_container_width=True
    )

    st.markdown("""
    ### 🌊 Apa yang Terjadi?

    - **El Niño** terjadi ketika suhu laut di area ini **lebih hangat dari normal** selama beberapa bulan.
    - **La Niña** terjadi ketika suhu laut di area ini **lebih dingin dari normal**.
    - Kedua fenomena ini dipantau menggunakan **ENSO Index** seperti **ONI (Oceanic Niño Index)**.

    """)
