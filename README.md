# Aplikasi Posyandu

![kivy](https://img.shields.io/badge/kivy-blue) ![Python](https://img.shields.io/badge/python-3.7-red) 

# Panduan Menjalankan Project Kivy

Dokumentasi ini akan memandu Anda melalui proses setup dan menjalankan project Kivy dari awal.

## Prerequisites

Pastikan Anda telah menginstall hal-hal berikut sebelum memulai:

- Python 3.7 atau yang lebih baru
- pip (package installer for Python)
- Git

## Langkah 1: Clone Repository

```bash
git clone https://github.com/username-anda/nama-repo-kivy.git
cd nama-repo-kivy
```

## Langkah 2: Setup Environment Virtual (Rekomendasi)
Kami sangat merekomendasikan menggunakan virtual environment untuk mengisolasi dependencies project.

Langkah 2: Setup Environment Virtual (Rekomendasi)
Kami sangat merekomendasikan menggunakan virtual environment untuk mengisolasi dependencies project.

# Untuk Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

# Untuk macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Langkah 3: Install Dependencies
Setelah environment virtual diaktifkan, install semua dependencies yang diperlukan:

```bash
pip install --upgrade pip
pip install kivy[base]
pip install -r requirements.txt
```
Jika file `requirements.txt` tidak tersedia, Anda bisa menginstall Kivy saja:

```bash
pip install kivy
```

## Langkah 4: Menjalankan Aplikasi
Jalankan aplikasi Kivy dengan perintah:
```bash
python main.py
```
Atau jika menggunakan Python 3 secara eksplisit:
```bash
python3 main.py
```

# Struktur Project

```bash
nama-repo-kivy/
├── main.py              # File utama aplikasi
├── requirements.txt     # Dependencies project
├── .gitignore          # File yang diignore oleh Git
├── assets/             # Folder untuk assets (images, fonts, etc.)
│   ├── images/
│   └── fonts/
└── README.md           # Dokumentasi ini
```

# Troubleshooting 🚀
## * Error: "No module named 'kivy'"
Pastikan Anda telah menginstall Kivy dan environment virtual sudah diaktifkan.

## * Error pada Windows: Microsoft Visual C++ 14.0 is required

Download dan install [Build Tools for Visual Studio 2019](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)

## * Error pada macOS: "Could not find a version that satisfies the requirement kivy"
Coba install dengan pip yang lebih baru:

```bash
pip install --upgrade pip
pip install kivy
```

## * Error: "Unable to find any valuable Window provider"

Pada sistem Linux, install dependencies berikut:
```bash
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev
```

# DUKUNGAN
## Jika Anda mengalami masalah dalam menjalankan project, silakan:

1. periksa [dokumentasi resmi kivy](https://kivy.org/doc/stable/)
2. cari solusi di [GitHub Issues](https://github.com/username-anda/nama-repo-kivy/issues)
3. Buat issue baru jika masalah belum terpecahkan

# Kontribusi

Kontribusi selalu diterima! Silakan:

1. Fork project ini
2. Buat branch untuk fitur Anda (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan Anda (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request
