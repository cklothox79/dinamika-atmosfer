import streamlit as st

st.title("🌦️ Prakiraan Cuaca")
st.markdown("Fitur ini akan menampilkan prakiraan cuaca real-time berdasarkan kota yang Anda pilih.")
st.info("📌 Fitur ini masih dalam pengembangan oleh Ferri Kusuma. Nantikan update selanjutnya!")

st.markdown("### 🏙️ Masukkan Nama Kota")
kota = st.text_input("Masukkan kota", "Malang").strip().title()

if kota:
    st.success(f"Menampilkan prakiraan cuaca untuk kota: **{kota}**")

    # Dummy data prakiraan
    st.markdown("#### 🌤️ Cuaca Hari Ini")
    st.markdown("- Kondisi: Cerah Berawan")
    st.markdown("- Suhu: 28°C")
    st.markdown("- Kelembapan: 75%")
    st.markdown("- Kecepatan Angin: 15 km/jam")
    st.markdown("- Tekanan: 1010 hPa")

    st.caption("📊 Data ini bersifat simulasi. Versi real-time akan segera tersedia.")
else:
    st.warning("Masukkan nama kota terlebih dahulu.")
