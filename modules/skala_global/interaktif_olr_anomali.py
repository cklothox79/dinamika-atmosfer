# modules/skala_global/interaktif_olr_anomali.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def app():
    st.title("🌧️ OLR Anomali Interaktif")
    st.markdown("""
    **OLR (Outgoing Longwave Radiation)** merupakan pancaran gelombang panjang dari permukaan bumi dan awan ke luar angkasa.  
    Nilai OLR rendah → **tutupan awan tebal**, potensi hujan tinggi.  
    Nilai OLR tinggi → **cuaca cerah**, langit bersih dari awan konvektif.

    Di bawah ini adalah visualisasi anomali OLR 30 hari terakhir (simulasi data):
    """)

    # Simulasi data
    tanggal = [datetime(2025, 6, 10) + timedelta(days=i) for i in range(30)]
    olr_anomali = [
        5, 3, 0, -3, -8, -12, -15, -18, -10, -5,
        -2, 1, 4, 7, 10, 12, 8, 5, 2, -2,
        -5, -10, -13, -17, -12, -8, -4, 0, 4, 6
    ]

    # Pastikan jumlah data sama
    if len(tanggal) != len(olr_anomali):
        st.error("Jumlah data tanggal dan OLR tidak sama.")
        return

    df = pd.DataFrame({
        "Tanggal": tanggal,
        "Anomali_OLR": olr_anomali
    })

    fig = px.line(df, x="Tanggal", y="Anomali_OLR", markers=True,
                  title="📉 Anomali OLR 30 Hari Terakhir",
                  labels={"Anomali_OLR": "Anomali OLR (W/m²)"},
                  color_discrete_sequence=["orange"])

    fig.add_hline(y=0, line_dash="dot", line_color="gray")

    fig.update_layout(
        height=400,
        plot_bgcolor="#f9f9f9",
        yaxis=dict(title="Anomali OLR (W/m²)", zeroline=True)
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("📌 Nilai negatif = awan banyak (potensi hujan). Positif = cuaca cerah.")
