# ✅ 2. interaktif_enso_index.py

```python
import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("📈 ENSO Index Interaktif")

    data = {
        "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun"],
        "ONI": [0.5, 0.6, 0.8, 1.0, 0.9, 0.7]
    }
    df = pd.DataFrame(data)

    fig = px.line(df, x="Bulan", y="ONI", title="Oceanic Niño Index (ONI)")
    fig.update_traces(mode="lines+markers")
    st.plotly_chart(fig, use_container_width=True)
