import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Analisis Data Bike Sharing")

st.write("Dashboard ini menampilkan analisis data Bike Sharing")

day_data = pd.read_csv('day_data.csv')
hour_data = pd.read_csv('hour_data.csv')
 
season_order = ['spring', 'summer', 'fall', 'winter']
day_data['season_label'] = pd.Categorical(day_data['season_label'], categories=season_order, ordered=True)
seasonal_trend = day_data.groupby(['year', 'season_label'], observed=False)['cnt'].mean().reset_index()

st.subheader('Tren Penggunaan Sepeda per Musim di Washington D.C. (2011 vs 2012)')
plt.figure(figsize=(10, 6))
sns.lineplot(data=seasonal_trend, x='season_label', y='cnt', hue='year', marker='o')
for i in range(len(seasonal_trend)):
    plt.text(seasonal_trend['season_label'][i], seasonal_trend['cnt'][i], 
             f'{seasonal_trend["cnt"][i]:.0f}', 
             ha='center', va='bottom')
plt.title('Tren Penggunaan Sepeda per Musim')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Jumlah Sepeda yang Dipinjam')
plt.legend(title='Tahun')
st.pyplot(plt)


t_min = -8
t_max = 39
hour_data['temp_celsius'] = hour_data['temp'] * (t_max - t_min) + t_min

bins = range(int(hour_data['temp_celsius'].min()), int(hour_data['temp_celsius'].max()) + 5, 5)
hour_data['temp_range'] = pd.cut(hour_data['temp_celsius'], bins=bins)
range_counts = hour_data.groupby('temp_range', observed=False)['cnt'].sum().reset_index()

max_idx = range_counts['cnt'].idxmax()
max_temp_range = range_counts.loc[max_idx, 'temp_range']
max_cnt = range_counts.loc[max_idx, 'cnt']

col1, col2 = st.columns(2)

with col1:
    st.subheader("Barplot: Jumlah Sepeda Berdasarkan Rentang Suhu")    
    st.write(f"Rentang suhu dengan jumlah sepeda terbanyak: {max_temp_range}")
    st.write(f"Jumlah sepeda yang dipinjam: {max_cnt}")
    colors = ['blue' if i != max_idx else 'red' for i in range(len(range_counts))]
    plt.figure(figsize=(6, 4))
    sns.barplot(x='temp_range', y='cnt', data=range_counts, palette=colors)
    plt.title('Jumlah Sepeda yang Dipinjam Berdasarkan Rentang Suhu')
    plt.xlabel('Rentang Suhu (°C)')
    plt.ylabel('Jumlah Sepeda yang Dipinjam')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    
