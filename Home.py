import streamlit as st
import pandas as pd
import requests
import io
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Dinamika Atmosfer – Home",
    layout="wide",
    page_icon="🌏"
)

st.title("🌏 Dinamika Atmosfer Global")
st.markdown(
    """
    Dashboard pemantauan **ENSO (Nino3.4)**, **IOD**, dan **MJO** 
    menggunakan data _real-time_ dari **NOAA CPC** dan **BOM Australia**.
    """
)

# ===========================
# Helper functions
# ===========================
@st.cache_data(ttl=3600)
def fetch_csv(url, skiprows=0):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text), skiprows=skiprows)

# ===========================
# 1️⃣ ENSO (Nino3.4) - NOAA CPC
# ===========================
st.subheader("1️⃣ ENSO – Nino 3.4 SST Anomaly (°C)")
try:
    enso_url = "https://www.cpc.ncep.noaa.gov/data/indices/sstoi.indices"
    df_enso = fetch_csv(enso_url, skiprows=1)
    df_enso.columns = ["YR","MON","NINO1+2","NINO3","NINO4","NINO3.4"]
    df_enso["date"] = pd.to_datetime(
        df_enso["YR"].astype(str) + "-" + df_enso["MON"].astype(str),
        format="%Y-%m"
    )
    df_enso = df_enso.sort_values("date")

    fig_enso = px.line(df_enso.tail(120), x="date", y="NINO3.4",
                       title="Anomali Nino 3.4 (10 tahun terakhir)",
                       labels={"date":"Tahun","NINO3.4":"Anomali (°C)"})
    st.plotly_chart(fig_enso, use_container_width=True)

    last_enso = df_enso.iloc[-1]
    st.info(f"📊 **Terbaru (bulan {last_enso['date'].strftime('%b %Y')})**: "
            f"{last_enso['NINO3.4']:.2f} °C")
except Exception as e:
    st.error(f"Gagal memuat ENSO data: {e}")

# ===========================
# 2️⃣ Indian Ocean Dipole (IOD) - BOM Australia
# ===========================
st.subheader("2️⃣ Indian Ocean Dipole (IOD) Index (°C)")
try:
    iod_url = "https://www.bom.gov.au/climate/enso/indices/weekly.iod.index.csv"
    df_iod = fetch_csv(iod_url)
    df_iod["Date"] = pd.to_datetime(df_iod["Year"].astype(str) + df_iod["Week"].astype(str) + '1',
                                    format='%Y%U%w')  # Sunday as start
    df_iod = df_iod.sort_values("Date")

    fig_iod = px.line(df_iod.tail(260), x="Date", y="IOD",
                      title="IOD Mingguan (5 tahun terakhir)",
                      labels={"Date":"Tahun","IOD":"IOD (°C)"})
    st.plotly_chart(fig_iod, use_container_width=True)

    last_iod = df_iod.iloc[-1]
    st.info(f"📊 **Terbaru (minggu ke-{int(last_iod['Week'])}, {int(last_iod['Year'])})**: "
            f"{last_iod['IOD']:.2f} °C")
except Exception as e:
    st.error(f"Gagal memuat IOD data: {e}")

# ===========================
# 3️⃣ Madden–Julian Oscillation (MJO) – RMM Index
# ===========================
st.subheader("3️⃣ Madden–Julian Oscillation (MJO) – RMM1 & RMM2")
try:
    # NOAA menyediakan RMM daily
    mjo_url = "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_mjo_index/projRMM.74toRealtime.txt"
    r = requests.get(mjo_url, timeout=30)
    r.raise_for_status()
    raw = [x.split() for x in r.text.splitlines() if not x.startswith("#")]
    df_mjo = pd.DataFrame(raw, columns=["year","month","day","RMM1","RMM2","phase","amplitude"])
    df_mjo = df_mjo.astype({"year":int,"month":int,"day":int,
                            "RMM1":float,"RMM2":float,"phase":int,"amplitude":float})
    df_mjo["date"] = pd.to_datetime(df_mjo[["year","month","day"]])
    df_mjo = df_mjo.sort_values("date")

    fig_mjo = px.line(df_mjo.tail(90), x="date", y="amplitude",
                      title="Amplitudo MJO (90 hari terakhir)",
                      labels={"date":"Tanggal","amplitude":"Amplitude"})
    st.plotly_chart(fig_mjo, use_container_width=True)

    last_mjo = df_mjo.iloc[-1]
    st.info(
        f"📊 **Terbaru ({last_mjo['date'].strftime('%d %b %Y')})**: "
        f"Phase {last_mjo['phase']} | Amplitudo {last_mjo['amplitude']:.2f}"
    )
except Exception as e:
    st.error(f"Gagal memuat MJO data: {e}")

# ===========================
# Footer
# ===========================
st.markdown("---")
st.caption(
    "Data: [NOAA CPC](https://www.cpc.ncep.noaa.gov/) & "
    "[BOM Australia](https://www.bom.gov.au/). "
    "Update otomatis setiap refresh (cache 1 jam)."
)
