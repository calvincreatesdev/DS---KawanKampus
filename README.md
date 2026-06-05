# Kawan Kampus: Urban Infrastructure & Spatial Analytics 2026

![Logo Kawan Kampus](assets/logo_kawan_kampus.jpg)

*Dashboard* ini adalah **Decision Support Tool** yang dirancang untuk mengevaluasi infrastruktur perkotaan dan aksesibilitas fasilitas bagi mahasiswa. Dengan memanfaatkan *spatial data*, proyek ini memberikan *actionable insights* untuk mengoptimalkan *AI-based recommendation system* dan layanan fasilitas kampus.

## 🚀 Fitur Utama & Kemampuan Analitik
* **Spatial Accessibility Mapping:** Mengevaluasi distribusi fasilitas berdasarkan radius transit (Jalan Kaki vs. Bermotor).
* **Hidden Gems Discovery:** Menggunakan analisis kuadran untuk mengidentifikasi fasilitas produktivitas (Cafe/Kedai) yang berkualitas tinggi namun berada di area periferal.
* **Emergency Risk Mitigation:** Mendeteksi "Zona Merah" atau area dengan *critical gap* pada infrastruktur medis darurat (Apotek).
* **Commuter Mobility Insights:** Menganalisis kesenjangan antara halte transportasi publik formal dengan ekspansi logistik ritel (Minimarket).
* **Bias-Aware Recommendation:** Menggunakan *logarithmic distribution analysis* untuk melawan *popularity bias* dan menonjolkan fasilitas berkualitas yang *underrated*.

## 🛠️ Tech Stack
* **Language:** Python
* **Web Framework:** Streamlit
* **Analytical Libraries:** Pandas, Seaborn, Matplotlib
* **Deployment:** Streamlit Cloud

## 📂 Struktur Repositori
```text
├── assets/             # Branding & visual assets
├── data/               # Master datasets
├── notebooks/          # EDA & Feature Engineering workstreams
├── dashboard.py        # Main Streamlit application entry point
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
