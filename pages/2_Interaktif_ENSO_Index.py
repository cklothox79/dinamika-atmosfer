# File: pages/2_Interaktif_ENSO_Index.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Interaktif ENSO Index", layout="wide")
st.title("📈 Interaktif ENSO Index")

st.markdown("""
ENSO (El Niño–Southern Oscillation) index digunakan untuk mengklasifikasikan kondisi El Niño, La Niña, atau netral.
Data di bawah ini adalah **simulasi**. Nantinya akan terhubung ke sumber data resmi seperti NOAA atau BMKG.
""")

# Simulasi data index ENSO
bulan = pd.date_range("2024-01-01", periods=18, freq='M')
data_enso = [
    -0.3, -0.4, -0.6, -0.8, -0.9, -0.7, -0.5, -0.2, 0.0,
     0.1, 0.4, 0.7, 0.9, 1.1, 0.8, 0.3, 0.0, -0.2
]
df = pd.DataFrame({"Bulan": bulan, "ENSO Index": data_enso})

# Status ENSO
def status(enso):
    if enso >= 0.5:
        return "El Niño"
    elif enso <= -0.5:
        return "La Niña"
    else:
        return "Netral"
df["Status"] = df["ENSO Index"].apply(status)

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Bulan'], y=df['ENSO Index'],
                         mode='lines+markers', name='ENSO Index',
                         line=dict(color='royalblue')))
fig.add_hline(y=0.5, line=dict(dash='dash', color='red'))
fig.add_hline(y=-0.5, line=dict(dash='dash', color='blue'))
fig.update_layout(
    title="Simulasi Grafik ENSO Index Bulanan",
    xaxis_title="Bulan",
    yaxis_title="Indeks ENSO",
    height=500,
    plot_bgcolor="#f0f2f6",
)

st.plotly_chart(fig, use_container_width=True)

# Tabel
st.markdown("### 📋 Data Indeks ENSO")
st.dataframe(df, use_container_width=True)

st.caption("📌 Nilai simulasi. Nantinya akan terhubung ke data NOAA secara otomatis.")
