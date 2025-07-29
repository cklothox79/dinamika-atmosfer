import streamlit as st
import pandas as pd
import random
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

# -------------------------------
# CONFIGURASI HALAMAN
# -------------------------------
st.set_page_config(page_title="Dinamika Atmosfer", layout="wide")

# -------------------------------
# INPUT NAMA KOTA
# -------------------------------
st.title("🌦️ Dinamika Atmosfer - Halaman Utama")
st.markdown("Masukkan nama kota untuk melihat **faktor lokal atmosfer**:")
kota = st.text_input("Contoh: Malang, Bandung, Jakarta", "Surabaya").title()
st.write("---")

# -------------------------------
# DATA DUMMY
# -------------------------------
cuaca = {
    "Suhu": random.randint(27, 33),
    "Kelembaban": random.randint(60, 90),
    "Curah Hujan": random.randint(0, 20)
}

# Data NDVI
try:
    df_ndvi = pd.read_csv("ndvi_kota_besar_indo_jun2023.csv")
    ndvi_val = df_ndvi[df_ndvi['kota'].str.lower() == kota.lower()]['ndvi'].values[0]
except:
    ndvi_val = round(random.uniform(0.5, 0.9), 2)

# ENSO & IOD lokal (dummy)
enso_local = "Netral – faktor lokal lebih berperan."
iod_local = "Netral – tidak berdampak signifikan."

# Histori curah hujan (dummy 7 hari)
hujan_data = [random.randint(0, 30) for _ in range(7)]
hari = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]

# Anomali suhu (dummy)
suhu_normal = 30
anomali_suhu = cuaca["Suhu"] - suhu_normal

# -------------------------------
# LAYOUT DASHBOARD
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌤️ Cuaca Saat Ini")
    st.write(f"**Suhu:** {cuaca['Suhu']} °C")
    st.write(f"**Kelembaban:** {cuaca['Kelembaban']} %")
    st.write(f"**Curah Hujan:** {cuaca['Curah Hujan']} mm")

with col2:
    st.markdown("### 🌿 NDVI Lokal")
    st.write(f"**NDVI:** {ndvi_val} (Hijau {'tinggi' if ndvi_val >= 0.7 else 'rendah'})")
    st.progress(min(ndvi_val, 1.0))

with col3:
    st.markdown("### 🌊 ENSO & IOD Lokal")
    st.info(f"**ENSO:** {enso_local}")
    st.info(f"**IOD:** {iod_local}")

st.write("---")
st.markdown("### 📊 Curah Hujan 7 Hari Terakhir")
df_hujan = pd.DataFrame({"Hari": hari, "Curah Hujan (mm)": hujan_data})
st.bar_chart(df_hujan.set_index("Hari"))

# -------------------------------
# ANOMALI SUHU
# -------------------------------
st.write("---")
st.markdown("### 🌡️ Anomali Suhu Lokal")
if anomali_suhu > 0:
    st.error(f"Suhu lebih tinggi {anomali_suhu}°C dari normal ({suhu_normal}°C).")
elif anomali_suhu < 0:
    st.warning(f"Suhu lebih rendah {abs(anomali_suhu)}°C dari normal ({suhu_normal}°C).")
else:
    st.success("Suhu berada pada kisaran normal.")

# -------------------------------
# MINI MAP LOKASI
# -------------------------------
st.write("---")
st.markdown("### 🗺️ Lokasi Kota")

geolocator = Nominatim(user_agent="geoapi")
location = geolocator.geocode(kota)

if location:
    map_center = [location.latitude, location.longitude]
    m = folium.Map(location=map_center, zoom_start=11)
    folium.Marker(map_center, popup=kota).add_to(m)
    st_folium(m, width=700, height=400)
else:
    st.warning("Lokasi kota tidak ditemukan.")

# -------------------------------
# CATATAN
# -------------------------------
st.caption("⚠️ Data sementara (dummy). Data cuaca, curah hujan, dan anomali suhu akan dihubungkan dengan API BMKG/OpenWeather.")
