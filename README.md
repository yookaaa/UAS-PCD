# Aplikasi Pengolahan Citra

Aplikasi web untuk pengolahan citra digital menggunakan Python, Streamlit, dan OpenCV.

## ✨ Fitur

- **Filtering & Restorasi**: Mean Filter, Median Filter, Adaptive Filter
- **Morfologi**: Dilasi, Erosi, Closing, Opening
- **Ruang Warna**: Pisah RGB, Konversi HSV, Konversi YIQ
- **Segmentasi**: Thresholding Binary, Thresholding Iteratif

## 🚀 Instalasi

### 1. Install Python
Download dan install Python dari [python.org](https://www.python.org/downloads/) (versi 3.8 atau lebih baru)

### 2. Clone Repository
```bash
git clone https://github.com/yookaaa/UAS-PCD.git
cd UAS-PCD
```

### 3. Install Dependencies
```bash
pip install streamlit
pip install opencv-python
pip install numpy
pip install pillow
```

### 4. Jalankan Aplikasi
```bash
streamlit run app.py
```

Buka browser dan akses: `http://localhost:8501`

## 📖 Cara Pakai

1. Upload gambar melalui sidebar
2. Pilih kategori operasi
3. Pilih jenis operasi
4. Atur parameter (jika ada)
5. Klik "Proses Gambar"

## 🛠️ Dependencies

Aplikasi ini membutuhkan 4 library Python:

| Library | Fungsi | Ukuran |
|---------|--------|--------|
| **streamlit** | Membuat web interface | ~10 MB |
| **opencv-python** | Memproses gambar (filter, morfologi, dll) | ~90 MB |
| **numpy** | Operasi matematika pada gambar | ~20 MB |
| **pillow** | Membaca file gambar | ~3 MB |

**Total download:** ~123 MB

### Cara Install:

**Opsi 1: Install otomatis via requirements.txt**
```bash
pip install -r requirements.txt
```

**Opsi 2: Install manual satu per satu**
```bash
pip install streamlit
pip install opencv-python
pip install numpy
pip install pillow
```

**Opsi 3: Install sekaligus**
```bash
pip install streamlit opencv-python numpy pillow
```

## ⚠️ Troubleshooting

**Error: "streamlit: command not found"**
```bash
python -m streamlit run app.py
```

**Error: "No module named 'cv2'"**
```bash
pip install opencv-python
```
