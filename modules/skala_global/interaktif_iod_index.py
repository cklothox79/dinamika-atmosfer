import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("🌊 IOD Index Interaktif")

    st.markdown("""
    **Indian Ocean Dipole (IOD)** adalah fenomena suhu permukaan laut di Samudra Hindia bagian barat dan timur.  
    Nilai IOD diukur dari selisih suhu antara dua wilayah ini:

    - **IOD Positif**: Perairan barat lebih hangat → curah hujan ke arah Afrika Timur, kekeringan di Indonesia.  
    - **IOD Negatif**: Perairan timur lebih hangat → hujan meningkat di Indonesia.

    Sumber data: [NOAA - JAMSTEC / BOM](https://www.jamstec.go.jp/aplinfo/sintexf/e/iod/dipole_mode_index.html)
    """)

    # Contoh data dummy (ganti dengan data asli jika tersedia)
    data = {
        "Tahun": [2021, 2022, 2023, 2024],
        "Januari": [0.1, -0.2, 0.3, 0.2],
        "Februari": [0.0, -0.1, 0.2, 0.1],
        "Maret": [-0.1, 0.0, 0.1, 0.0],
        "April": [0.0, 0.1, 0.2, 0.1],
        "Mei": [0.1, 0.3, 0.4, 0.2],
        "Juni": [0.2, 0.4, 0.5, 0.3],
        "Juli": [0.3, 0.5, 0.6, 0.4],
        "Agustus": [0.4, 0.6, 0.7, 0.5],
        "September": [0.5, 0.7, 0.8, 0.6],
        "Oktober": [0.4, 0.6, 0.7, 0.5],
        "November": [0.3, 0.5, 0.6, 0.4],
        "Desember": [0.2, 0.4, 0.5, 0.3],
    }

    df = pd.DataFrame(data)
    df_melted = df.melt(id_vars=["Tahun"], var_name="Bulan", value_name="IOD Index")

    fig = px.line(
        df_melted,
        x="Bulan",
        y="IOD Index",
        color="Tahun",
        markers=True,
        title="Perkembangan IOD Index per Bulan"
    )

    st.plotly_chart(fig, use_container_width=True)
