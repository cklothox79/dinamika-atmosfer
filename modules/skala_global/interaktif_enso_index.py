# modules/skala_global/interaktif_enso_index.py

import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("🌊 ENSO Index Interaktif")
    st.markdown("Visualisasi indeks ENSO bulanan (ONI - Oceanic Niño Index).")

    # Contoh data dummy
    data = {
        "Bulan": pd.date_range("2023-01", periods=12, freq='M'),
        "ONI": [-0.6, -0.7, -0.8, -0.5, -0.3, 0.1, 0.4, 0.6, 0.9, 1.1, 0.8, 0.5]
    }
    df = pd.DataFrame(data)

    fig = px.line(df, x="Bulan", y="ONI", title="📈 ONI (Oceanic Niño Index) Bulanan")
    st.plotly_chart(fig, use_container_width=True)
