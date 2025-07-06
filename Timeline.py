import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Timeline Skala Atmosfer", layout="wide")
st.title("📈 Timeline Skala Atmosfer Aktif")

data = [
    {"Skala": "MJO", "Mulai": "2025-07-03", "Selesai": "2025-07-11", "Pengaruh": "Ya"},
    {"Skala": "ENSO (La Niña)", "Mulai": "2025-06-10", "Selesai": "2025-08-15", "Pengaruh": "Ya"},
    {"Skala": "IOD (Negatif)", "Mulai": "2025-06-20", "Selesai": "2025-09-05", "Pengaruh": "Ya"}
]

df = pd.DataFrame(data)
df["Mulai"] = pd.to_datetime(df["Mulai"])
df["Selesai"] = pd.to_datetime(df["Selesai"])

fig = px.timeline(
    df,
    x_start="Mulai",
    x_end="Selesai",
    y="Skala",
    color="Skala",
    text="Pengaruh",
    title="Aktivitas Skala Atmosfer"
)

fig.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=50, b=20),
    xaxis_title="Tanggal",
    yaxis_title="Skala",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
