import streamlit as st
import pandas as pd
import random

# -------------------------------
# CONFIGURASI HALAMAN
# -------------------------------
st.set_page_config(page_title="Dinamika Atmosfer", layout="wide")

# -------------------------------
# JUDUL APLIKASI
# -------------------------------
st.title("🌦️ Dinamika Atmosfer - Halaman Utama")
st.markdown("Masukkan nama kota untuk melihat **faktor lokal atmosfer**:")
kota = st.text_input("Contoh: Malang, Bandung, Jakarta", "Surabaya").title()

st.write("---")

# -------------------------------
# DATA DUMMY (BISA DIGANTI API)
# -------------------------------
# Cuaca real-time (dummy)
cuaca = {
    "Suhu": f"{random.randint(27, 33)} °C",
    "Kelembaban": f"{random.randint(60, 90)} %",
    "Curah Hujan": f"{random.randint(0, 20)} mm"
}

# NDVI data
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

# -------------------------------
# LAYOUT DASHBOARD
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌤️ Cuaca Saat Ini")
    for key, val in cuaca.items():
        st.write(f"**{key}:** {val}")

with col2:
    st.markdown("### 🌿 NDVI Lokal")
    st.write(f"**NDVI:** {ndvi_val} (Hijau {'tinggi' if ndvi_val >= 0.7 else 'rendah'})")
    st.progress(min(ndvi_val, 1.0))

with col3:
    st.markdown("### 🌊 ENSO & IOD Lokal")
    st.info(f"**ENSO:** {enso_local}")
    st.info(f"**IOD:** {iod_local}")

# -------------------------------
# GRAFIK HISTORI CURAH HUJAN
# -------------------------------
st.write("---")
st.markdown("### 📊 Curah Hujan 7 Hari Terakhir")
df_hujan = pd.DataFrame({"Hari": hari, "Curah Hujan (mm)": hujan_data})
st.bar_chart(df_hujan.set_index("Hari"))

# -------------------------------
# CATATAN
# -------------------------------
st.caption("⚠️ Data sementara (dummy). Data cuaca dan curah hujan akan dihubungkan dengan API atau dataset BMKG.")
