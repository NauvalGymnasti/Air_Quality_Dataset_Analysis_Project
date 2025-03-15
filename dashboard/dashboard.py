import pandas as pd
import plotly.express as px
import streamlit as st
import seaborn as sns

# Konfigurasi Tema Dark Mode
st.set_page_config(page_title="Air Quality Analysis Dashboard", layout="wide")
st.markdown("""
    <style>
        body {background-color: #121212; color: #00FF00;}
        .sidebar .sidebar-content {background-color: #1E1E1E;}
        .stPlotlyChart div {background-color: #1E1E1E !important;}
    </style>
""", unsafe_allow_html=True)

sns.set(style='dark')

# Load dataset
df_prsa = pd.read_csv("prsa.csv")
df_prsa['rain_category'] = df_prsa['RAIN'].apply(lambda x: 'Hujan' if x > 0 else 'Tidak Hujan')
df_prsa['datetime'] = pd.to_datetime(df_prsa[['year', 'month', 'day', 'hour']])

# ==============================
# SIDEBAR SEBAGAI NAVIGASI
# ==============================
st.sidebar.title("🔍 Navigasi Dashboard")

st.sidebar.image("airquality.webp", width=275)

page = st.sidebar.radio("Pilih Analisis:", [
    "Hubungan Curah Hujan dengan CO",
    "Tren Polusi Karbon Monoksida"
])

# ==============================
# DASHBOARD CONTENT
# ==============================
st.title("🌍Air Quality Analysis Dashboard")
st.markdown(
    "Dashboard ini menampilkan data kualitas udara di kota Guanyuan, China.\n\n"
    "Ada 2 topik utama yang divisualisasikan dalam dashboard ini yaitu:\n\n"
    "1. **Bagaimana relasi antara curah hujan (RAIN) dengan kadar Karbon Monoksida (CO) di kota Guanyuan?**\n"
    "2. **Bagaimana pola tren kadar karbon monoksida (CO) di Kota Guanyuan per bulan pada tahun 2015 dibandingkan dengan 2016?** "
    "Apakah terdapat korelasi yang signifikan antara keduanya?"
)

st.markdown("---")

if page == "Hubungan Curah Hujan dengan CO":
    st.header("☔ Hubungan Curah Hujan dengan Karbon Monoksida (CO)")
    
    # Interaktif: Slider untuk menyaring rentang curah hujan
    min_rain, max_rain = st.slider("Pilih Rentang Curah Hujan:",
                                   float(df_prsa['RAIN'].min()),
                                   float(df_prsa['RAIN'].max()),
                                   (float(df_prsa['RAIN'].min()), float(df_prsa['RAIN'].max())))
    df_filtered = df_prsa[(df_prsa['RAIN'] >= min_rain) & (df_prsa['RAIN'] <= max_rain)]
    
    # Scatter Plot
    fig_rain_co = px.scatter(df_filtered, x='RAIN', y='CO', color='rain_category', opacity=0.7,
                             title="Curah Hujan vs Karbon Monoksida",
                             labels={'RAIN': 'Curah Hujan (mm)', 'CO': 'CO (ppm)'},
                             color_discrete_sequence=["#00FF00", "#FF4500"], template="plotly_dark")
    st.plotly_chart(fig_rain_co, use_container_width=True)
    
    # Box Plot
    fig_box = px.box(df_filtered, x='rain_category', y='CO', color='rain_category',
                     title="Distribusi CO pada Hari Hujan vs Tidak Hujan",
                     labels={'rain_category': 'Kategori Hujan', 'CO': 'CO (PPM)'},
                     color_discrete_sequence=["#00FF00", "#FF4500"], template="plotly_dark")
    st.plotly_chart(fig_box, use_container_width=True)
    
    # Histogram tambahan untuk distribusi kadar CO
    fig_hist = px.histogram(df_filtered, x='CO', nbins=30, color='rain_category',
                            title="Distribusi Kadar CO",
                            labels={'CO': 'Kadar CO (PPM)'},
                            color_discrete_sequence=["#00FF00", "#FF4500"], template="plotly_dark")
    st.plotly_chart(fig_hist, use_container_width=True)

elif page == "Tren Polusi Karbon Monoksida":
    st.header("📈 Tren Kadar Karbon Monoksida (CO) di Kota Guanyuan")
    
    # Dropdown untuk pemilihan tahun pertama dan kedua
    year1 = st.selectbox("Pilih Tahun Pertama:", sorted(df_prsa['year'].unique()), index=0)
    year2 = st.selectbox("Pilih Tahun Kedua:", sorted(df_prsa['year'].unique()), index=1)
    
    if year1 == year2:
        st.warning("Silakan pilih dua tahun yang berbeda untuk perbandingan.")
    else:
        df_filtered = df_prsa[df_prsa['year'].isin([year1, year2])]
        
        # Tren CO Sepanjang Tahun
        monthly_trend = df_filtered.groupby(['year', "month"])['CO'].mean().reset_index()
        fig_trend = px.line(monthly_trend, x='month', y='CO', color='year', markers=True,
                            title=f"Tren Kadar CO ({year1} vs {year2})",
                            labels={'month': 'Bulan', 'CO': 'Rata-rata CO (PPM)', 'year': 'Tahun'},
                            color_discrete_sequence=["#00FF00", "#FF4500"], template="plotly_dark")
        fig_trend.update_xaxes(tickmode='array', tickvals=list(range(1, 13)),
                                ticktext=["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
        st.plotly_chart(fig_trend, use_container_width=True)

        # Analisis korelasi
        co_trend = df_filtered.pivot_table(index='month', columns='year', values='CO')
        correlation = co_trend.corr().iloc[0, 1]
        
        st.markdown("## 🔍 Analisis Korelasi")
        st.metric(label="Korelasi antara kadar CO", value=f"{correlation:.2f}")
        
        if correlation > 0.7:
            st.success("Korelasi kuat: Pola kadar CO antar tahun sangat mirip.")
        elif correlation > 0.4:
            st.info("Korelasi sedang: Ada kesamaan pola tetapi tidak terlalu signifikan.")
        else:
            st.warning("Korelasi lemah atau tidak ada korelasi yang signifikan.")

st.caption("✨ Dashboard Analisis Data Kualitas Udara - Nauval Gymnasti ✨")