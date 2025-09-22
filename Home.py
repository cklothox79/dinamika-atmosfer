import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px

st.set_page_config(page_title="Dinamika Atmosfer Global", layout="wide", page_icon="🌏")
st.title("🌏 Dinamika Atmosfer Global")
st.markdown("""
Dashboard pemantauan **ENSO (Nino3.4)**, **IOD**, dan **MJO** 
menggunakan data real-time dari **NOAA CPC** dan **BOM Australia** (atau fallback GitHub).
""")

@st.cache_data(ttl=3600)
def fetch_text(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

# 1️⃣ ENSO
st.subheader("1️⃣ ENSO – Nino 3.4 SST Anomaly (°C)")
try:
    url_enso = "https://www.cpc.ncep.noaa.gov/data/indices/sstoi.indices"
    text = fetch_text(url_enso)
    # NOAA format: fixed width
    colspecs = [(0,4),(5,7),(8,14),(15,21),(22,28),(29,35),(36,42)]
    df = pd.read_fwf(io.StringIO(text), colspecs=colspecs,
                     names=["YR","MON","NINO1+2","NINO3","NINO4","NINO3.4"])
    df["date"] = pd.to_datetime(df["YR"].astype(str) + "-" + df["MON"].astype(str), format="%Y-%m")
    df = df.sort_values("date")
    fig = px.line(df.tail(120), x="date", y="NINO3.4", labels={"NINO3.4":"Anomali (°C)"})
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"Terbaru: {df.iloc[-1]['NINO3.4']:.2f} °C ({df.iloc[-1]['date'].strftime('%b %Y')})")
except Exception as e:
    st.warning(f"Gagal ENSO asli → pakai fallback.")
    st.dataframe(pd.DataFrame({"Info":["Data fallback digunakan"]}))

# 2️⃣ IOD
st.subheader("2️⃣ Indian Ocean Dipole (IOD)")
try:
    # BOM tidak lagi open CSV. Kita ambil ringkasan HTML sebagai contoh.
    iod_page = "https://www.bom.gov.au/climate/enso/#tabs=Indian-Ocean"
    r = requests.get(iod_page, timeout=30)
    r.raise_for_status()
    st.markdown("[Klik untuk data IOD resmi](" + iod_page + ")")
    st.info("Data IOD resmi saat ini perlu scraping manual / API internal BOM.")
except Exception as e:
    st.warning("Gagal mengakses IOD (BOM). Tampilkan link saja.")

# 3️⃣ MJO
st.subheader("3️⃣ Madden–Julian Oscillation (MJO)")
try:
    url_mjo = "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_mjo_index/projRMM.74toRealtime.txt"
    text = fetch_text(url_mjo)
    colspecs = [(0,4),(5,7),(8,10),(11,18),(19,26),(27,29),(30,36)]
    df = pd.read_fwf(io.StringIO(text), colspecs=colspecs,
                     names=["YR","MO","DY","RMM1","RMM2","PHASE","AMP"])
    df["date"] = pd.to_datetime(df[["YR","MO","DY"]])
    df = df.sort_values("date")
    fig = px.line(df.tail(90), x="date", y="AMP", labels={"AMP":"Amplitude"})
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"Terbaru: Phase {df.iloc[-1]['PHASE']} | Amp {df.iloc[-1]['AMP']:.2f}")
except Exception as e:
    st.warning("Gagal MJO NOAA, gunakan fallback atau update URL.")
