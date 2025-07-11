import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from io import StringIO

st.set_page_config(page_title="Grafik Real-Time ENSO & IOD", layout="wide")
st.title("📊 Grafik Real-Time ENSO & IOD")

st.markdown("""
Halaman ini menampilkan grafik **ONI (ENSO Index)** dan **IOD Index** berdasarkan data resmi dari NOAA dan BOM Australia.

- 🔴 ONI: Indeks suhu laut Pasifik tengah (Nino 3.4)
- 🟠 IOD: Perbedaan suhu laut Samudra Hindia barat & timur
""")

# ========================================
# Fungsi Ambil Data ONI (NOAA)
# ========================================
@st.cache_data
def fetch_oni():
    url = "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.txt"
    res = requests.get(url)
    lines = res.text.strip().split('\n')[1:]

    data = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 13:
            year = parts[0]
            months = parts[1:]
            for i, val in enumerate(months):
                try:
                    month_str = ['DJF', 'JFM', 'FMA', 'MAM', 'AMJ', 'MJJ', 
                                 'JJA', 'JAS', 'ASO', 'SON', 'OND', 'NDJ'][i]
                    data.append({
                        'Year': int(year),
                        'TriMonth': month_str,
                        'ONI': float(val)
                    })
                except:
                    continue
    df = pd.DataFrame(data)

    # Mapping bulan tengah dari tiap 3-bulanan
    month_map = {
        'DJF': '01', 'JFM': '02', 'FMA': '03', 'MAM': '04',
        'AMJ': '05', 'MJJ': '06', 'JJA': '07', 'JAS': '08',
        'ASO': '09', 'SON': '10', 'OND': '11', 'NDJ': '12'
    }
    df['Tanggal'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['TriMonth'].map(month_map), errors='coerce')
    return df.dropna(subset=['Tanggal'])

# ========================================
# Fungsi Ambil Data IOD (BOM Australia)
# ========================================
@st.cache_data
def fetch_iod():
    url = "https://www.bom.gov.au/climate/enso/indices/archive/iod.txt"
    res = requests.get(url)
    lines = res.text.strip().split('\n')

    data = []
    for line in lines:
        if line and line[0].isdigit():
            parts = line.strip().split()
            if len(parts) >= 3:
                try:
                    year, month, iod_val = int(parts[0]), int(parts[1]), float(parts[2])
                    data.append({
                        'Tanggal': pd.to_datetime(f"{year}-{month:02d}-15"),
                        'IOD': iod_val
                    })
                except:
                    continue
    return pd.DataFrame(data)

# ========================================
# Grafik ONI
# ========================================
st.subheader("🔴 Oceanic Niño Index (ONI)")

try:
    oni_df = fetch_oni()
    fig_oni = go.Figure()
    fig_oni.add_trace(go.Scatter(x=oni_df['Tanggal'], y=oni_df['ONI'],
                                 mode='lines+markers', name='ONI',
                                 line=dict(color='red')))
    fig_oni.add_hline(y=0.5, line=dict(color="gray", dash="dot"), annotation_text="El Niño Threshold", annotation_position="top left")
    fig_oni.add_hline(y=-0.5, line=dict(color="gray", dash="dot"), annotation_text="La Niña Threshold", annotation_position="bottom left")
    fig_oni.update_layout(title="Oceanic Niño Index (ONI)",
                          xaxis_title="Tanggal",
                          yaxis_title="ONI (°C)",
                          height=400)
    st.plotly_chart(fig_oni, use_container_width=True)
except Exception as e:
    st.error(f"Gagal memuat data ONI: {e}")

# ========================================
# Grafik IOD
# ========================================
st.subheader("🟠 Indian Ocean Dipole (IOD) Index")

try:
    iod_df = fetch_iod()
    fig_iod = go.Figure()
    fig_iod.add_trace(go.Scatter(x=iod_df['Tanggal'], y=iod_df['IOD'],
                                 mode='lines+markers', name='IOD',
                                 line=dict(color='orange')))
    fig_iod.add_hline(y=0.4, line=dict(color="gray", dash="dot"), annotation_text="IOD Positif", annotation_position="top left")
    fig_iod.add_hline(y=-0.4, line=dict(color="gray", dash="dot"), annotation_text="IOD Negatif", annotation_position="bottom left")
    fig_iod.update_layout(title="Indian Ocean Dipole (IOD) Index",
                          xaxis_title="Tanggal",
                          yaxis_title="IOD Index",
                          height=400)
    st.plotly_chart(fig_iod, use_container_width=True)
except Exception as e:
    st.error(f"Gagal memuat data IOD: {e}")
