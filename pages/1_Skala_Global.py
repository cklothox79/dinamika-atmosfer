# File: pages/1_Skala_Global.py

import streamlit as st
import importlib

st.set_page_config(page_title="🌏 Skala Global", layout="wide")
st.title("🌏 Skala Global")
st.markdown("Silakan pilih visualisasi di bawah:")

opsi = st.radio("📌 Pilih visualisasi global", [
    "Visualisasi Nino 3.4",
    "ENSO Index Interaktif",
    "IOD Index Interaktif",
    "MJO Index Interaktif",
    "OLR Anomali Interaktif"
])

if opsi == "Visualisasi Nino 3.4":
    modul = importlib.import_module("modules.skala_global.visualisasi_nino34")
    modul.app()

elif opsi == "ENSO Index Interaktif":
    modul = importlib.import_module("modules.skala_global.interaktif_enso_index")
    modul.app()

elif opsi == "IOD Index Interaktif":
    modul = importlib.import_module("modules.skala_global.interaktif_iod_index")
    modul.app()

elif opsi == "MJO Index Interaktif":
    modul = importlib.import_module("modules.skala_global.interaktif_mjo_index")
    modul.app()

elif opsi == "OLR Anomali Interaktif":
    modul = importlib.import_module("modules.skala_global.interaktif_olr_anomali")
    modul.app()
