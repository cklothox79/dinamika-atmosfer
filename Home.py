import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px

st.set_page_config(page_title="Dinamika Atmosfer Global",
                   layout="wide", page_icon="🌏")

st.title("🌏 Dinamika Atmosfer Global")
st.markdown("""
Dashboard pemantauan **ENSO (Nino3.4)**, **IOD**, dan **MJO**
menggunakan data real-time dari **NOAA CPC/PSL** dan **BOM Australia (mirror GitHub)**.
""")

@st.cache_data(ttl=3600)
def fetch_text(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

@st.cache_data(ttl=3600)
def fetch_csv(url):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

# ----------------------------
# 1️⃣ ENSO (Nino 3.4) NOAA PSL
# ----------------------------
st.subheader("1️⃣ ENSO – Nino 3.4 SST Anomaly (°C)")
try:
    url_enso = "https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/nino34.long.anom.data"
    text = fetch_text(url_enso)
    # Format: header + data dalam kolom per bulan
    lines = text.splitlines()
    data_lines = [ln.split() for ln in lines if ln and ln[0].isdigit()]
    df_enso = pd.DataFrame(data_lines)
    # Struktur: Year Jan Feb ... Dec
    df_enso.columns = ["Year"] + [f"{m:02d}" for m in range(1,13)]
    df_enso = df_enso.melt(id_vars="Year", var_name="Month", value_name="Anomaly")
    df_enso["date"] = pd.to_datetime(df_enso["Year"] + "-" + df_enso["Month"],
                                     format="%Y-%m", errors="coerce")
    df_enso["Anomaly"] = pd.to_numeric(df_enso["Anomaly"], errors="coerce")
    df_enso = df_enso.dropna().sort_values("date")
    fig = px.line(df_enso.tail(120), x="date", y="Anomaly",
                  labels={"Anomaly":"°C"}, title="Nino3.4 10 Tahun Terakhir")
    st.plotly_chart(fig, use_container_width=True)
    last = df_enso.dropna().iloc[-1]
    st.info(f"Terbaru: {last['Anomaly']:.2f} °C ({last['date'].strftime('%b %Y')})")
except Exception as e:
    st.warning(f"Gagal memuat ENSO real-time: {e}")

# ----------------------------
# 2️⃣ IOD (GitHub mirror BOM)
# ----------------------------
st.subheader("2️⃣ Indian Ocean Dipole (IOD) Index (°C)")
try:
    url_iod = "https://raw.githubusercontent.com/bo-mirror/iod-index/main/weekly_iod.csv"
    iod_text = fetch_csv(url_iod)
    iod_df = pd.read_csv(io.StringIO(iod_text))
    iod_df["date"] = pd.to_datetime(iod_df["date"])
    fig = px.line(iod_df.tail(156), x="date", y="iod",
                  labels={"iod":"°C"}, title="IOD Weekly (3 Tahun Terakhir)")
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"Terbaru: {iod_df.iloc[-1]['iod']:.2f} °C ({iod_df.iloc[-1]['date'].date()})")
except Exception as e:
    st.warning(f"Gagal memuat IOD real-time: {e}")
    st.markdown("[Klik data IOD resmi BOM](https://www.bom.gov.au/climate/enso/#tabs=Indian-Ocean)")

# ----------------------------
# 3️⃣ MJO (NOAA daily_rmm)
# ----------------------------
st.subheader("3️⃣ Madden–Julian Oscillation (MJO) – RMM1 & RMM2")
try:
    url_mjo = "https://www.cpc.ncep.noaa.gov/data/indices/daily_rmm.txt"
    mjo_text = fetch_text(url_mjo)
    # Format: Year Mon Day RMM1 RMM2 Phase Amp
    colspecs = [(0,4),(5,7),(8,10),(11,18),(19,26),(27,29),(30,36)]
    mjo_df = pd.read_fwf(io.StringIO(mjo_text), colspecs=colspecs,
                         names=["YR","MO","DY","RMM1","RMM2","PHASE","AMP"])
    mjo_df["date"] = pd.to_datetime(mjo_df[["YR","MO","DY"]])
    mjo_df = mjo_df.sort_values("date")
    fig = px.line(mjo_df.tail(90), x="date", y="AMP",
                  labels={"AMP":"Amplitude"}, title="MJO Amplitude (3 Bulan Terakhir)")
    st.plotly_chart(fig, use_container_width=True)
    last = mjo_df.iloc[-1]
    st.info(f"Terbaru: Phase {last['PHASE']} | Amp {last['AMP']:.2f} ({last['date'].date()})")
except Exception as e:
    st.warning(f"Gagal memuat MJO real-time: {e}")
