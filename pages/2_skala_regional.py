# File: pages/2_skala_regional.py

import streamlit as st
import importlib

st.set_page_config(page_title="🌐 Skala Regional", layout="wide")
st.title(":globe_with_meridians: Skala Regional")
st.markdown("Silakan pilih visualisasi fenomena skala regional:")

opsi = st.radio("\ud83d\udccc Pilih visualisasi regional", [
    "MJO Index Interaktif",
    "Gelombang Kelvin Interaktif",
    "Gelombang Rossby Interaktif",
    "Posisi ITCZ Harian"
])

if opsi == "MJO Index Interaktif":
    modul = importlib.import_module("modules.skala_regional.interaktif_mjo_index")
    modul.app()

elif opsi == "Gelombang Kelvin Interaktif":
    modul = importlib.import_module("modules.skala_regional.interaktif_kelvin")
    modul.app()

elif opsi == "Gelombang Rossby Interaktif":
    modul = importlib.import_module("modules.skala_regional.interaktif_rossby")
    modul.app()

elif opsi == "Posisi ITCZ Harian":
    modul = importlib.import_module("modules.skala_regional.itcz_posisi")
    modul.app()
