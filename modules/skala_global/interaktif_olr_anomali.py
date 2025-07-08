import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("🔴🔵 OLR Anomali Interaktif")

    st.markdown("""
    **Outgoing Longwave Radiation (OLR)** merupakan pancaran gelombang panjang dari permukaan Bumi ke atmosfer luar.  
    OLR sering digunakan sebagai **indikator tutupan awan konvektif** di daerah tropis.

    - **OLR negatif (anomali rendah)** → Menandakan banyak awan dan hujan (konveksi aktif).
    - **OLR positif (anomali tinggi)** → Menandakan sedikit awan atau kondisi kering.

    📌 **Sumber data**: NOAA Climate Prediction Center  
    Referensi: [https://www.cpc.ncep.noaa.gov/products/precip/CWlink/ir_anim_monthly.shtml](https://www.cpc.ncep.noaa.gov/products/precip/CWlink/ir_anim_monthly.shtml)
    """)

    # Contoh data dummy OLR anomali per kota
    data = {
        "Tanggal": pd.date_range(start="2024-12-01", periods=30, freq="D"),
        "Wilayah": ["Sumatera", "Jawa", "Kalimantan", "Sulawesi", "Papua"] * 6,
        "Anomali_OLR": [-10, -5, 0, 5, 10] * 6
    }
    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x="Tanggal",
        y="Anomali_OLR",
        color="Wilayah",
        title="Anomali OLR Harian per Wilayah",
        labels={"Anomali_OLR": "Anomali OLR (W/m²)"},
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    > 🔵 Anomali negatif = potensi hujan tinggi  
    > 🔴 Anomali positif = cuaca cerah/kering
    """)
