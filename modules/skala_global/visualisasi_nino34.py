# modules/skala_global/visualisasi_nino34.py

import streamlit as st

def app():
    st.markdown("<h1 style='color:#0066cc'>📍 Visualisasi Area Nino 3.4</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div style='font-size:18px'>
    <b>Area Nino 3.4</b> adalah zona penting di Samudra Pasifik Tropis  
    (antara <b>5°LU–5°LS</b> dan <b>170°BB–120°BB</b>)  
    yang digunakan untuk memantau gangguan suhu laut seperti <b>El Niño</b> dan <b>La Niña</b>.
    </div>
    """, unsafe_allow_html=True)

    st.image(
        "https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/el_nino_map.png",
        caption="Citra Area Nino 3.4 di Samudra Pasifik Tengah",
        use_column_width=True
    )

    st.markdown("""
    <div style='font-size:16px'>
    🔴 <b>El Niño</b>: pemanasan suhu laut di area Nino 3.4.<br>
    🔵 <b>La Niña</b>: pendinginan suhu laut di area tersebut.<br><br>
    Pemantauan biasanya dilakukan melalui <b>ENSO Index</b> seperti <i>ONI (Oceanic Niño Index)</i>.
    </div>
    """, unsafe_allow_html=True)
