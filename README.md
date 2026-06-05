# Kawan Kampus: Data Science Path

## Project Lifecycle
Untuk menghasilkan *dashboard* yang akurat, alur kerja proyek ini meliputi beberapa tahapan teknis:

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

### 4. Dashboarding
*   Visualisasi interaktif menggunakan Streamlit untuk mempermudah *stakeholder* memahami *spatial distribution* dan *risk assessment* infrastruktur.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Processing:** Pandas, NumPy
* **EDA & Visualization:** Seaborn, Matplotlib
* **Dashboarding:** Streamlit
* **Environment:** Conda (Anaconda)

## 📂 Struktur Repositori
```text
Kawan-Kampus/
├── Assets/             # Branding & visual assets
├── Data/               # Master datasets & processed files
├── Raw Dataset/        # Original source files
├── dashboard.py        # Streamlit Main App
├── eda.ipynb           # Exploratory Data Analysis Notebook
├── wrangling_data.ipynb# Wrangling & Feature Engineering Notebook
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
