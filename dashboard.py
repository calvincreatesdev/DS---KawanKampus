import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(page_title="Dashboard Analitik Kawan Kampus", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# INJEKSI CSS (POPPINS FONT & ORANGE-YELLOW THEME)
# ==========================================
custom_css = """
<style>
    /* Import Font Poppins dari Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* Terapkan ke seluruh elemen */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Warna Header Kustom */
    h1 {
        color: #FF8C00 !important; /* Dark Orange */
        font-weight: 700 !important;
    }
    h2, h3 {
        color: #FFA000 !important; /* Amber/Yellow-Orange */
        font-weight: 600 !important;
    }
    
    /* Warna Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFDF8 !important; /* Krem sangat muda */
        border-right: 2px solid #FFC107 !important;
    }
    
    /* Styling Metrik (Angka KPI) */
    [data-testid="stMetricValue"] {
        color: #FF9800 !important;
        font-weight: 700 !important;
    }
    
    /* Styling Tabs Aktif */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        border-bottom-color: #FF9800 !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] [data-testid="stMarkdownContainer"] p {
        color: #FF8C00 !important;
        font-weight: 700 !important;
    }
    
    /* Styling Info Box (Pertanyaan Bisnis) */
    .stAlert {
        background-color: #FFF3E0 !important;
        color: #E65100 !important;
        border: none !important;
        border-left: 5px solid #FF9800 !important;
    }
    
    /* Styling Success Box (Insight Bisnis) */
    [data-testid="stNotificationSuccess"] {
        background-color: #FFFFFF !important;
        border-left: 5px solid #8BC34A !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Setel Palet Matplotlib agar bernuansa hangat tapi tetap jelas terbaca
sns.set_theme(style="whitegrid", palette=["#FF9800", "#FFC107", "#424242", "#757575"])

# ==========================================
# DATA PIPELINE (CACHED)
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('Data/kawankampus_master_dataset.csv')
    
    singkatan_kampus = {
        'Universitas Bina Nusantara @Anggrek': 'BINUS', 
        'Universitas Institut Teknologi Bandung - Ganesha': 'ITB',
        'Universitas Airlangga - B': 'UNAIR', 
        'Universitas Pendidikan Indonesia Bandung': 'UPI',
        'Universitas Multi Data Palembang': 'MDP', 
        'Universitas Indonesia': 'UI',
        'Universitas Institut Pertanian Bogor': 'IPB',     
        'Universitas Gadjah Mada': 'UGM',
        'Universitas Brawijaya': 'UB', 
        'STMIK IKMI CIREBON': 'IKMI'
    }
    df['Singkatan'] = df['Kampus'].map(singkatan_kampus)
    
    klaster_mapping = {
        'BINUS': 'Urban', 'ITB': 'Urban', 'UNAIR': 'Urban', 'UPI': 'Urban', 'MDP': 'Urban',
        'UI': 'Sub-urban', 'IPB': 'Sub-urban', 'UGM': 'Sub-urban', 'UB': 'Sub-urban', 'IKMI': 'Sub-urban'
    }
    df['Klaster'] = df['Singkatan'].map(klaster_mapping)
    
    df_master = pd.DataFrame(list(singkatan_kampus.values()), columns=['Singkatan'])
    return df, df_master

df, df_master = load_data()

# ==========================================
# SIDEBAR: FILTER INTERAKTIF & LOGO
# ==========================================
# Menampilkan Logo Kawan Kampus
st.sidebar.image("Assets/logo_kawan_kampus.png", use_container_width=True)

st.sidebar.header("Filter Analitik")
kampus_list = ['Semua Kampus'] + list(df['Singkatan'].dropna().unique())
selected_kampus = st.sidebar.selectbox("Pilih Target Universitas", kampus_list)

if selected_kampus != 'Semua Kampus':
    df_filtered = df[df['Singkatan'] == selected_kampus]
    df_master_filtered = df_master[df_master['Singkatan'] == selected_kampus]
else:
    df_filtered = df.copy()
    df_master_filtered = df_master.copy()

# ==========================================
# HEADER & KPI METRICS
# ==========================================
st.title("Kawan Kampus: Evaluasi Infrastruktur & Analisis Spasial 2026")
st.markdown("Dashboard interaktif ini membedah pola perilaku, kelayakan infrastruktur, dan mitigasi risiko fasilitas di sekitar area kampus untuk optimalisasi sistem rekomendasi AI.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Fasilitas", len(df_filtered))
col2.metric("Rata-rata Skor Keseluruhan", round(df_filtered['Skor_Kepercayaan'].mean(), 2))
col3.metric("Fasilitas Sangat Populer", len(df_filtered[df_filtered['Kategori_Popularitas'] == 'Sangat Populer']))
col4.metric("Kategori Dominan", df_filtered['Kategori_Awal'].mode()[0] if not df_filtered.empty else "N/A")

st.divider()

# ==========================================
# TAB KONTEN UTAMA
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Q1: Jarak vs Kuliner", 
    "Q2: Hidden Gems", 
    "Q3: Kesiapan Medis", 
    "Q4: Mobilitas Komuter", 
    "Q5: Bias Popularitas"
])

# ------------------------------------------
# TAB 1: SENSITIVITAS JARAK KULINER
# ------------------------------------------
with tab1:
    st.info("📌 **Pertanyaan Bisnis:** Apakah terdapat perbedaan rata-rata Skor_Kepercayaan yang signifikan secara statistik antara fasilitas kuliner merakyat ('Warteg' dan 'Restoran padang') di radius 'Jalan Kaki' (<= 0.5 KM) dibandingkan radius 'Perlu Motor' (0.5 - 2.0 KM) pada master dataset Kawan Kampus 2026?")
    
    df_q1 = df_filtered[
        (df_filtered['Kategori_Awal'].isin(['Warteg', 'Restoran padang'])) & 
        (df_filtered['Kategori_Jarak'].isin(['Jalan Kaki', 'Perlu Motor']))
    ]
    
    if not df_q1.empty:
        fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        sns.boxplot(data=df_q1, x='Kategori_Jarak', y='Skor_Kepercayaan', hue='Kategori_Awal', palette=['#FF9800', '#FFC107'], ax=ax1)
        ax1.set(title='Distribusi Skor Kepercayaan Berdasarkan Radius', xlabel='Radius Kategori Jarak', ylabel='Skor Kepercayaan (1-5)', ylim=(1, 5.2))
        
        sns.pointplot(data=df_q1, x='Kategori_Jarak', y='Skor_Kepercayaan', hue='Kategori_Awal', palette=['#FF9800', '#FFC107'], dodge=True, ax=ax2)
        ax2.set(title='Rata-Rata Skor & Margin of Error (95% CI)', xlabel='Radius Kategori Jarak', ylabel='Rata-rata Skor Kepercayaan', ylim=(3.5, 4.8))
        
        st.pyplot(fig1)
    else:
        st.warning("Data tidak tersedia untuk filter saat ini.")
        
    st.markdown("### 💡 Kesimpulan")
    st.markdown("Jarak tidak menjadi faktor penurun kualitas untuk kuliner merakyat. Grafik boxplot dan pointplot mengonfirmasi bahwa rentang dan rata-rata Skor Kepercayaan Warteg maupun Restoran Padang tetap stabil di atas angka 4.0, baik di radius jalan kaki maupun radius bermotor.")
    st.success("🚀 **Insight Bisnis:** Algoritma rekomendasi tidak boleh memberikan penalti (penurunan peringkat) pada warteg atau resto Padang yang lokasinya berada di radius 'Perlu Motor'. Mahasiswa terbukti tetap mendapatkan kualitas yang tinggi meskipun harus menempuh jarak sedikit lebih jauh untuk kategori makanan ini.")

# ------------------------------------------
# TAB 2: HIDDEN GEMS
# ------------------------------------------
with tab2:
    st.info("📌 **Pertanyaan Bisnis:** Kategori fasilitas penunjang produktivitas ('Cafe' dan 'Kedai') mana saja yang mendominasi posisi kuartil atas (Top 15%) Skor_Kepercayaan tertinggi meskipun terklasifikasi dalam zona 'Agak Jauh' (> 2.0 KM) pada data Capstone 2026?")
    
    df_q2 = df_filtered[df_filtered['Kategori_Awal'].isin(['Cafe', 'Kedai'])].copy()
    
    if not df_q2.empty:
        threshold_skor = df['Skor_Kepercayaan'][df['Kategori_Awal'].isin(['Cafe', 'Kedai'])].quantile(0.85)
        
        df_q2['Is_Hidden_Gem'] = (df_q2['Jarak_KM'] > 2.0) & (df_q2['Skor_Kepercayaan'] >= threshold_skor)
        df_gems = df_q2[df_q2['Is_Hidden_Gem']]
        
        gem_counts = df_gems['Singkatan'].value_counts().reset_index()
        gem_counts.columns = ['Singkatan', 'Total_Hidden_Gems']
        gem_counts = pd.merge(df_master_filtered, gem_counts, on='Singkatan', how='left').fillna(0).sort_values('Total_Hidden_Gems', ascending=False)
        
        fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        sns.scatterplot(data=df_q2, x='Jarak_KM', y='Skor_Kepercayaan', hue='Kategori_Awal', palette=['#FF9800', '#FFC107'], s=80, alpha=0.7, ax=ax1)
        ax1.axvline(2.0, color='gray', linestyle='--')
        ax1.axhline(threshold_skor, color='red', linestyle='--')
        ax1.fill_between(x=[2.0, df_q2['Jarak_KM'].max() + 0.1], y1=threshold_skor, y2=5.2, color='#FFC107', alpha=0.15)
        ax1.set(title='Peta Kuadran Ruang Produktivitas', xlabel='Jarak dari Kampus (KM)', ylabel='Skor Kepercayaan')
        
        sns.barplot(data=gem_counts, x='Total_Hidden_Gems', y='Singkatan', color='#FF9800', ax=ax2)
        ax2.set(title='Kuantitas Hidden Gems di Tiap Kampus', xlabel='Jumlah Tempat (Jarak > 2.0 KM & Top 15% Skor)', ylabel='')
        
        st.pyplot(fig2)
    else:
        st.warning("Data tidak tersedia untuk filter saat ini.")
        
    st.markdown("### 💡 Kesimpulan")
    st.markdown("Kuadran \"Hidden Gems\" terbukti valid dan memiliki pasokan data yang solid. Terdapat sebaran cafe dan kedai di jarak jauh (> 2.0 KM) yang sukses menembus Top 15% Skor Kepercayaan. ITB dan BINUS mendominasi ketersediaan fasilitas tersembunyi ini secara signifikan dibandingkan kampus lain.")
    st.success("🚀 **Insight Bisnis:** Fitur atau penyesuaian bobot untuk \"Hidden Gems\" sangat mendesak untuk diimplementasikan, terutama bagi pengguna di klaster kampus seperti ITB dan BINUS. Ini membuktikan ada segmen pasar mahasiswa yang rela menjauh dari pusat kampus demi mendapatkan tempat produktivitas berkualitas premium.")

# ------------------------------------------
# TAB 3: INFRASTRUKTUR APOTEK DARURAT
# ------------------------------------------
with tab3:
    st.info("📌 **Pertanyaan Bisnis:** Berapa persentase ketersediaan fasilitas kesehatan darurat ('Apotek') yang memiliki Skor_Kepercayaan minimal 4.0 di dalam radius 'Jalan Kaki' (<= 0.5 KM) untuk mengidentifikasi area kampus dengan infrastruktur medis terendah pada dataset 2026?")
    
    df_apotek = df_filtered[df_filtered['Kategori_Awal'] == 'Apotek'].copy()
    
    if not df_apotek.empty:
        df_apotek['Status_Aman'] = ((df_apotek['Skor_Kepercayaan'] >= 4.0) & (df_apotek['Jarak_KM'] <= 0.5)).map({True: 'Aman', False: 'Risiko'})
        cross_tab = pd.crosstab(df_apotek['Singkatan'], df_apotek['Status_Aman'])
        cross_tab_pct = cross_tab.div(cross_tab.sum(1), axis=0) * 100
        
        persentase_aman = pd.merge(df_master_filtered, cross_tab_pct.get('Aman', pd.Series(dtype=float)).reset_index(name='Pct_Aman'), on='Singkatan', how='left').fillna(0)
        persentase_aman = persentase_aman.sort_values('Pct_Aman', ascending=True).set_index('Singkatan')['Pct_Aman']
        
        fig3, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        colors = ['#EF5350' if x < 10 else '#FFB74D' for x in persentase_aman]
        persentase_aman.plot(kind='barh', color=colors, ax=ax1)
        ax1.axvline(10, color='black', linestyle='-.', label='Batas Kritis 10%')
        ax1.set(title='Persentase Apotek Sesuai Standar (Skor ≥ 4.0 & ≤ 0.5 KM)', xlabel='Persentase Ketersediaan (%)', ylabel='Universitas')
        ax1.legend()
        
        cross_tab_pct.reindex(persentase_aman.index).plot(kind='barh', stacked=True, color=['#81C784', '#E57373'], ax=ax2)
        ax2.set(title='Proporsi Rasio Apotek: Aman vs Risiko', xlabel='Persentase (%)', ylabel='')
        ax2.legend(title='Status Validasi', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        st.pyplot(fig3)
    else:
        st.warning("Data Apotek tidak tersedia untuk filter saat ini.")

    st.markdown("### 💡 Kesimpulan")
    st.markdown("Terdapat kesenjangan infrastruktur medis darurat yang sangat kritis. Kampus seperti UGM, IPB, dan UPI memiliki 0% ketersediaan apotek berstandar mutu aman di radius pejalan kaki, menjadikan wilayah tersebut sebagai zona risiko merah. Sebaliknya, BINUS dan MDP memiliki tingkat keamanan fasilitas kesehatan pejalan kaki yang sangat prima.")
    st.success("🚀 **Insight Bisnis:** Sistem aplikasi harus diprogram untuk mendeteksi lokasi pengguna. Jika pengguna berada di kampus berisiko tinggi (UGM, IPB, UPI), radius pencarian darurat aplikasi harus secara otomatis zoom-out ke jangkauan bermotor agar tidak memberikan hasil pencarian kosong (blank screen) saat kondisi krisis.")

# ------------------------------------------
# TAB 4: MOBILITAS KOMUTER
# ------------------------------------------
with tab4:
    st.info("📌 **Pertanyaan Bisnis:** Bagaimana rasio ketersediaan fasilitas 'Perhentian bus' terhadap total entitas 'Minimarket' di radius 'Perlu Motor' (0.5 - 2.0 KM) untuk membandingkan kesiapan mobilitas antara klaster kampus sub-urban dan urban pada data spasial 2026?")
    
    klaster_mapping_komuter = {
        'BINUS': 'Urban', 'ITB': 'Urban', 'UNAIR': 'Urban', 'UPI': 'Urban', 'MDP': 'Urban',
        'UI': 'Sub-urban', 'IPB': 'Sub-urban', 'UGM': 'Sub-urban', 'UB': 'Sub-urban', 'IKMI': 'Sub-urban'
    }
    
    df_komuter = df_filtered[
        (df_filtered['Kategori_Awal'].isin(['Perhentian bus', 'Minimarket'])) & 
        (df_filtered['Kategori_Jarak'] == 'Perlu Motor')
    ].copy()
    
    if not df_komuter.empty:
        df_komuter['Klaster'] = df_komuter['Singkatan'].map(klaster_mapping_komuter)
        pivot_k = df_komuter.pivot_table(index=['Singkatan', 'Klaster'], columns='Kategori_Awal', aggfunc='size', fill_value=0).reset_index()
        
        pivot_k['Perhentian bus'] = pivot_k.get('Perhentian bus', 0)
        pivot_k['Minimarket'] = pivot_k.get('Minimarket', 0)
        pivot_k['Rasio_Bus_Mini'] = pivot_k['Perhentian bus'] / (pivot_k['Minimarket'] + 1)
        pivot_k = pivot_k.sort_values('Rasio_Bus_Mini', ascending=False)
        
        fig4, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        sns.barplot(data=pivot_k, x='Rasio_Bus_Mini', y='Singkatan', hue='Klaster', dodge=False, palette={'Urban':'#FF9800', 'Sub-urban':'#4DB6AC'}, ax=ax1)
        ax1.set(title='Rasio Perhentian Bus terhadap Minimarket', xlabel='Nilai Rasio (Bus / Minimarket)', ylabel='')
        
        sns.scatterplot(data=pivot_k, x='Minimarket', y='Perhentian bus', hue='Klaster', s=150, palette={'Urban':'#FF9800', 'Sub-urban':'#4DB6AC'}, ax=ax2)
        
        urban_data = pivot_k[pivot_k['Klaster']=='Urban']
        suburban_data = pivot_k[pivot_k['Klaster']=='Sub-urban']
        if len(urban_data) > 1: sns.regplot(data=urban_data, x='Minimarket', y='Perhentian bus', scatter=False, color='#FF9800', ax=ax2)
        if len(suburban_data) > 1: sns.regplot(data=suburban_data, x='Minimarket', y='Perhentian bus', scatter=False, color='#4DB6AC', ax=ax2)
        
        for i in range(pivot_k.shape[0]):
            ax2.text(pivot_k['Minimarket'].iloc[i]+0.5, pivot_k['Perhentian bus'].iloc[i], pivot_k['Singkatan'].iloc[i], fontsize=8)
        ax2.set(title='Korelasi Kuantitas Logistik vs Transportasi')
        
        st.pyplot(fig4)
    else:
        st.warning("Data Komuter/Logistik tidak tersedia untuk filter saat ini.")

    st.markdown("### 💡 Kesimpulan")
    st.markdown("Infrastruktur transportasi publik formal (perhentian bus) sama sekali tidak eksis di klaster sub-urban jika disandingkan dengan ekspansi ritel logistik (minimarket). Grafik menunjukkan seluruh kampus sub-urban (seperti UB, UI, UGM, IPB) memiliki rasio 0.0, yang berarti minimarket jauh meninggalkan pembangunan halte bus di radius menengah.")
    st.success("🚀 **Insight Bisnis:** Aplikasi tidak bisa mengandalkan titik transportasi formal Google Maps untuk kampus sub-urban. Tim pengembang wajib mengintegrasikan titik kumpul ojek pangkalan, rute angkot lokal, atau fitur ride-sharing pihak ketiga untuk menambal lubang mobilitas mahasiswa perantau di wilayah tersebut.")

# ------------------------------------------
# TAB 5: BIAS POPULARITAS VIRAL
# ------------------------------------------
with tab5:
    st.info("📌 **Pertanyaan Bisnis:** Bagaimana perbandingan Skor_Kepercayaan antara fasilitas berstatus 'Sepi' dengan fasilitas 'Sangat Populer' pada kategori tempat produktivitas ('Cafe' dan 'Kedai') di 10 kampus pada dataset 2026?")
    
    df_q5 = df_filtered[
        (df_filtered['Kategori_Awal'].isin(['Cafe', 'Kedai'])) & 
        (df_filtered['Kategori_Popularitas'].isin(['Sepi', 'Sangat Populer']))
    ].copy()
    
    if not df_q5.empty:
        fig5, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        sns.violinplot(data=df_q5, x='Kategori_Popularitas', y='Skor_Kepercayaan', hue='Kategori_Awal', split=False, inner="quart", palette=['#FFB74D', '#FFF176'], ax=ax1)
        ax1.set(title='Pemusatan Skor: Sepi vs Sangat Populer', xlabel='Status Popularitas (Volume Ulasan)', ylabel='Skor Kepercayaan', ylim=(2, 5.2))
        
        sns.scatterplot(data=df_q5, x='Total_Reviews', y='Skor_Kepercayaan', hue='Kategori_Popularitas', style='Kategori_Awal', s=80, alpha=0.7, palette=['#FF9800', '#FFC107'], ax=ax2)
        ax2.set_xscale('log')
        ax2.axhline(df_q5['Skor_Kepercayaan'].mean(), color='gray', linestyle='--', label='Rata-rata Skor Keseluruhan')
        ax2.set(title='Sebaran Skor berdasarkan Kuantitas Ulasan Absolut', xlabel='Total Ulasan di Google Maps (Skala Logaritmik)', ylabel='')
        ax2.legend(loc='lower right')
        
        st.pyplot(fig5)
    else:
        st.warning("Data Cafe/Kedai Popularitas tidak tersedia untuk filter saat ini.")

    st.markdown("### 💡 Kesimpulan")
    st.markdown("Popularitas berbanding terbalik dengan jaminan mutu. Violin plot dan skala logaritmik secara gamblang memperlihatkan bahwa tempat berstatus \"Sepi\" justru memiliki konsentrasi skor sempurna (5.0) yang jauh lebih padat. Sebaliknya, tempat \"Sangat Populer\" dengan ribuan ulasan rentan mengalami over-rating palsu atau penurunan kualitas akibat terlalu ramai (crowded), sehingga skornya stagnan di garis rata-rata.")
    st.success("🚀 **Insight Bisnis:** Algoritma sistem harus direkalibrasi untuk melawan bias viralitas. Jika sistem hanya mengurutkan rekomendasi berdasarkan volume ulasan, pengguna akan terus diarahkan ke tempat padat yang kualitasnya rata-rata. AI harus menaikkan visibilitas tempat \"Sepi\" yang memiliki skor tinggi agar pengguna mendapatkan pengalaman yang benar-benar berkualitas.")