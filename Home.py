import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random

# -------------------------------
# Fungsi Ambil Data PM dari BMKG
# -------------------------------
def get_pm_data():
    url = "https://pm.meteojuanda.id"
    pm25 = None
    pm10 = None

    try:
        # 1️⃣ Coba cari endpoint JSON terlebih dahulu
        json_url = url + "/api/data/latest"
        try:
            resp_json = requests.get(json_url, timeout=5)
            if resp_json.status_code == 200:
                data = resp_json.json()
                # Sesuaikan key JSON sesuai struktur API
                pm25 = data.get("PM25") or data.get("pm25") or None
                pm10 = data.get("PM10") or data.get("pm10") or None
                if pm25 and pm10:
                    return float(pm25), float(pm10)
        except:
            pass

        # 2️⃣ Jika JSON tidak ada, fallback ke scraping HTML
        resp_html = requests.get(url, timeout=10)
        if resp_html.status_code == 200:
            soup = BeautifulSoup(resp_html.text, "html.parser")
            # Ganti selector sesuai hasil inspeksi HTML
            pm25_elem = soup.find("span", {"id": "pm25_value"})
            pm10_elem = soup.find("span", {"id": "pm10_value"})

            pm25 = pm25_elem.text.strip() if pm25_elem else None
            pm10 = pm10_elem.text.strip() if pm10_elem else None

            if pm25:
                pm25 = float(pm25.replace(",", "."))
            if pm10:
                pm10 = float(pm10.replace(",", "."))

    except Exception as e:
        print("Error get_pm_data:", e)

    return pm25, pm10

# -------------------------------
# Konfigurasi Halaman
# -------------------------------
st.set_page_config(page_title="Dinamika Atmosfer", layout="wide")
st.title("🌦️ Dinamika Atmosfer")
st.markdown("Masukkan nama kota untuk melihat **faktor atmosfer skala Lokal, Regional, dan Global:**")
kota = st.text_input("Contoh: Surabaya, Sidoarjo, Malang", "Surabaya").title()
st.write("---")

# -------------------------------
# DATA DUMMY (sementara)
# -------------------------------
ndvi_val = round(random.uniform(0.5, 0.9), 2)
curah_hujan = random.randint(0, 20)
anomali_suhu = random.choice([-1, 0, 1, 2])

# Regional
mjo_phase = random.choice(["Inaktif", "Aktif di fase 3", "Aktif di fase 5"])
itcz_pos = random.choice(["Selatan Jawa", "Utara Kalimantan", "Tidak signifikan"])

# Global
enso = random.choice(["Netral", "El Niño Lemah", "La Niña Lemah"])
iod = random.choice(["Netral", "Positif", "Negatif"])

# -------------------------------
# 3 KOLOM SKALA
# -------------------------------
col1, col2, col3 = st.columns(3)

# -------------------------------
# SKALA LOKAL
# -------------------------------
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

    # Jika kota Sidoarjo atau Surabaya → ambil data PM
    if kota in ["Surabaya", "Sidoarjo"]:
        pm25, pm10 = get_pm_data()
        if pm25 and pm10:
            st.write(f"**PM2.5:** {pm25} µg/m³")
            st.write(f"**PM10:** {pm10} µg/m³")
            if pm25 < 25 and pm10 < 50:
                st.success("Kualitas udara: Baik")
            elif pm25 < 50 and pm10 < 100:
                st.warning("Kualitas udara: Sedang")
            else:
                st.error("Kualitas udara: Tidak Sehat")
        else:
            st.warning("⚠️ Data kualitas udara BMKG tidak dapat diakses saat ini.")

# -------------------------------
# SKALA REGIONAL
# -------------------------------
with col2:
    st.subheader("🌎 Skala Regional")
    st.write(f"**MJO:** {mjo_phase}")
    st.write(f"**Posisi ITCZ:** {itcz_pos}")
    st.write("**Status Hujan Regional:** Normal")

# -------------------------------
# SKALA GLOBAL
# -------------------------------
with col3:
    st.subheader("🌐 Skala Global")
    st.write(f"**ENSO:** {enso}")
    st.write(f"**IOD:** {iod}")
    st.write("**SST Anomali:** +0.5°C (dummy)")

# -------------------------------
# NARASI FENOMENA TERKINI
# -------------------------------
st.write("---")
st.markdown("### 📝 Fenomena Atmosfer Terkini")

narasi = f"Beberapa hari terakhir, {kota} mengalami curah hujan {curah_hujan} mm per hari. "
if anomali_suhu > 0:
    narasi += f"Suhu rata-rata {anomali_suhu}°C lebih tinggi dari normal. "
elif anomali_suhu < 0:
    narasi += f"Suhu rata-rata {abs(anomali_suhu)}°C lebih rendah dari normal. "

if kota in ["Surabaya", "Sidoarjo"]:
    if pm25 and pm10:
        narasi += f"Kualitas udara menunjukkan PM2.5={pm25} µg/m³ dan PM10={pm10} µg/m³. "

narasi += f"Secara regional, {mjo_phase}, ITCZ berada di {itcz_pos}. Fenomena global menunjukkan ENSO {enso} dan IOD {iod}."

st.info(narasi)
