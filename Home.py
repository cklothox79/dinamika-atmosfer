import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# -------------------------------------------------------
# 🔄 Auto Refresh setiap 30 menit (1800 detik)
# -------------------------------------------------------
st_autorefresh(interval=1800 * 1000, key="data_refresh")

# -------------------------------------------------------
# Konfigurasi Halaman
# -------------------------------------------------------
st.set_page_config(page_title="🌏 Dinamika Atmosfer Global", layout="wide")
st.title("🌏 Dinamika Atmosfer Global")
st.markdown("""
Dashboard pemantauan **ENSO (Nino3.4)**, **IOD**, dan **MJO**  
Menggunakan data real-time dari **NOAA CPC** & **BOM Australia** (otomatis fallback jika gagal).
""")
st.write("---")


# -------------------------------------------------------
# 1️⃣ ENSO – Nino 3.4 SST Anomaly
# -------------------------------------------------------
st.subheader("1️⃣ ENSO – Nino 3.4 SST Anomaly (°C)")
enso_url = "https://psl.noaa.gov/gcos_wgsp/Timeseries/Data/nino34.long.anom.data"

def parse_enso_noaa(text):
    df_list = []
    lines = text.splitlines()
    months = lines[1].split()
    for line in lines[2:]:
        parts = line.split()
        if len(parts) >= 13:
            year = parts[0]
            vals = parts[1:13]
            for m, v in zip(months, vals):
                try:
                    df_list.append([
                        datetime.strptime(f"{year}-{m}", "%Y-%b"),
                        float(v)
                    ])
                except:
                    pass
    return pd.DataFrame(df_list, columns=["Date", "Anomaly"])

try:
    r = requests.get(enso_url, timeout=10)
    r.raise_for_status()
    enso_df = parse_enso_noaa(r.text)
    enso_df = enso_df.tail(36)  # 3 tahun terakhir
    status_enso = "✅ Data asli NOAA CPC"
except Exception as e:
    enso_df = pd.DataFrame({
        "Date": pd.date_range("2022-01-01", periods=36, freq="M"),
        "Anomaly": np.random.uniform(-1, 1, 36)
    })
    status_enso = f"⚠️ Gagal ENSO asli → Dummy digunakan"

st.caption(status_enso)
fig_enso = go.Figure()
fig_enso.add_trace(go.Scatter(x=enso_df["Date"], y=enso_df["Anomaly"],
                              mode="lines+markers", name="Nino3.4"))
fig_enso.update_layout(title="ENSO Nino3.4 SST Anomaly (°C)",
                       xaxis_title="Tanggal", yaxis_title="Anomali (°C)",
                       height=400)
st.plotly_chart(fig_enso, use_container_width=True)


# -------------------------------------------------------
# 2️⃣ Indian Ocean Dipole (IOD)
# -------------------------------------------------------
st.subheader("2️⃣ Indian Ocean Dipole (IOD) Index (°C)")
st.warning("⚠️ Data CSV BOM saat ini sering 403 Forbidden.\n"
           "Silakan akses langsung di: "
           "[👉 BOM IOD Weekly Data](https://www.bom.gov.au/climate/enso/indices/weekly.iod.index.shtml)")


# -------------------------------------------------------
# 3️⃣ Madden–Julian Oscillation (MJO)
# -------------------------------------------------------
st.subheader("3️⃣ Madden–Julian Oscillation (MJO) – RMM1 & RMM2")
mjo_url = "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_mjo_index/projRMM.74toRealtime.txt"
mjo_fallback = "https://psl.noaa.gov/mjo/mjoindex/projRMM.74toRealtime.txt"

def parse_mjo_noaa(text):
    data = []
    for line in text.splitlines():
        if line.strip() and line[0].isdigit():
            parts = line.split()
            if len(parts) >= 5:
                try:
                    date = f"{parts[0]}-{parts[1]}-{parts[2]}"
                    rmm1 = float(parts[3])
                    rmm2 = float(parts[4])
                    data.append([date, rmm1, rmm2])
                except:
                    pass
    return pd.DataFrame(data, columns=["Date","RMM1","RMM2"])

try:
    r = requests.get(mjo_url, timeout=10)
    r.raise_for_status()
    mjo_df = parse_mjo_noaa(r.text)
    status_mjo = "✅ Data asli NOAA CPC"
except Exception:
    try:
        r = requests.get(mjo_fallback, timeout=10)
        r.raise_for_status()
        mjo_df = parse_mjo_noaa(r.text)
        status_mjo = "⚠️ Gagal sumber asli → Fallback PSL NOAA"
    except:
        dates = pd.date_range("2025-01-01", periods=30, freq="D")
        mjo_df = pd.DataFrame({
            "Date": dates.strftime("%Y-%m-%d"),
            "RMM1": np.sin(np.linspace(0,6,30)),
            "RMM2": np.cos(np.linspace(0,6,30))
        })
        status_mjo = "❌ Gagal semua sumber → Dummy digunakan"

st.caption(status_mjo)
fig_mjo = go.Figure()
fig_mjo.add_trace(go.Scatter(x=mjo_df["Date"], y=mjo_df["RMM1"],
                             mode="lines", name="RMM1"))
fig_mjo.add_trace(go.Scatter(x=mjo_df["Date"], y=mjo_df["RMM2"],
                             mode="lines", name="RMM2"))
fig_mjo.update_layout(title="MJO RMM1 & RMM2 Index",
                      xaxis_title="Tanggal", yaxis_title="Index",
                      height=400)
st.plotly_chart(fig_mjo, use_container_width=True)

# -------------------------------------------------------
# Footer
# -------------------------------------------------------
st.write("---")
st.caption("Data sumber: [NOAA CPC](https://www.cpc.ncep.noaa.gov/) | "
           "[BOM Australia](https://www.bom.gov.au/) | Fallback: NOAA PSL")
