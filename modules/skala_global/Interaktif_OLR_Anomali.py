# File: pages/skala_global/5_Interaktif_OLR_Anomali.py

import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="OLR Anomali", layout="wide")
st.title("☁️ Interaktif OLR Anomali")

st.markdown("""
Anomali OLR (Outgoing Longwave Radiation) adalah selisih antara nilai pancaran radiasi gelombang panjang sebenarnya
dengan nilai normalnya. Nilai ini digunakan untuk mengamati aktivitas konveksi (awan dan hujan) di wilayah tropis.

- **OLR negatif** → banyak awan tinggi dan kemungkinan hujan.
- **OLR positif** → langit cerah, sedikit awan tinggi.

Data OLR sangat penting untuk analisis dinamika atmosfer global, termasuk mendeteksi MJO, Kelvin Wave, dan siklus hujan tropis.
""")

st.info("📌 Simulasi ini menampilkan data OLR anomali bulanan secara interaktif.")

# Simulasi data
bulan = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
data = {
    "Bulan": bulan,
    "Anomali OLR (W/m²)": [-5, -3, 0, 2, 4, -2, -6, -3, 1, 3, 2, -1]
}
df = pd.DataFrame(data)

fig = px.bar(df, x="Bulan", y="Anomali OLR (W/m²)", color="Anomali OLR (W/m²)",
             color_continuous_scale="RdBu_r",
             title="Anomali OLR Bulanan (simulasi)")
fig.update_layout(
    xaxis_title="Bulan",
    yaxis_title="Anomali OLR (W/m²)",
    height=400,
    margin=dict(l=10, r=10, t=40, b=10),
    plot_bgcolor="#f0f2f6"
)

st.plotly_chart(fig, use_container_width=True)

st.caption("📊 Data simulasi. Untuk implementasi penuh dapat terhubung ke NOAA atau BMKG.")
