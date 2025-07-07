# File: pages/3_Interaktif_IOD_Index.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Interaktif IOD Index", layout="wide")
st.title("🌊 Interaktif IOD Index")

st.markdown("""
**IOD (Indian Ocean Dipole)** adalah fenomena anomali suhu permukaan laut di Samudra Hindia bagian barat dan timur.
- **IOD Positif**: Samudra Hindia barat lebih hangat → Indonesia lebih kering.
- **IOD Negatif**: Samudra Hindia timur lebih hangat → Indonesia lebih basah.

Data di bawah adalah **simulasi** dan dapat diganti dengan data resmi dari BOM Australia.
""")

# Simulasi data IOD
bulan = pd.date_range("2024-01-01", periods=18, freq='M')
data_iod = [
    0.2, 0.3, 0.5, 0.6, 0.7, 0.4, 0.1, -0.1, -0.3,
   -0.5, -0.6, -0.4, -0.2, 0.0, 0.2, 0.3, 0.1, -0.2
]
df = pd.DataFrame({"Bulan": bulan, "IOD Index": data_iod})

# Status IOD
status = lambda iod: "Positif" if iod >= 0.4 else "Negatif" if iod <= -0.4 else "Netral"
df["Status"] = df["IOD Index"].apply(status)

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Bulan'], y=df['IOD Index'],
                         mode='lines+markers', name='IOD Index',
                         line=dict(color='darkorange')))
fig.add_hline(y=0.4, line=dict(dash='dash', color='red'))
fig.add_hline(y=-0.4, line=dict(dash='dash', color='blue'))
fig.update_layout(
    title="Simulasi Grafik IOD Index Bulanan",
    xaxis_title="Bulan",
    yaxis_title="Indeks IOD",
    height=500,
    plot_bgcolor="#fdf6ed",
)

st.plotly_chart(fig, use_container_width=True)

# Tabel
st.markdown("### 📋 Data Indeks IOD")
st.dataframe(df, use_container_width=True)

st.caption("📌 Nilai simulasi. Nantinya akan terhubung ke data BOM Australia secara otomatis.")
