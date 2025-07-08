# modules/skala_global/interaktif_mjo_index.py

import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("🌐 MJO Index Interaktif")
    st.markdown("""
    **Madden–Julian Oscillation (MJO)** adalah gelombang konvektif tropis yang bergerak dari barat ke timur,  
    membawa awan dan hujan di sepanjang khatulistiwa, dan berdampak besar pada pola hujan di Indonesia.

    - **Fase 1–2** → MJO aktif di Afrika
    - **Fase 3–4** → Samudra Hindia barat
    - **Fase 5–6** → Indonesia & sekitarnya
    - **Fase 7–8** → Samudra Pasifik

    Berikut adalah data simulasi indeks MJO 30 hari terakhir:
    """)

    # Data simulasi MJO
    tgl = pd.date_range("2025-06-10", periods=30, freq='D')
    fase = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 8, 7, 6, 5, 4, 3, 4, 5, 6, 6, 5, 4, 3, 3, 4, 5, 6, 7, 8]
    amplitudo = [0.3, 0.5, 0.8, 1.0, 1.3, 1.4, 1.2, 1.1, 0.9, 0.8, 0.6, 0.7, 0.8, 1.0, 1.3, 1.4, 1.2, 1.1, 1.3, 1.5, 1.4, 1.2, 1.1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]

    df = pd.DataFrame({
        "Tanggal": tgl,
        "Fase": fase,
        "Amplitudo": amplitudo
    })

    fig = px.scatter(df, x="Fase", y="Amplitudo", color="Tanggal",
                     size="Amplitudo", hover_data=["Tanggal"],
                     title="📈 MJO Index – 30 Hari Terakhir",
                     labels={"Fase": "Fase MJO", "Amplitudo": "Kuatnya MJO"})

    fig.update_layout(
        xaxis=dict(dtick=1, range=[0.5, 8.5]),
        yaxis=dict(range=[0, 2]),
        coloraxis_showscale=False,
        plot_bgcolor="#fafafa"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("📌 Data simulasi. MJO fase 4–6 menunjukkan potensi hujan meningkat di Indonesia.")
