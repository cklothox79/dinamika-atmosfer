import streamlit as st

st.set_page_config(page_title="Tentang Aplikasi", layout="wide")
st.title("ℹ️ Tentang Aplikasi")

st.markdown("""
Aplikasi ini dikembangkan oleh **Ferri Kusuma (STMKG/M8TB_14.22.0003)** untuk membantu masyarakat dan pelajar memahami skala dinamika atmosfer yang sedang aktif.

Fitur utama meliputi:
- Deteksi skala global (ENSO, IOD)
- Informasi durasi dan pengaruh MJO, Kelvin, dll
- Interaksi peta dan input kota
- Penjelasan fenomena atmosfer per skala
- (Segera hadir) Prakiraan cuaca real-time dan peta interaktif

Silakan gunakan menu navigasi di sebelah kiri untuk mengeksplorasi tiap bagian aplikasi.
""")

st.success("💡 Aplikasi ini bersifat edukatif. Data yang ditampilkan adalah simulasi dan akan terhubung ke data real-time di versi selanjutnya.")
