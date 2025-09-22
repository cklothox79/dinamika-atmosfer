import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import StringIO
import plotly.graph_objects as go

st.set_page_config(page_title="🌏 Dinamika Atmosfer Global", layout="wide")
st.title("🌏 Dinamika Atmosfer Global")
st.markdown("""
Dashboard pemantauan **ENSO (Nino3.4)**, **IOD**, dan **MJO**  
Data real-time dari **NOAA CPC** dan **BOM Australia** *(otomatis fallback jika sumber asli gagal)*.
""")

# ---------------------- 🔵 Utility untuk ambil data dengan fallback ----------------------
def fetch_csv_with_fallback(url_primary, url_fallback=None, names=None):
    """
    Ambil CSV dari url_primary. Jika gagal, coba url_fallback (jika ada).
    """
    try:
        r = requests.get(url_primary, timeout=10)
        r.raise_for_status()
        df = pd.read_csv(StringIO(r.text), names=names)
        return df, "✅ Data asli NOAA/BOM"
    except Exception as e:
        if url_fallback:
            try:
                r = requests.get(url_fallback, timeout=10)
                r.raise_for_status()
                df = pd.read_csv(StringIO(r.text), names=names)
                return df, "⚠️ Gagal sumber asli → Fallback GitHub"
            except Exception as e2:
                return None, f"❌ Gagal semua sumber: {e2}"
        else:
            return None, f"❌ Gagal memuat data: {e}"

# ---------------------- 1️⃣ ENSO – Nino 3.4 ----------------------
st.subheader("1️⃣ ENSO – Nino 3.4 SST Anomaly (°C)")
enso_url = "https://www.cpc.ncep.noaa.gov/data/indices/wksst8110.for"
enso_fallback = "https://raw.githubusercontent.com/NOAA-PSL/psl-data/main/enso_nino34_weekly.csv"

try:
    # Data asli NOAA berformat fixed-width, perlu parsing manual
    r = requests.get(enso_url, timeout=10)
    r.raise_for_status()
    raw = r.text
    # Cari baris dengan data (skip header)
    lines = [x for x in raw.splitlines() if x.strip() and x[0].isdigit()]
    data = []
    for l in lines:
        yr = int(l[:4])
        wk = int(l[5:7])
        n34 = float(l[48:53])  # kolom Nino3.4
        data.append([f"{yr}-W{wk:02d}", n34])
    enso_df = pd.DataFrame(data, columns=["Week", "Nino3.4"])
    status_enso = "✅ Data asli NOAA CPC"
except Exception as e:
    # Fallback CSV GitHub
    enso_df, status_enso = fetch_csv_with_fallback(enso_fallback)

if enso_df is not None:
    st.caption(status_enso)
    fig_enso = go.Figure()
    fig_enso.add_trace(go.Scatter(x=enso_df["Week"], y=enso_df["Nino3.4"],
                                  mode="lines", name="Nino3.4 SST Anomaly"))
    fig_enso.update_layout(title="Weekly Nino3.4 SST Anomaly (°C)",
                           xaxis_title="Minggu", yaxis_title="Anomali (°C)",
                           height=400)
    st.plotly_chart(fig_enso, use_container_width=True)
else:
    st.error(status_enso)

# ---------------------- 2️⃣ Indian Ocean Dipole (IOD) ----------------------
st.subheader("2️⃣ Indian Ocean Dipole (IOD) Index (°C)")
st.markdown("""
⚠️ **Data CSV BOM** saat ini sering *403 Forbidden*.  
Silakan akses langsung di:
👉 [BOM IOD Weekly Data](https://www.bom.gov.au/climate/enso/indices/weekly.iod.index.csv)
""")

# ---------------------- 3️⃣ Madden–Julian Oscillation (MJO) ----------------------
st.subheader("3️⃣ Madden–Julian Oscillation (MJO) – RMM1 & RMM2")
mjo_url = "https://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_mjo_index/projRMM.74toRealtime.txt"
mjo_fallback = "https://raw.githubusercontent.com/NOAA-PSL/psl-data/main/mjo_rmm.csv"

def parse_mjo_noaa(text):
    """
    Format asli NOAA MJO (projRMM.74toRealtime.txt)
    Kolom: year, month, day, RMM1, RMM2, phase, amplitude
    """
    data = []
    for line in text.splitlines():
        if line.strip() and line[0].isdigit():
            parts = line.split()
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
except Exception as e:
    mjo_df, status_mjo = fetch_csv_with_fallback(mjo_fallback)

if mjo_df is not None and not mjo_df.empty:
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
else:
    st.error(status_mjo)

# ---------------------- Footer ----------------------
st.markdown("---")
st.caption("Data sumber: [NOAA CPC](https://www.cpc.ncep.noaa.gov/) | [BOM Australia](https://www.bom.gov.au/) | Fallback: GitHub PSL Data")
