# File: pages/skala_global/3_Interaktif_IOD_Index.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="IOD Index", layout="wide")
st.title("🌊 Interaktif IOD Index")

st.markdown("""
IOD (Indian Ocean Dipole) Index mengukur anomali suhu permukaan laut antara barat dan timur Samudra Hindia.
- IOD Positif → Timur lebih dingin → **Musim kering di Indonesia**
- IOD Negatif → Timur lebih hangat → **Musim hujan di Indonesia**
- IOD Netral → Tidak dominan

""")

# Simulasi data IOD index
data = {
    "Tanggal": pd.date_range(start="2025-01-01", periods=12, freq="M"),
    "IOD_Index": [0.0, -0.3, -0.5, -0.7, -0.6, -0.2, 0.3, 0.6, 0.9, 0.5, 0.1, -0.1]
}
df_iod = pd.DataFrame(data)
df_iod["Kategori"] = df_iod["IOD_Index"].apply(
    lambda x: "Positif" if x >= 0.4 else "Negatif" if x <= -0.4 else "Netral"
)

fig = px.line(df_iod, x="Tanggal", y="IOD_Index", color="Kategori", markers=True,
              title="Grafik IOD Index per Bulan",
              labels={"IOD_Index": "Nilai IOD", "Tanggal": "Waktu"})

fig.add_hline(y=0.4, line_dash="dash", line_color="red")
fig.add_hline(y=-0.4, line_dash="dash", line_color="blue")

st.plotly_chart(fig, use_container_width=True)

st.caption("📊 Data disimulasikan untuk kebutuhan edukasi. Nantinya bisa dihubungkan ke BMKG atau JAMSTEC.")
