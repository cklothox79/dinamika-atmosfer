# modules/skala_regional/interaktif_rossby.py

import streamlit as st

def app():
    st.title("🌊 Visualisasi Gelombang Rossby (BBLJ)")

    st.markdown("""
    **Gelombang Rossby** atau **Back-Building Longwave Jet (BBLJ)** adalah gelombang atmosfer yang bergerak ke barat
    dan berperan dalam pola konveksi di wilayah tropis.

    Ciri-ciri:
    - Bergerak lambat dan besar skalanya.
    - Dapat memperkuat atau mengganggu sistem cuaca di Indonesia.
    - Terpantau melalui anomali angin dan OLR.

    Di bawah ini contoh wilayah dan waktu dominasi gelombang Rossby:

    """)
    
    st.image("https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/gelombang_rossby_zona.png",
             caption="Contoh lokasi dominasi Gelombang Rossby di kawasan maritim Indonesia.",
             use_column_width=True)
