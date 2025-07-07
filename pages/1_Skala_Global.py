# File: pages/1_Skala_Global.py

import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Skala Global", layout="wide")
st.title("🌎 Skala Atmosfer Global")

st.markdown("""
Fenomena skala global memengaruhi pola cuaca secara luas hingga lintas benua dan samudra.

#### 🌊 **ENSO (El Niño Southern Oscillation)**
- Mengacu pada pemanasan (El Niño) atau pendinginan (La Niña) di Samudra Pasifik tengah dan timur.
- El Niño → potensi kekeringan di Indonesia.
- La Niña → peningkatan curah hujan.

#### 🌐 **IOD (Indian Ocean Dipole)**
- Anomali suhu laut Samudra Hindia.
- Positif → lebih kering di Indonesia.
- Negatif → lebih lembap dan hujan meningkat.
""")

st.markdown("### 🗺️ Wilayah Pengaruh Skala Global")

# Inisialisasi peta
m = folium.Map(location=[0, 120], zoom_start=3, tiles="CartoDB positron")

# Wilayah ENSO di Pasifik Tengah
enso_area = folium.Rectangle(
    bounds=[[5, -170], [-5, -120]],
    color="red",
    fill=True,
    fill_opacity=0.2,
    tooltip="Zona ENSO (El Niño/La Niña)"
).add_to(m)

# Wilayah IOD di Samudra Hindia
iod_area = folium.Rectangle(
    bounds=[[-10, 50], [10, 100]],
    color="blue",
    fill=True,
    fill_opacity=0.2,
    tooltip="Zona IOD (Indian Ocean Dipole)"
).add_to(m)

# Lokasi Indonesia (titik fokus)
folium.Marker(
    location=[-2, 118],
    tooltip="Indonesia",
    icon=folium.Icon(color="green")
).add_to(m)

st_folium(m, width=1000, height=450)

st.info("📌 Wilayah berwarna menunjukkan zona aktif ENSO dan IOD yang memengaruhi cuaca di Indonesia.")
