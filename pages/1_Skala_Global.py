# File: pages/1_Skala_Global.py

import streamlit as st

st.set_page_config(page_title="Skala Global", layout="wide")
st.title("🌎 Skala Atmosfer Global")

st.markdown("""
Fenomena atmosfer skala global adalah dinamika sistem atmosfer dan laut yang memengaruhi pola cuaca lintas benua, termasuk Indonesia.

### 🌊 El Niño dan La Niña
""")

col1, col2 = st.columns([1.1, 0.9])
with col1:
    st.markdown("""
**El Niño** terjadi saat suhu permukaan laut di wilayah tengah dan timur Samudra Pasifik (terutama area Nino 3.4) menghangat secara signifikan. Hal ini **melemahkan pertumbuhan awan hujan di Indonesia**, sehingga berpotensi menyebabkan kekeringan.

Sebaliknya, **La Niña** adalah kondisi ketika suhu permukaan laut di wilayah yang sama lebih **dingin dari normal**, sehingga **meningkatkan curah hujan** di wilayah Indonesia, khususnya bagian tengah dan timur.

🔵 **Area Nino 3.4** adalah zona penting yang berada di Samudra Pasifik Tengah (5°LU – 5°LS dan 170°BB – 120°BB), digunakan untuk memantau dan mengklasifikasikan ENSO.
""")

with col2:
    st.image(
        "https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/el_nino_vs_la_nina.png",
        caption="Perbandingan kondisi atmosfer dan laut pada El Niño vs La Niña.",
        use_container_width=True
    )

st.markdown("---")

st.markdown("""
### 📍 Lokasi Area Nino 3.4

Berikut ini lokasi area Nino 3.4 secara spasial:

- **Lintang**: 5°LU – 5°LS
- **Bujur**: 170°BB – 120°BB

Area ini berada di tengah Samudra Pasifik, jauh dari Indonesia, namun **sangat berpengaruh terhadap cuaca Indonesia**.

Contoh pengaruhnya:
- 🌧️ Saat **La Niña**: Curah hujan meningkat di Indonesia bagian tengah dan timur
- ☀️ Saat **El Niño**: Potensi kekeringan meningkat di sebagian besar wilayah Indonesia
""")

st.info("📌 Halaman ini akan dikembangkan lebih lanjut untuk menampilkan animasi perubahan suhu Nino 3.4 berdasarkan data realtime NOAA.")
