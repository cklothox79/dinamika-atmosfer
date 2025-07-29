import streamlit as st
import pandas as pd
import random

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Dinamika Atmosfer", layout="wide")
st.title("🌦️ Dinamika Atmosfer")
st.markdown("Masukkan nama kota untuk melihat **faktor atmosfer skala Lokal, Regional, dan Global**:")

kota = st.text_input("Contoh: Surabaya, Sidoarjo, Malang", "Surabaya").title()
st.write("---")

# -------------------------------
# DATA DUMMY
# -------------------------------
# Lokal
ndvi_val = round(random.uniform(0.5, 0.9), 2)
curah_hujan = random.randint(0, 20)
anomali_suhu = random.choice([-1, 0, 1, 2])
pm25 = pm10 = None

# Dummy PM2.5 & PM10 hanya untuk Surabaya dan Sidoarjo
if kota in ["Surabaya", "Sidoarjo"]:
    pm25 = random.randint(10, 80)
    pm10 = random.randint(20, 150)

# Regional (dummy)
mjo_phase = random.choice(["Inaktif", "Aktif di fase 3", "Aktif di fase 5"])
itcz_pos = random.choice(["Selatan Jawa", "Utara Kalimantan", "Tidak signifikan"])

# Global (dummy)
enso = random.choice(["Netral", "El Niño Lemah", "La Niña Lemah"])
iod = random.choice(["Netral", "Positif", "Negatif"])

# -------------------------------
# 3 KOLOM SKALA
# -------------------------------
col1, col2, col3 = st.columns(3)

# Skala Lokal
with col1:
    st.subheader("🏠 Skala Lokal")
    st.write(f"**NDVI:** {ndvi_val}")
    st.write(f"**Curah Hujan:** {curah_hujan} mm")
    if anomali_suhu > 0:
        st.error(f"Anomali suhu: +{anomali_suhu}°C di atas normal")
    elif anomali_suhu < 0:
        st.warning(f"Anomali suhu: {anomali_suhu}°C di bawah normal")
    else:
        st.success("Suhu normal")
    
    # PM2.5 & PM10 jika kota Sidoarjo atau Surabaya
    if pm25 is not None:
        st.write(f"**PM2.5:** {pm25} µg/m³")
        st.write(f"**PM10:** {pm10} µg/m³")
        if pm25 < 25 and pm10 < 50:
            st.success("Kualitas udara: Baik")
        elif pm25 < 50 and pm10 < 100:
            st.warning("Kualitas udara: Sedang")
        else:
            st.error("Kualitas udara: Tidak Sehat")

# Skala Regional
with col2:
    st.subheader("🌎 Skala Regional")
    st.write(f"**MJO:** {mjo_phase}")
    st.write(f"**Posisi ITCZ:** {itcz_pos}")
    st.write("**Status Hujan Regional:** Normal")

# Skala Global
with col3:
    st.subheader("🌐 Skala Global")
    st.write(f"**ENSO:** {enso}")
    st.write(f"**IOD:** {iod}")
    st.write("**SST Anomali:** +0.5°C (dummy)")

# -------------------------------
# PENJELASAN FENOMENA TERBARU
# -------------------------------
st.write("---")
st.markdown("### 📝 Fenomena Atmosfer Terkini")

narasi = f"Beberapa hari terakhir, {kota} mengalami kondisi cuaca dengan curah hujan {curah_hujan} mm per hari. "
if anomali_suhu > 0:
    narasi += f"Suhu rata-rata {anomali_suhu}°C lebih tinggi dari normal. "
elif anomali_suhu < 0:
    narasi += f"Suhu rata-rata {abs(anomali_suhu)}°C lebih rendah dari normal. "

if pm25 is not None:
    narasi += f"Kualitas udara terpantau PM2.5={pm25} µg/m³ dan PM10={pm10} µg/m³. "

narasi += f"Secara regional, {mjo_phase}, ITCZ berada di {itcz_pos}. Fenomena global menunjukkan ENSO {enso} dan IOD {iod}."

st.info(narasi)
