# modules/skala_global/visualisasi_nino34.py

import streamlit as st

def app():
    st.title("📍 Visualisasi Area Nino 3.4")

    st.markdown("""
    **Area Nino 3.4** adalah zona penting di Samudra Pasifik Tropis  
    (antara 5°LU–5°LS dan 170°BB–120°BB) yang digunakan untuk memantau  
    gangguan suhu laut seperti **El Niño** dan **La Niña**.
    """)

    st.image(
        "https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/el_nino_vs_la_nina.png",
        caption="Perbandingan El Niño dan La Niña",
        use_container_width=True
    )

    st.markdown("""
    - **El Niño**: Pemanasan suhu laut di area Nino 3.4 → berdampak pada musim kemarau lebih panjang.
    - **La Niña**: Pendinginan suhu laut di area Nino 3.4 → berpotensi meningkatkan curah hujan di Indonesia.
    - Pemantauan biasanya menggunakan **ENSO Index** seperti ONI (Oceanic Niño Index).
    """)

    st.info("🔍 Gambar menunjukkan lokasi area Nino 3.4 dan pola perbedaan suhu laut saat El Niño dan La Niña.")
