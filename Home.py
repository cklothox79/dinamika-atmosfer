# File: Home.py (Versi dengan Tampilan Lebih Menarik)

import streamlit as st
from datetime import datetime
import folium
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Skala Atmosfer Aktif", layout="wide")

# ===== Header =====
st.markdown("""
<div style='text-align: center; padding: 10px 0;'>
    <h1 style='color: #0a58ca;'>🌀 <b>SKALA ATMOSFER AKTIF SAAT INI</b></h1>
    <h5><i>Editor: Ferri Kusuma (STMKG/M8TB_14.22.0003)</i></h5>
</div>
""", unsafe_allow_html=True)

# === Inisialisasi lokasi ===
latlon_dict = {
    "Malang": (-7.98, 112.63),
    "Surabaya": (-7.25, 112.75),
    "Sidoarjo": (-7.45, 112.70),
    "Jember": (-8.17, 113.70)
}
if 'clicked_latlon' not in st.session_state:
    st.session_state.clicked_latlon = None

# === Layout Utama ===
col1, col2 = st.columns([1.5, 1.0])

with col1:
    st.markdown("### 🏙️ Masukkan Nama Kota atau Klik Peta")
    kota_input = st.text_input("", "Malang").strip().title()

    kota = kota_input
    lat, lon = None, None
    lokasi_dari_peta = False

    if st.session_state.clicked_latlon:
        lat, lon = st.session_state.clicked_latlon
        kota = "Lokasi Kustom"
        lokasi_dari_peta = True
    elif kota in latlon_dict:
        lat, lon = latlon_dict[kota]
    else:
        st.warning("🌐 Kota tidak tersedia. Pilih: " + ", ".join(latlon_dict.keys()))

    st.markdown(f"<h4>📍 Kota yang dipilih: <code>{kota}</code></h4>", unsafe_allow_html=True)

    if lat and lon:
        # ==== PETA ====
        st.markdown("### 🗺️ Lokasi di Peta")
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon], tooltip=kota, icon=folium.Icon(color='blue')).add_to(m)
        folium.Circle(radius=400000, location=[lat, lon], color="cyan", fill=True, fill_opacity=0.05).add_to(m)
        components.html(m._repr_html_(), height=350)

        # ==== INFO GLOBAL ====
        with st.container():
            st.markdown("### 🌐 Indeks Atmosfer Global Saat Ini")
            enso_index, iod_index = -0.6, -0.5
            enso_status = "La Niña" if enso_index <= -0.5 else "El Niño" if enso_index >= 0.5 else "Netral"
            iod_status = "Negatif" if iod_index <= -0.4 else "Positif" if iod_index >= 0.4 else "Netral"

            colg1, colg2 = st.columns(2)
            colg1.metric(label="🌀 ENSO Index", value=f"{enso_index}", delta=enso_status)
            colg2.metric(label="🌊 IOD Index", value=f"{iod_index}", delta=iod_status)

        # ==== DURASI AKTIF ====
        st.markdown("### ⏱️ Durasi Skala Atmosfer Aktif")
        skala_durasi = {
            "MJO Fase 4": ("2025-07-01", "2025-07-10"),
            "IOD Negatif": ("2025-06-20", "2025-08-15"),
            "La Niña": ("2025-06-15", "2025-08-31"),
            "Gelombang Kelvin": ("2025-07-05", "2025-07-08"),
        }
        for skala, (mulai, selesai) in skala_durasi.items():
            mulai_fmt = datetime.strptime(mulai, "%Y-%m-%d").strftime("%d %B %Y")
            selesai_fmt = datetime.strptime(selesai, "%Y-%m-%d").strftime("%d %B %Y")
            st.markdown(f"- ⏳ **{skala}** → *{mulai_fmt} s.d. {selesai_fmt}*")

        # ==== TIMELINE ====
        st.markdown("### 📈 Grafik Timeline")
        df_durasi = [
            {"Skala": nama, "Mulai": datetime.strptime(start, "%Y-%m-%d"), "Selesai": datetime.strptime(end, "%Y-%m-%d")}
            for nama, (start, end) in skala_durasi.items()
        ]
        df = pd.DataFrame(df_durasi)
        fig = px.timeline(df, x_start="Mulai", x_end="Selesai", y="Skala", color="Skala")
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            height=450,
            width=950,
            margin=dict(l=10, r=10, t=40, b=40),
            plot_bgcolor="#f8f9fa"
        )
        st.plotly_chart(fig, use_container_width=False)

        st.divider()

        wilayah_dipengaruhi = ["Malang", "Surabaya", "Sidoarjo", "Jember"]
        if kota in wilayah_dipengaruhi or lokasi_dari_peta:
            st.success("✅ Wilayah ini sedang dipengaruhi oleh:")
            st.markdown("""
            - 🌐 **MJO aktif fase 4**
            - 🌊 **IOD negatif**
            - 💧 **La Niña ringan**
            - 🌬️ **Kelvin Wave**
            """)
        else:
            st.info("ℹ️ Tidak ada skala atmosfer signifikan yang terdeteksi saat ini.")
    else:
        st.warning("⚠️ Data lokasi belum tersedia. Silakan isi nama kota atau klik lokasi di peta.")

# === Panel Penjelasan (Kolom Kanan) ===
with col2:
    st.markdown("### 📘 Penjelasan Skala Atmosfer")

    st.markdown("#### 🌌 Skala Global")
    with st.expander("🔍 Penjelasan"):
        st.markdown("""
        - **El Niño / La Niña**: Gangguan suhu laut Pasifik → pengaruh besar terhadap musim hujan.
        - **IOD**: Anomali suhu Samudra Hindia. Positif = kering, Negatif = basah.
        - **MJO**: Gangguan konvektif bergerak ke timur → memicu hujan fase tertentu.
        """)

    st.markdown("#### 🌍 Skala Regional")
    with st.expander("🔍 Penjelasan"):
        st.markdown("""
        - **Gelombang Kelvin**: Gelombang tropis → memicu hujan sore–malam.
        - **BBLJ**: Belokan angin lapisan rendah → konvergensi hujan.
        - **ITCZ**: Zona pertemuan angin tropis → hujan lebat.
        """)

    st.markdown("#### 🧽 Skala Lokal")
    with st.expander("🔍 Penjelasan"):
        st.markdown("""
        - **Angin Lembah–Gunung**: Pola harian → awan orografis.
        - **Konvergensi Mikro**: Efek suhu mikro → awan lokal.
        - **Efek Urban**: Pemanasan kota → konvektif & hujan petir.
        """)

    st.caption("📚 Panel edukatif untuk publik dan siswa meteorologi.")
