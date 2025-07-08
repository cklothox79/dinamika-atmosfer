# modules/skala_global/interaktif_enso_index.py

import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("🌊 ENSO Index Interaktif")
    st.markdown("""
    Indeks ENSO (El Niño–Southern Oscillation) menggambarkan anomali suhu laut di kawasan Nino 3.4.  
    Nilai positif menandakan **El Niño**, sementara nilai negatif menandakan **La Niña**.
    """)

    # Contoh data ENSO (ONI) dummy
    data = {
        "Bulan": pd.date_range("2024-07-01", periods=12, freq="MS"),
        "ONI": [-0.6, -0.7, -0.8, -0.5, -0.3, 0.1, 0.4, 0.6, 0.9, 1.1, 0.8, 0.5]
    }
    df = pd.DataFrame(data)

    # Visualisasi grafik
    fig = px.line(df, x="Bulan", y="ONI", markers=True,
                  title="📈 ONI (Oceanic Niño Index) Bulanan",
                  labels={"ONI": "Nilai ONI", "Bulan": "Bulan"})
    
    fig.update_layout(
        yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='gray'),
        shapes=[
            dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=0.5, y1=2.5,
                 fillcolor="red", opacity=0.1, layer="below", line_width=0),
            dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=-2.5, y1=-0.5,
                 fillcolor="blue", opacity=0.1, layer="below", line_width=0)
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("📌 Data disimulasikan untuk tujuan visualisasi. Data asli tersedia di [NOAA Climate Prediction Center](https://origin.cpc.ncep.noaa.gov).")
