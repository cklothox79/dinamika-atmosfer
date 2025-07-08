# File: modules/skala_global/visualisasi_nino34.py

import streamlit as st

def app():
    st.title("📍 Visualisasi Area Nino 3.4")

    st.markdown("""
    **Area Nino 3.4** adalah zona penting di Samudra Pasifik Tropis (antara 5°LU–5°LS dan 170°BB–120°BB)  
    yang digunakan untuk memantau gangguan suhu laut seperti **El Niño** dan **La Niña**.
    """)

    # Gambar langsung dari GitHub raw
    st.image(
        "https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/el_nino_map.png",
        caption="Area Nino 3.4 di Samudra Pasifik",
        use_column_width=True
    )

    st.markdown("""
    - **El Niño**: pemanasan suhu laut di area Nino 3.4.  
    - **La Niña**: pendinginan suhu laut di area tersebut.  
    - Pemantauan dilakukan melalui **ENSO Index** seperti **ONI (Oceanic Niño Index)**.
    """)