with col2:
    max_cnt = hour_data['cnt'].max()
    max_temp = hour_data[hour_data['cnt'] == max_cnt]['temp_celsius'].values[0]
    st.subheader(f"Suhu Tertinggi Penggunaan Sepeda: {max_temp:.1f}°C")
    st.write(f"Jumlah sepeda paling banyak digunakan pada suhu: {max_temp:.1f}°C dengan {max_cnt} sepeda.")
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x=hour_data['temp_celsius'], y=hour_data['cnt'])
    sns.regplot(x=hour_data['temp_celsius'], y=hour_data['cnt'], scatter=False, color='red')
    plt.annotate(f'Max pada {max_temp:.1f}°C', xy=(max_temp, max_cnt), 
                 xytext=(max_temp + 2, max_cnt + 200),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.title('Hubungan Suhu dan Jumlah Sepeda yang Dipinjam')
    plt.xlabel('Suhu (°C)')
    plt.ylabel('Jumlah Sepeda yang Dipinjam (cnt)')
    st.pyplot(plt)

bins_hum = range(int(hour_data['hum'].min() * 100), int(hour_data['hum'].max() * 100) + 5, 5)
hour_data['hum_range'] = pd.cut(hour_data['hum'] * 100, bins=bins_hum)
range_counts_hum = hour_data.groupby('hum_range', observed=False)['cnt'].sum().reset_index()

col3, col4 = st.columns(2)

with col3:
    max_idx_hum = range_counts_hum['cnt'].idxmax()  
    max_hum_range = range_counts_hum.loc[max_idx_hum, 'hum_range'] 
    max_cnt_hum = range_counts_hum.loc[max_idx_hum, 'cnt']   
    st.subheader("Barplot: Jumlah Sepeda Berdasarkan Rentang Kelembapan")    
    st.write(f"Rentang kelembapan dengan jumlah sepeda terbanyak: {max_hum_range}")
    st.write(f"Jumlah sepeda yang dipinjam: {max_cnt_hum}")
    colors_hum = ['blue' if i != max_idx_hum else 'red' for i in range(len(range_counts_hum))]
    plt.figure(figsize=(6, 4))
    sns.barplot(x='hum_range', y='cnt', data=range_counts_hum, palette=colors_hum)
    plt.title('Jumlah Sepeda yang Dipinjam Berdasarkan Rentang Kelembapan')
    plt.xlabel('Rentang Kelembapan (%)')
    plt.ylabel('Jumlah Sepeda yang Dipinjam')
    plt.xticks(rotation=45)
    st.pyplot(plt)

with col4:
    max_hum_cnt = hour_data['cnt'].max()
    max_hum = hour_data[hour_data['cnt'] == max_hum_cnt]['hum'].values[0]
    st.subheader(f"Kelembapan Tertinggi Penggunaan Sepeda: {max_hum*100:.1f}%")
    st.write(f"Jumlah sepeda paling banyak digunakan pada kelembapan: {max_hum*100:.1f}% dengan {max_hum_cnt} sepeda.")
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x=hour_data['hum'], y=hour_data['cnt'])
    sns.regplot(x=hour_data['hum'], y=hour_data['cnt'], scatter=False, color='green')
    plt.annotate(f'Max pada {max_hum*100:.1f}%', xy=(max_hum, max_hum_cnt), 
                 xytext=(max_hum + 0.05, max_hum_cnt + 200),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.title('Hubungan Kelembapan dan Jumlah Sepeda yang Dipinjam')
    plt.xlabel('Kelembapan (%)')
    plt.ylabel('Jumlah Sepeda yang Dipinjam (cnt)')
    st.pyplot(plt)

bins_windspeed = range(int(hour_data['windspeed'].min() * 100), int(hour_data['windspeed'].max() * 100) + 5, 5)
hour_data['windspeed_range'] = pd.cut(hour_data['windspeed'] * 100, bins=bins_windspeed)
range_counts_windspeed = hour_data.groupby('windspeed_range', observed=False)['cnt'].sum().reset_index()

col5, col6 = st.columns(2)

with col5:
    max_idx_windspeed = range_counts_windspeed['cnt'].idxmax()  
    max_windspeed_range = range_counts_windspeed.loc[max_idx_windspeed, 'windspeed_range']  
    max_cnt_windspeed = range_counts_windspeed.loc[max_idx_windspeed, 'cnt']  
    st.subheader("Barplot: Jumlah Sepeda Berdasarkan Rentang Kecepatan Angin")    
    st.write(f"Rentang kecepatan angin dengan jumlah sepeda terbanyak: {max_windspeed_range}")
    st.write(f"Jumlah sepeda yang dipinjam: {max_cnt_windspeed}")
    colors_windspeed = ['blue' if i != max_idx_windspeed else 'red' for i in range(len(range_counts_windspeed))]
    plt.figure(figsize=(6, 4))
    sns.barplot(x='windspeed_range', y='cnt', data=range_counts_windspeed, palette=colors_windspeed)
    plt.title('Jumlah Sepeda yang Dipinjam Berdasarkan Rentang Kecepatan Angin')
    plt.xlabel('Rentang Kecepatan Angin (km/h)')
    plt.ylabel('Jumlah Sepeda yang Dipinjam')
    plt.xticks(rotation=45)
    st.pyplot(plt)

with col6:
    max_windspeed_cnt = hour_data['cnt'].max()
    max_windspeed = hour_data[hour_data['cnt'] == max_windspeed_cnt]['windspeed'].values[0]
    st.subheader(f"Kecepatan Angin Tertinggi Penggunaan Sepeda: {max_windspeed*100:.1f} km/h")
    st.write(f"Jumlah sepeda paling banyak digunakan pada kecepatan angin: {max_windspeed*100:.1f} km/h dengan {max_windspeed_cnt} sepeda.")
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x=hour_data['windspeed'], y=hour_data['cnt'])
    sns.regplot(x=hour_data['windspeed'], y=hour_data['cnt'], scatter=False, color='green')
    plt.annotate(f'Max pada {max_windspeed*100:.1f} km/h', xy=(max_windspeed, max_windspeed_cnt), 
                 xytext=(max_windspeed + 0.05, max_windspeed_cnt + 200),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
    plt.title('Hubungan Kecepatan Angin dan Jumlah Sepeda yang Dipinjam')
    plt.xlabel('Kecepatan Angin (km/h)')
    plt.ylabel('Jumlah Sepeda yang Dipinjam (cnt)')
    st.pyplot(plt)