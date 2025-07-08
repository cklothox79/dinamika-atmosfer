# ✅ 4. interaktif_mjo_index.py

```python
import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("💫 MJO Index Interaktif")

    data = {
        "Tanggal": pd.date_range(start="2025-07-01", periods=10, freq='D'),
        "Amplitude": [0.5, 0.6, 0.9, 1.2, 1.5, 1.3, 1.0, 0.8, 0.6, 0.4]
    }
    df = pd.DataFrame(data)

    fig = px.line(df, x="Tanggal", y="Amplitude", title="Indeks MJO Harian")
    fig.update_traces(mode="lines+markers")
    st.plotly_chart(fig, use_container_width=True)
