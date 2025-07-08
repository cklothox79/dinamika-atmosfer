# File: modules/skala_global/visualisasi_nino34.py

import streamlit as st

def app():
    st.set_page_config(page_title="Visualisasi Nino 3.4", layout="wide")

    st.title("📍 Visualisasi Area Nino 3.4")

    st.markdown("""
    **Area Nino 3.4** adalah zona penting di Samudra Pasifik Tropis (antara 5°LU–5°LS dan 170°BB–120°BB)  
    yang digunakan untuk memantau gangguan suhu laut seperti **El Niño** dan **La Niña**.

    Berikut ini perbandingan visual kondisi atmosfer dan laut pada kedua fenomena:
    """)

    st.image("https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/el_nino_vs_lanina.png", caption="Perbandingan kondisi El Niño dan La Niña", use_column_width=True)

    st.markdown("""
    - **El Niño** ditandai dengan pemanasan suhu laut di area Nino 3.4.
    - **La Niña** ditandai dengan pendinginan suhu laut di area tersebut.
    - Indeks yang digunakan untuk memantau kondisi ini disebut **ENSO Index**, salah satunya adalah ONI (Oceanic Niño Index).

    Anda dapat melihat grafik indeks ENSO lebih lanjut di halaman lain.
    """)

