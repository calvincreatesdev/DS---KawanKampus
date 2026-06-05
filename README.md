# Kawan Kampus: Data Science Path

## Project Lifecycle

### 1. Data Wrangling (Gathering, Assessing, Cleaning)
*   **Handling Bus Stops:** Memberikan *value* 0 pada kategori *bus stop* karena berfungsi sebagai titik jemput/transisi (bukan destinasi utama).
*   **Data Type Conversion:** Mengonversi *total reviews* dari tipe desimal menjadi numerik integer agar bisa diolah secara matematis.
*   **Feature Reduction:** Menghapus kolom *komentar populer* yang tidak relevan dengan analisis spasial untuk meningkatkan performa dataset.
*   **Data Cleaning:** Menangani *missing values* dan menstandarisasi format data antar kampus.

### 2. Exploratory Data Analysis (EDA)
*   Menemukan pola distribusi fasilitas di berbagai radius kampus.
*   Analisis korelasi antara jarak tempuh dengan *User Trust Score*.
*   Identifikasi anomali data (misal: membandingkan fasilitas yang sangat populer vs fasilitas *underrated*).

### 3. Feature Engineering
*   **Skor Kepercayaan:** Menggabungkan *rating* dan *total reviews* untuk menciptakan metrik *place reliability*.
*   **Popularity Index:** Klasifikasi tempat populer berdasarkan volume *total reviews*.
*   **Spatial Analysis:** Mengimplementasikan *Haversine distance formula* berbasis koordinat (latitude/longitude) untuk mengkategorikan jarak tempuh (dekat, standar, jauh) antara kampus dan destinasi.

### 4. Dashboard
*   **https://imrn7fr247rul99qeaupa8.streamlit.app/**



## Tech Stack
* **Language:** Python
* **Data Processing:** Pandas, NumPy
* **EDA & Visualization:** Seaborn, Matplotlib
* **Dashboarding:** Streamlit
* **Environment:** Conda (Anaconda)



## Struktur Repository
```text
Kawan-Kampus/
├── Assets/               
│
├── Data/
│   ├── kawankampus_cleaned_data.csv
│   ├── kawankampus_feature_engineered.csv
│   ├── kawankampus_master_dataset.csv # Main Dataset     
│
├── Raw Dataset/          
├── dashboard.py          
├── eda.ipynb             
├── wrangling_data.ipynb  
├── requirements.txt      
├── AB_Testing_Analysis
├── KAWAN KAMPUS | TECHNICAL COMPREHENSIVE REPORT
├── Data Dictionary_Kawan Kampus Master Dataset
└── README.md             
