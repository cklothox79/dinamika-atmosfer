# ✅ 5. interaktif_olr_anomali.py

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    st.title("🌥️ Anomali OLR Interaktif")

    tanggal = pd.date_range(start="2025-07-01", periods=7)
    anomali = [-5, -10, 0, 5, 12, 8, -3]

    fig = go.Figure(data=go.Scatter(x=tanggal, y=anomali, mode='lines+markers'))
    fig.update_layout(title="Anomali Outgoing Longwave Radiation (OLR)",
                      xaxis_title="Tanggal", yaxis_title="Anomali (W/m²)")

    st.plotly_chart(fig, use_container_width=True)
