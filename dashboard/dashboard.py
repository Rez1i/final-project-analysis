import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

st.set_page_config(
    page_title="Analisa Rental Sepeda",
    page_icon=":bicycle:",
)

def create_trend_bike(df):
    trend_bike = df.groupby(by='yr').agg({
    'cnt': 'mean'
    }).sort_values(by="yr", ascending=False) # diurutkan berdasarkan tahun
    return trend_bike

def create_comparisson_workingday(df):
    comparisson_workingday=df.groupby(by='workingday').agg({
    'cnt': ['max', 'min', 'mean']
    })
    return comparisson_workingday

# Meload dataset kedalam variabel day_df
day_df = pd.read_csv('dashboard/day_cleaned.csv')

# Menyiapkan dataframe
trend_bike = create_trend_bike(day_df)
comparisson_workingday = create_comparisson_workingday(day_df)

st.title('Dashboard Rental Sepeda🚲 ')
tab1, tab2, tab3 = st.tabs(["Latar Belakang", "Data Set", "Chart"])
 
with tab1:
    st.header("Latar Belakang Rental Sepeda")
    st.image("bike.jpg")
    st.write("Sistem berbagi sepeda merupakan generasi baru dari penyewaan sepeda tradisional di mana seluruh proses mulai dari keanggotaan, penyewaan, dan pengembalian telah menjadi otomatis. Melalui sistem ini, pengguna dapat dengan mudah menyewa sepeda dari lokasi tertentu dan mengembalikannya di lokasi lain. Saat ini, terdapat sekitar lebih dari 500 program berbagi sepeda di seluruh dunia yang terdiri dari lebih dari 500 ribu sepeda. Saat ini, terdapat minat yang besar terhadap sistem ini karena perannya yang penting dalam masalah lalu lintas, lingkungan, dan kesehatan. Selain aplikasi sistem berbagi sepeda yang menarik di dunia nyata, karakteristik data yang dihasilkan oleh sistem ini membuatnya menarik untuk penelitian. Berbeda dengan layanan transportasi lain seperti bus atau kereta bawah tanah, durasi perjalanan, posisi keberangkatan, dan kedatangan dicatat secara eksplisit dalam sistem ini. Fitur ini mengubah sistem berbagi sepeda menjadi jaringan sensor virtual yang dapat digunakan untuk mendeteksi mobilitas di kota. Oleh karena itu, diharapkan sebagian besar peristiwa penting di kota dapat dideteksi melalui pemantauan data ini.")
    
 
with tab2:
    st.header("Data Set")
    st.caption("Setelah dibersihkan")
    st.dataframe(data=day_df, width=800, height=500)
    st.write("Proses penyewaan sepeda bersama sangat berkorelasi dengan lingkungan dan musim. Misalnya, kondisi cuaca, curah hujan, hari dalam seminggu, musim, jam dalam sehari, dll. dapat memengaruhi perilaku penyewaan. Kumpulan data inti terkait dengan catatan historis dua tahun yang sesuai dengan tahun 2011 dan 2012 dari sistem Capital Bikeshare, Washington D.C., AS yang tersedia untuk umum di http://capitalbikeshare.com/system-data. Kami menggabungkan data berdasarkan dua jam dan harian, lalu mengekstrak dan menambahkan informasi cuaca dan musim yang sesuai. Informasi cuaca diekstrak dari http://www.freemeteo.com.")
 
with tab3:
    st.header("Chart Hasil Analisis")
    st.subheader("Tren Jumlah Pengguna Sepeda Dalam Beberapa Tahun Terakhir")
    
    trend_bike = trend_bike.reset_index() # Mereset index setiap row nya
    day_df['mnth'] = pd.Categorical(day_df['mnth'], categories=
    ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    ordered=True)

    # Menjumlahkan total cnt dalam setiap bulan nya
    monthly_counts = day_df.groupby(by=["mnth","yr"]).agg({
        "cnt": "sum"
    }).sort_values(by=["yr","mnth"], ascending=False).reset_index()

    # Menentukan garis didalam chart menggunakan library seaborn
   
    sns.lineplot(
        data=monthly_counts,
        x="mnth",
        y="cnt",
        hue="yr",
        palette="deep",
        style="yr",
        marker="o",
        dashes=False)

    # Menambahkan atribut untuk memperjelas chart
    plt.title("Trend Sewa Sepeda")
    plt.xlabel(None)
    plt.ylabel("count of total rental")
    plt.legend(title="Tahun", loc="upper right")
    st.pyplot(plt)
    
    with st.expander("Insight"):
        st.write("Tren rental sepeda meningkat pada tahun 2012 dari 2011, dan untuk setiap bulannya peningkatan terjadi dalam awal tahun sampai pertengahan tahun, walaupun selalu terjadi penurunan tren setiap akhir tahun dimulai dari bulan october.")
    st.subheader("Perbandingan Penyewa Sepeda Workingday Dan Holiday")
    plt.figure(figsize=(10,6))
    sns.barplot(
        x='workingday',
        y='cnt',
        palette='rocket',
        data=day_df)

    plt.title('Perbandingan Penyewa Sepeda Workingday Dan Holiday')
    plt.xlabel(None)
    plt.ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(plt)
    with st.expander("Insight"):
        st.write("Lebih Banyak orang melakukan rental sepeda pada workday dibanding holiday. ini menunjukan bahwa orang suka menggunakan sepeda untuk menjalan kegiatan sehari-hari nya")

