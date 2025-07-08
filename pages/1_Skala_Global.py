# File: pages/1_Skala_Global.py

import streamlit as st

st.set_page_config(page_title="Skala Global", layout="wide")
st.title("🌏 Skala Global")
st.markdown("Silakan pilih visualisasi di bawah:")

# Tautan ke halaman di luar folder pages/
st.page_link("modules/skala_global/1_Visualisasi_Nino34.py", label="📍 Visualisasi Nino 3.4", icon="🌊")
st.page_link("modules/skala_global/2_Interaktif_ENSO_Index.py", label="📈 Interaktif ENSO Index")
st.page_link("modules/skala_global/3_Interaktif_IOD_Index.py", label="📈 Interaktif IOD Index")
st.page_link("modules/skala_global/4_Interaktif_MJO_Index.py", label="📈 Interaktif MJO Index")
st.page_link("modules/skala_global/5_Interaktif_OLR_Anomali.py", label="🌤️ Interaktif OLR Anomali")
