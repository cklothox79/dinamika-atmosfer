# modules/skala_global/interaktif_iod_index.py

import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("🌊 IOD Index Interaktif")
    st.markdown("""
    **Indian Ocean Dipole (IOD)** menggambarkan perbedaan suhu laut antara Samudra Hindia bagian barat dan timur.  
    - **IOD Positif** → Indonesia lebih kering  
    - **IOD Negatif** → Indonesia lebih basah  
    - **IOD Netral** → Tidak terlalu berpengaruh
    
    Berikut adalah data simulasi indeks IOD selama 12 bulan terakhir.
    """)

    # Contoh data IOD (simulasi)
    data = {
        "Bulan": pd.date_range("2024-07-01", periods=12, freq="MS"),
        "IOD": [-0.4, -0.5, -0.6, -0.3, -0.1, 0.2, 0.5, 0.8, 0.6, 0.3, 0.0, -0.2]
    }
    df = pd.DataFrame(data)

    # Visualisasi
    fig = px.line(df, x="Bulan", y="IOD", markers=True,
                  title="📈 IOD Index Bulanan",
                  labels={"IOD": "Nilai IOD", "Bulan": "Bulan"})
    
    fig.update_layout(
        yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='gray'),
        shapes=[
            dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=0.4, y1=2,
                 fillcolor="red", opacity=0.1, layer="below", line_width=0),
            dict(type="rect", xref="paper", yref="y", x0=0, x1=1, y0=-2, y1=-0.4,
                 fillcolor="blue", opacity=0.1, layer="below", line_width=0)
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("📌 Data disimulasikan. Data asli dapat diakses melalui Bureau of Meteorology Australia.")
