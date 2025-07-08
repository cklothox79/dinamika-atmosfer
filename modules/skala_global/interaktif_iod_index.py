# ✅ 3. interaktif_iod_index.py

```python
import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("🌊 IOD Index Interaktif")

    data = {
        "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun"],
        "IOD": [-0.2, -0.4, -0.3, 0.0, 0.1, 0.3]
    }
    df = pd.DataFrame(data)

    fig = px.bar(df, x="Bulan", y="IOD", title="Indian Ocean Dipole (IOD) Index")
    st.plotly_chart(fig, use_container_width=True)
