import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Penyewaan Sepeda", layout="wide")

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv('https://raw.githubusercontent.com/FatwaAlFajar/submission-main/refs/heads/main/data/day.csv')
    hour_df = pd.read_csv('https://raw.githubusercontent.com/FatwaAlFajar/submission-main/refs/heads/main/data/hour.csv')
    return day_df, hour_df

day_df, hour_df = load_data()
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar untuk filter rentang waktu
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", use_container_width=True)
    min_date = day_df['dteday'].min()
    max_date = day_df['dteday'].max()
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

# 🎯 Filter data berdasarkan rentang waktu
filtered_data = day_df[(day_df['dteday'] >= pd.Timestamp(start_date)) & (day_df['dteday'] <= pd.Timestamp(end_date))]

# Judul Dashboard
st.title("📊 Dashboard Penyewaan Sepeda")

# ✅ Menampilkan data yang sudah difilter
st.write("### Data Harian (Setelah Difilter):")
st.dataframe(filtered_data.head())

st.write("### Data Per Jam:")
st.dataframe(hour_df.head())

# **Plot Rata-rata Penyewaan Sepeda Berdasarkan Musim**
st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots()
    sns.barplot(x='season', y='cnt', data=filtered_data, estimator='mean', palette='coolwarm', ax=ax)
    ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    st.pyplot(fig)

with col2:
    st.image("https://e7.pngegg.com/pngimages/57/994/png-clipart-bicycle-helmets-mountain-bike-bicycle-wheels-cycling-ride-bike-bicycle-frame-bicycle.png", caption="Musim Penyewaan", use_container_width=True)

# **Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda**
st.subheader("Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots()
    sns.barplot(x='weathersit', y='cnt', data=filtered_data, estimator='mean', palette='Set2', ax=ax)
    ax.set_xticklabels(['Cerah', 'Berkabut', 'Hujan Ringan', 'Hujan Lebat'])
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    st.pyplot(fig)

with col2:
    st.image("https://source.unsplash.com/200x200/?weather", caption="Cuaca dan Penyewaan", use_container_width=True)

# **Jam dengan Penyewaan Tertinggi**
max_hour = hour_df.loc[hour_df['cnt'].idxmax(), 'hr']
st.write(f"### 🚴 Penyewaan sepeda paling banyak dilakukan pada jam ke-{max_hour}.")

# **Visualisasi Penyewaan Sepeda Per Jam**
st.subheader("Penyewaan Sepeda Per Jam")
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots()
    sns.lineplot(x='hr', y='cnt', data=hour_df, marker='o', ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

with col2:
    st.image("https://source.unsplash.com/200x200/?clock", caption="Jam Penyewaan", use_container_width=True)
