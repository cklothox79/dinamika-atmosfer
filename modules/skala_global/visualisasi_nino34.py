# 📁 Folder: modules/skala_global/

# ✅ 1. visualisasi_nino34.py

```python
import streamlit as st

def app():
    st.title("📍 Visualisasi Area Nino 3.4")

    st.markdown("""
    **Area Nino 3.4** adalah zona penting di Samudra Pasifik Tropis (antara 5°LU–5°LS dan 170°BB–120°BB)  
    yang digunakan untuk memantau gangguan suhu laut seperti **El Niño** dan **La Niña**.
    """)

    st.image("https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/el_nino_vs_lanina.png",
             caption="Perbandingan El Niño dan La Niña", use_column_width=True)

    st.markdown("""
    - **El Niño**: Pemanasan suhu laut di area Nino 3.4.
    - **La Niña**: Pendinginan suhu laut di area tersebut.
    - Pemantauan melalui ENSO Index seperti **ONI (Oceanic Niño Index)**.
    """)
