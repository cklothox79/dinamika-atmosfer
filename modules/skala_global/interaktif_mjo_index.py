import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("🌐 MJO Index Interaktif")

    st.markdown("""
    **Madden-Julian Oscillation (MJO)** adalah pola gangguan atmosfer tropis yang berpindah dari barat ke timur,  
    biasanya berdampak pada hujan, tekanan udara, dan konveksi di wilayah tropis, termasuk Indonesia.

    - MJO memiliki **8 fase**, tiap fase memengaruhi wilayah yang berbeda.
    - Fase **4–6** biasanya mendukung peningkatan curah hujan di Indonesia.
    - Fase **0 (nol)** menunjukkan kondisi MJO lemah/tidak aktif.

    Sumber data: [BOM Australia](http://www.bom.gov.au/climate/mjo/graphics/rmm.74toRealtime.txt)
    """)

    # Contoh data dummy (bisa diganti dengan RMM index asli)
    data = {
        "Tanggal": pd.date_range(start="2024-12-01", periods=30, freq="D"),
        "Fase_MJO": [1, 2, 3, 4, 5, 6, 7, 8, 0] * 3 + [1, 2, 3],
        "Amplitude": [1.2, 1.4, 1.0, 0.8, 1.1, 1.3, 0.9, 1.2, 0.3]*3 + [1.0, 1.1, 0.9],
    }
    df = pd.DataFrame(data)

    fig = px.scatter(
        df,
        x="Tanggal",
        y="Fase_MJO",
        color="Amplitude",
        color_continuous_scale="Viridis",
        size="Amplitude",
        title="Pergerakan Fase MJO Harian",
        labels={"Fase_MJO": "Fase MJO", "Amplitude": "Amplitudo"},
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    > Amplitudo di bawah 1.0 umumnya menandakan MJO tidak signifikan atau **tidak aktif**.
    """)
