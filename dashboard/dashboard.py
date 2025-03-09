import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
import os

sns.set(style='dark')

# ==============================
# DASHBOARD HEADER
# ==============================
st.set_page_config(page_title="PRSA Pollution Analysis Dashboard", layout="wide")

# Load dataset
file_path = "prsa.csv"
df_prsa = pd.read_csv(file_path)

df_prsa['rain_category'] = df_prsa['RAIN'].apply(lambda x: 'Hujan' if x > 0 else 'Tidak Hujan')

df_prsa['datetime'] = pd.to_datetime(df_prsa[['year', 'month', 'day', 'hour']])

# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("Informasi:")
st.sidebar.markdown("**• Nama: Nauval Gymnasti**")
st.sidebar.markdown(
    "**• Email: [nauvalgymnasti7@gmail.com](nauvalgymnasti7@gmail.com)**")
st.sidebar.title("🔍 Informasi Dashboard")
st.sidebar.markdown("**📌 Analisis Polusi Udara Berdasarkan Curah Hujan dan Waktu**")
st.sidebar.markdown("**💡 Sumber Data: PRSA Dataset**")

# Filter data sidebar
start_date, end_date = df_prsa["datetime"].min(), df_prsa["datetime"].max()

with st.sidebar:
    st.image("polution.webp", width=275)
    st.sidebar.header("📆 Filter Rentang Tanggal:")
    selected_dates = st.date_input("Pilih Rentang Tanggal", [start_date, end_date], min_value=start_date, max_value=end_date)

# Validasi rentang tanggal yang dipilih
start_date, end_date = selected_dates if isinstance(selected_dates, list) and len(selected_dates) == 2 else (start_date, end_date)
filtered_df = df_prsa[(df_prsa["datetime"] >= str(start_date)) & (df_prsa["datetime"] <= str(end_date))]

# ==============================
# DASHBOARD CONTENT
# ==============================
st.title("🌍 PRSA Pollution Analysis Dashboard")
st.markdown("---")

# Membuat kolom untuk menampilkan metrik utama
col1, col2 = st.columns(2)
col1.metric("Rata-rata CO", value=round(filtered_df['CO'].mean(), 2))
col2.metric("Curah Hujan Tertinggi", value=f"{filtered_df['RAIN'].max()} mm")
st.markdown("---")

# ==============================
# ANALISIS 1: Hubungan Curah Hujan dan CO
# ==============================
st.header("☔ Hubungan Curah Hujan dengan Karbon Monoksida (CO)")

# Scatter plot interaktif dengan Plotly
fig_rain_co = px.scatter(filtered_df, x='RAIN', y='CO', color='rain_category', opacity=0.7,
                         title="Curah Hujan vs Karbon Monoksida",
                         labels={'RAIN': 'Curah Hujan (mm)', 'CO': 'CO (ppm)'},
                         color_discrete_sequence=["blue", "red"])
st.plotly_chart(fig_rain_co, use_container_width=True)

# Box plot untuk CO pada hari hujan vs tidak hujan
fig_box = px.box(filtered_df, x='rain_category', y='CO', color='rain_category',
                 title="Distribusi CO pada Hari Hujan vs Tidak Hujan",
                 labels={'rain_category': 'Kategori Hujan', 'CO': 'CO (PPM)'},
                 color_discrete_sequence=["blue", "red"])
st.plotly_chart(fig_box, use_container_width=True)

# ==============================
# ANALISIS 2: Tren Polusi CO Sepanjang Tahun
# ==============================
st.header("📈 Tren Polusi Karbon Monoksida (CO) Sepanjang Tahun")

# Mengelompokkan data berdasarkan bulan dan menghitung rata-rata CO per bulan
monthly_trend = filtered_df.groupby("month")["CO"].mean().reset_index()

# Visualisasi tren CO sepanjang tahun dengan Plotly
fig_trend = px.line(monthly_trend, x='month', y='CO', markers=True,
                    title="Tren Polusi Karbon Monoksida (CO) Sepanjang Tahun",
                    labels={'month': 'Bulan', 'CO': 'Rata-rata CO (PPM)'},
                    color_discrete_sequence=["orange"])
fig_trend.update_xaxes(tickmode='array', tickvals=list(range(1, 13)), 
                        ticktext=["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
st.plotly_chart(fig_trend, use_container_width=True)

st.caption("✨ Dashboard Analisis Data PRSA - Visualisasi dengan Plotly ✨")
