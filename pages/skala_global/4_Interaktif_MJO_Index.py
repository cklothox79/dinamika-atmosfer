# File: pages/skala_global/4_Interaktif_MJO_Index.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="MJO Index", layout="wide")
st.title("☁️ Interaktif MJO Index")

st.markdown("""
Madden-Julian Oscillation (MJO) adalah gangguan atmosfer tropis yang bergerak dari barat ke timur. Aktivitas MJO memengaruhi pola hujan dan konveksi di Indonesia.
- Fase 4–6 → MJO aktif di wilayah Indonesia
- Nilai indeks mendekati pusat lingkaran → MJO lemah atau tidak aktif

Berikut ini adalah simulasi indeks MJO untuk beberapa waktu ke belakang:
""")

# Simulasi data MJO
tanggal = pd.date_range(start="2025-01-01", periods=15, freq="7D")
data = {
    "Tanggal": tanggal,
    "Fase": [3, 4, 5, 6, 6, 5, 4, 3, 2, 1, 8, 7, 6, 5, 4],
    "Amplitude": [0.5, 1.2, 1.6, 1.8, 1.7, 1.4, 1.1, 0.8, 0.6, 0.4, 0.3, 0.7, 1.1, 1.5, 1.8]
}
df_mjo = pd.DataFrame(data)

fig = px.scatter_polar(
    df_mjo,
    r="Amplitude",
    theta="Fase",
    color="Tanggal",
    title="Diagram Polar MJO Index",
    color_discrete_sequence=px.colors.sequential.Plasma_r,
    range_r=[0, 2.5],
    direction="clockwise",
    start_angle=90
)

st.plotly_chart(fig, use_container_width=True)

st.caption("🌐 Sumber data: simulasi. Untuk implementasi nyata bisa disambungkan ke data BMKG atau CPC NOAA.")
