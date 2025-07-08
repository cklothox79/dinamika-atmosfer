# File: modules/skala_global/interaktif_enso_index.py

import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("📈 ENSO Index Interaktif")

    st.markdown("""
    **ENSO Index** seperti **ONI (Oceanic Niño Index)** digunakan untuk memantau kejadian **El Niño** dan **La Niña**  
    berdasarkan anomali suhu laut di area Nino 3.4.

    Di bawah ini adalah contoh visualisasi interaktif ENSO Index.
    """)

    # Contoh dummy data ENSO
    data = {
        "Tahun": [2019, 2020, 2021, 2022, 2023],
        "ONI": [0.7, -0.8, -0.5, 0.9, 1.2]
    }
    df = pd.DataFrame(data)

    fig = px.line(df, x="Tahun", y="ONI", markers=True, title="Anomali ONI (Oceanic Niño Index)")
    fig.update_layout(yaxis_title="ONI (°C)", xaxis_title="Tahun")

    st.plotly_chart(fig, use_container_width=True)

    st.info("📌 Nilai ONI > 0.5 menandakan El Niño, ONI < -0.5 menandakan La Niña.")
