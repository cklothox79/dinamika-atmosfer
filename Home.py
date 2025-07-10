import streamlit as st
import requests
import pandas as pd
from io import StringIO
from geopy.geocoders import Nominatim
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Dinamika Atmosfer", layout="wide")
st.title("🌏 Dinamika Atmosfer - Halaman Utama")

# =======================
# Input Nama Kota
# =======================
st.subheader("📍 Masukkan Nama Kota")
location_name = st.text_input("Contoh: Malang, Bandung, Jakarta")

lat, lon = None, None
if location_name:
    try:
        geolocator = Nominatim(user_agent="dinamika-atmosfer")
        location = geolocator.geocode(location_name)
        if location:
            lat, lon = location.latitude, location.longitude
            st.success(f"{location.address} | Koordinat: {lat:.3f}, {lon:.3f}")
        else:
            st.error("❌ Lokasi tidak ditemukan.")
    except:
        st.error("❌ Gagal mengakses layanan geocoding.")

# =======================
# Fetch ENSO
# =======================
def fetch_enso_data():
    url = "https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        raw = response.text
        lines = raw.strip().split('\n')[1:]
        df = pd.read_csv(StringIO('\n'.join(lines)), delim_whitespace=True)
        last_row = df.iloc[-1]
        season = last_row['SEAS']
        oni = last_row.iloc[-1]

        if oni >= 0.5:
            phase = "El Niño"
        elif oni <= -0.5:
            phase = "La Niña"
        else:
            phase = "Netral"

        return {"oni": oni, "season": season, "phase": phase}
    except:
        return None

# =======================
# Fetch IOD
# =======================
def fetch_iod_data():
    url = "https://www.bom.gov.au/climate/enso/indices/archive/iod.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        raw = response.text
        lines = raw.strip().split('\n')
        data_lines = [line for line in lines if line and line[0].isdigit()]
        df = pd.read_csv(StringIO('\n'.join(data_lines)), delim_whitespace=True)
        last_row = df.iloc[-1]
        iod = last_row['IOD']
        date = f"{int(last_row['Year'])}-{int(last_row['Month']):02d}"

        if iod >= 0.4:
            phase = "IOD Positif"
        elif iod <= -0.4:
            phase = "IOD Negatif"
        else:
            phase = "IOD Netral"

        return {"iod": iod, "date": date, "phase": phase}
    except:
        return None

# =======================
# Tampilkan ENSO & IOD
# =======================
st.subheader("🌊 Status Global: ENSO & IOD (Real-Time)")

col1, col2 = st.columns(2)
enso = fetch_enso_data()
iod = fetch_iod_data()

with col1:
    if enso:
        st.metric("ENSO (ONI)", f"{enso['oni']:.2f}", delta=enso["phase"])
        st.caption(f"Musim: {enso['season']}")
    else:
        st.error("❌ Gagal memuat data ENSO.")

with col2:
    if iod:
        st.metric("IOD Index", f"{iod['iod']:.2f}", delta=iod["phase"])
        st.caption(f"Bulan: {iod['date']}")
    else:
        st.error("❌ Gagal memuat data IOD.")

# =======================
# Deteksi Skala Atmosfer
# =======================
if lat and lon:
    st.markdown("---")
    st.subheader(f"📡 Skala Atmosfer yang Aktif di Sekitar **{location_name.title()}**")

    aktif = {
        "ENSO": enso["phase"] if enso else "Tidak Terdeteksi",
        "IOD": iod["phase"] if iod else "Tidak Terdeteksi",
        "MJO": "Aktif (fase 3-4)",  # Placeholder sementara
    }

    signifikan = [s for s in aktif.values() if "Netral" not in s and "Tidak" not in s]

    if signifikan:
        for skala, status in aktif.items():
            st.write(f"- **{skala}**: {status}")
    else:
        st.info("ℹ️ Tidak ada skala atmosfer signifikan yang terdeteksi saat ini.")

# =======================
# Timeline Dummy
# =======================
if lat and lon:
    st.subheader("📅 Timeline Indeks Skala Atmosfer (Simulasi)")

    dates = pd.date_range(end=datetime.today(), periods=12, freq='M')
    dummy_enso = [0.4, 0.6, 0.8, 1.0, 0.7, 0.5, 0.2, -0.1, -0.3, -0.5, -0.4, -0.2]
    dummy_iod = [0.1, 0.3, 0.5, 0.6, 0.4, 0.1, -0.1, -0.3, -0.5, -0.2, 0.0, 0.2]
    dummy_mjo = [1, 2, 3, 5, 6, 4, 3, 2, 1, 0, 0, 1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=dummy_enso, name="ENSO (ONI)"))
    fig.add_trace(go.Scatter(x=dates, y=dummy_iod, name="IOD Index"))
    fig.add_trace(go.Scatter(x=dates, y=dummy_mjo, name="Fase MJO", yaxis="y2"))

    fig.update_layout(
        title="Timeline Skala Atmosfer 12 Bulan Terakhir (Contoh)",
        xaxis_title="Bulan",
        yaxis=dict(title="ENSO / IOD"),
        yaxis2=dict(title="MJO Fase", overlaying="y", side="right"),
        legend=dict(orientation="h", y=-0.3),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

# =======================
# Mode Edukasi Interaktif
# =======================
with st.expander("🎓 Penjelasan Skala Atmosfer (Klik untuk lihat)"):
    st.markdown("""
    ### 🌀 ENSO (El Niño–Southern Oscillation)
    - **El Niño**: Pemanasan suhu laut Pasifik timur dan tengah → mengurangi hujan di Indonesia.
    - **La Niña**: Pendinginan suhu laut Pasifik → meningkatkan hujan di Indonesia.
    
    ### 🌊 IOD (Indian Ocean Dipole)
    - **IOD Positif**: Samudra Hindia barat lebih hangat → musim kemarau lebih kering.
    - **IOD Negatif**: Samudra Hindia timur lebih hangat → hujan meningkat di wilayah barat Indonesia.

    ### ☁️ MJO (Madden-Julian Oscillation)
    - Gelombang konveksi tropis yang berpindah dari barat ke timur.
    - Memengaruhi hujan 1–2 minggu ke depan tergantung fase dan lokasi.

    ### 🌐 Gelombang Kelvin dan Rossby
    - Gelombang atmosfer tropis yang berperan dalam pola tekanan, angin, dan hujan.
    """)
    st.image("https://www.bom.gov.au/climate/enso/history/enso-animation.gif",
             caption="Animasi ENSO - Sumber: BOM Australia", use_column_width=True)
