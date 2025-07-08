# File: pages/skala_global/2_Interaktif_ENSO_Index.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="ENSO Index", layout="wide")
st.title("📈 Interaktif ENSO Index")

st.markdown("""
ENSO (El Niño-Southern Oscillation) Index digunakan untuk mengukur intensitas El Niño atau La Niña berdasarkan suhu muka laut di area Nino 3.4. Nilai:
- di atas +0.5°C → **El Niño**
- di bawah -0.5°C → **La Niña**
- di antara -0.5 hingga +0.5°C → **Netral**
""")

# Simulasi data ENSO index
data = {
    "Tanggal": pd.date_range(start="2025-01-01", periods=12, freq="M"),
    "ENSO_Index": [0.1, 0.3, 0.7, 1.1, 0.9, 0.2, -0.3, -0.6, -1.0, -0.7, -0.2, 0.4]
}
df_enso = pd.DataFrame(data)
df_enso["Kategori"] = df_enso["ENSO_Index"].apply(
    lambda x: "El Niño" if x > 0.5 else "La Niña" if x < -0.5 else "Netral"
)

fig = px.line(df_enso, x="Tanggal", y="ENSO_Index", color="Kategori", markers=True,
              title="Grafik ENSO Index per Bulan",
              labels={"ENSO_Index": "Nilai ENSO", "Tanggal": "Waktu"})

fig.add_hline(y=0.5, line_dash="dash", line_color="red")
fig.add_hline(y=-0.5, line_dash="dash", line_color="blue")

st.plotly_chart(fig, use_container_width=True)

st.caption("📊 Data disimulasikan untuk kebutuhan edukasi. Nantinya bisa dihubungkan ke NOAA atau BMKG.")
