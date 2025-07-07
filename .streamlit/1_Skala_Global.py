# File: pages/1_Skala_Global.py

import streamlit as st

st.title("🌐 Skala Atmosfer Global")
st.markdown("""
Skala global mencakup fenomena yang memengaruhi cuaca dan iklim dalam skala sangat luas (antar-benua),
dan bisa berlangsung selama berbulan-bulan atau bahkan tahunan.

### 🌊 Fenomena Global:

- **El Niño / La Niña (ENSO)**: Merupakan fenomena suhu permukaan laut di Samudra Pasifik bagian tengah dan timur.
  - El Niño: Menyebabkan cuaca kering di Indonesia.
  - La Niña: Menyebabkan peningkatan hujan di Indonesia.

- **Indian Ocean Dipole (IOD)**: Merupakan perbedaan suhu laut antara bagian barat dan timur Samudra Hindia.
  - IOD Positif: Menyebabkan kekeringan di Indonesia.
  - IOD Negatif: Meningkatkan curah hujan di Indonesia.

---

📌 **Status Terkini:**
""")

# Status indeks ENSO dan IOD simulatif
enso_index = -0.7
iod_index = -0.4

enso_status = "La Niña" if enso_index <= -0.5 else "El Niño" if enso_index >= 0.5 else "Netral"
iod_status = "Negatif" if iod_index <= -0.4 else "Positif" if iod_index >= 0.4 else "Netral"

st.success(f"🌀 ENSO Index: `{enso_index}` → **{enso_status}**")
st.info(f"🌊 IOD Index: `{iod_index}` → **{iod_status}**")

st.caption("📘 Sumber data: Simulasi statis. Nantinya akan terhubung ke data BMKG atau NOAA secara otomatis.")
