import streamlit as st

st.set_page_config(page_title="Edukasi Skala Atmosfer", layout="wide")
st.title("🎓 Edukasi: Kenali Skala Atmosfer")

st.markdown("""
Selamat datang! Di halaman ini kamu bisa belajar tentang **fenomena skala atmosfer** yang memengaruhi cuaca dan iklim di Indonesia 🌧️🌞🌊.
""")

# ========== ENSO ==========
with st.expander("🌀 ENSO (El Niño - Southern Oscillation)"):
    st.image("https://www.bom.gov.au/climate/enso/history/enso-animation.gif",
             caption="Animasi ENSO - Sumber: BOM Australia", use_column_width=True)
    st.markdown("""
    **ENSO** adalah fenomena suhu laut di Samudra Pasifik yang memengaruhi iklim global.

    - **El Niño**: Pemanasan laut Pasifik → Kemarau lebih kering di Indonesia.
    - **La Niña**: Pendinginan laut Pasifik → Hujan lebih sering di Indonesia.
    - **Netral**: Tidak ada pengaruh dominan.

    ❗ ENSO berdampak besar pada musim hujan/kemarau, kekeringan, hingga banjir.
    """)

# ========== IOD ==========
with st.expander("🌊 IOD (Indian Ocean Dipole)"):
    st.image("https://www.bom.gov.au/climate/iod/images/iod-phases.png",
             caption="Fase IOD - Sumber: BOM Australia", use_column_width=True)
    st.markdown("""
    **IOD** menggambarkan perbedaan suhu laut di barat & timur Samudra Hindia.

    - **IOD Positif**: Laut barat lebih hangat → Indonesia cenderung kering.
    - **IOD Negatif**: Laut timur lebih hangat → Curah hujan meningkat di barat Indonesia.
    - **Netral**: Tidak signifikan.

    🔁 IOD biasanya muncul bersamaan dengan ENSO, bisa memperkuat atau melemahkan dampaknya.
    """)

# ========== MJO ==========
with st.expander("☁️ MJO (Madden-Julian Oscillation)"):
    st.image("https://www.bom.gov.au/climate/mjo/graphics/4phase.MJO.big.gif",
             caption="Fase MJO - Sumber: BOM Australia", use_column_width=True)
    st.markdown("""
    **MJO** adalah gelombang konveksi tropis yang bergerak dari barat ke timur.

    - Memengaruhi pola hujan 1–2 minggu ke depan.
    - MJO dibagi dalam **8 fase**, tiap fase menunjukkan posisi hujan aktif.

    ⏳ MJO bersifat **intra-musiman** (berlangsung dalam mingguan), dan sangat penting dalam prakiraan jangka pendek.
    """)

# ========== Gelombang Tropis ==========
with st.expander("🌐 Gelombang Kelvin & Rossby"):
    st.markdown("""
    Gelombang tropis ini berperan penting dalam dinamika atmosfer di daerah ekuator 🌍

    - **Gelombang Kelvin**: Bergerak cepat dari barat ke timur, bisa memicu hujan tiba-tiba.
    - **Gelombang Rossby**: Bergerak lambat dari timur ke barat, lebih sering muncul di musim transisi.

    🔄 Interaksi gelombang ini dapat memperkuat atau memperlemah curah hujan lokal.
    """)
    st.image("https://www.climate.gov/sites/default/files/styles/full_width/public/KelvinRossby_620.gif",
             caption="Animasi Gelombang Kelvin & Rossby", use_column_width=True)

# ========== Penutup ==========
st.info("💡 Kunjungi halaman 'Beranda' untuk melihat pengaruh nyata skala-skala ini di lokasi yang kamu pilih.")
