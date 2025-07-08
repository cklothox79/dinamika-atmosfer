import streamlit as st

def app():
    st.title("📍 Visualisasi Area Niño 3.4")

    st.markdown("""
    **Area Niño 3.4** berada di Samudra Pasifik Tropis  
    (5°LU–5°LS; 170°BB–120°BB). Gambar di bawah menandai area tersebut  
    dengan kotak putih pada peta SST (Sea Surface Temperature).
    """)

    st.image(
        "https://raw.githubusercontent.com/cklothox79/dinamika-atmosfer/main/media/el_nino_vs_la_nina.png",  # tambahkan gambar kotak jika sudah di-upload
        caption="🌊 Zonasi Niño 3.4 pada peta SST",
        use_container_width=True
    )

    st.markdown("""
    ### 🎯 Intisari:

    - **El Niño**: suhu laut lebih hangat → potensi cuaca kering.
    - **La Niña**: suhu laut lebih dingin → potensi cuaca basah.
    - Area ini dipantau menggunakan **ENSO Index** seperti Oceanic Niño Index (ONI).
    """)

    st.info("Kotak putih menunjukkan lokasi Niño 3.4. Warna mewakili suhu permukaan laut anomali.")
