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

# ================================
# Fungsi Ambil Data ONI (ENSO)
# ================================
@st.cache_data
def fetch_oni():
    url = "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.txt"
    r = requests.get(url)
    raw = r.text.strip().split('\n')[1:]  # skip header
    df = pd.read_csv(StringIO('\n'.join(raw)), delim_whitespace=True)
    data = df.melt(id_vars=['YR'], var_name='Bulan', value_name='ONI')
    data['Tanggal'] = data['YR'].astype(str) + '-' + data['Bulan']
    data['Tanggal'] = pd.to_datetime(data['Tanggal'], format='%Y-%b')
    data = data.sort_values('Tanggal')
    return data

# ================================
# Fungsi Ambil Data IOD
# ================================
@st.cache_data
def fetch_iod():
    url = "https://www.bom.gov.au/climate/enso/indices/archive/iod.txt"
    r = requests.get(url)
    lines = r.text.strip().split('\n')
    data_lines = [l for l in lines if l and l[0].isdigit()]
    df = pd.read_csv(StringIO('\n'.join(data_lines)), delim_whitespace=True)
    df['Tanggal'] = pd.to_datetime(df[['YR', 'MON']].assign(DAY=15))
    df = df[['Tanggal', 'IOD']]
    return df

# ================================
# Tampilkan Grafik ONI
# ================================
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

# ================================
# Tampilkan Grafik IOD
# ================================
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
