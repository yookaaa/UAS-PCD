import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Konfigurasi halaman
st.set_page_config(
    page_title="Aplikasi Pengolahan Citra",
    page_icon="🖼️",
    layout="wide"
)

# ==================== FUNGSI PEMROSESAN CITRA ====================

# --- Kelompok 1: Filtering & Restorasi ---
def mean_filtering(image, kernel_size=5):
    """Menerapkan Mean Filter"""
    return cv2.blur(image, (kernel_size, kernel_size))

def median_filtering(image, kernel_size=5):
    """Menerapkan Median Filter"""
    return cv2.medianBlur(image, kernel_size)

def adaptive_filtering(image, kernel_size=5):
    """Menerapkan Adaptive Bilateral Filter"""
    return cv2.bilateralFilter(image, kernel_size, 75, 75)

# --- Kelompok 2: Morfologi ---
def dilasi(image, kernel_size=5):
    """Operasi Dilasi"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

def erosi(image, kernel_size=5):
    """Operasi Erosi"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

def closing(image, kernel_size=5):
    """Operasi Closing (Dilasi lalu Erosi)"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

def opening(image, kernel_size=5):
    """Operasi Opening (Erosi lalu Dilasi)"""
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# --- Kelompok 3: Ruang Warna ---
def pisah_rgb(image):
    """Memisahkan channel RGB"""
    b, g, r = cv2.split(image)
    
    # Buat gambar dengan channel tunggal
    zeros = np.zeros_like(b)
    
    red_channel = cv2.merge([zeros, zeros, r])
    green_channel = cv2.merge([zeros, g, zeros])
    blue_channel = cv2.merge([b, zeros, zeros])
    
    return red_channel, green_channel, blue_channel

def konversi_hsv(image):
    """Konversi ke HSV"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

def konversi_yiq(image):
    """Konversi ke NTSC (YIQ)"""
    # OpenCV tidak memiliki konversi langsung ke YIQ
    # Menggunakan transformasi manual
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Matrix transformasi RGB ke YIQ
    transform_matrix = np.array([
        [0.299, 0.587, 0.114],
        [0.596, -0.274, -0.322],
        [0.211, -0.523, 0.312]
    ])
    
    # Reshape untuk operasi matrix
    pixels = rgb.reshape(-1, 3)
    yiq = np.dot(pixels, transform_matrix.T)
    yiq = yiq.reshape(rgb.shape)
    
    # Normalisasi untuk display
    yiq = cv2.normalize(yiq, None, 0, 255, cv2.NORM_MINMAX)
    return yiq.astype(np.uint8)

# --- Kelompok 4: Segmentasi (Thresholding) ---
def thresholding_binary(image, threshold_value=127):
    """Thresholding Binary"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, result = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

def thresholding_iteratif(image, max_iterations=10):
    """Thresholding Iteratif (Otsu's method)"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

# ==================== FUNGSI HELPER ====================

def load_image(uploaded_file):
    """Memuat gambar dari file yang diunggah"""
    image = Image.open(uploaded_file)
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def display_image(image, caption):
    """Menampilkan gambar dengan caption"""
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    st.image(image_rgb, caption=caption, use_container_width=True)

# ==================== APLIKASI UTAMA ====================

def main():
    # Header
    st.title("🖼️ APLIKASI PENGOLAHAN CITRA")
    st.markdown("---")
    
    # Sidebar untuk kontrol
    with st.sidebar:
        st.header("⚙️ Pengaturan")
        
        # Upload gambar
        uploaded_file = st.file_uploader(
            "📤 Upload Image",
            type=["jpg", "jpeg", "png", "bmp"],
            help="Pilih gambar yang ingin diproses"
        )
        
        if uploaded_file is not None:
            st.success("✅ Gambar berhasil diunggah!")
            
            # Pilihan kategori operasi
            st.markdown("---")
            st.subheader("🎯 Pilih Operasi")
            
            kategori = st.selectbox(
                "Kategori:",
                [
                    "Filtering & Restorasi",
                    "Morfologi",
                    "Ruang Warna",
                    "Segmentasi"
                ]
            )
            
            # Pilihan operasi berdasarkan kategori
            if kategori == "Filtering & Restorasi":
                operasi = st.selectbox(
                    "Jenis Operasi:",
                    ["Mean Filtering", "Median Filtering", "Adaptive Filtering"]
                )
                kernel_size = st.slider("Ukuran Kernel:", 3, 15, 5, step=2)
                params = {"kernel_size": kernel_size}
                
            elif kategori == "Morfologi":
                operasi = st.selectbox(
                    "Jenis Operasi:",
                    ["Dilasi", "Erosi", "Closing", "Opening"]
                )
                kernel_size = st.slider("Ukuran Kernel:", 3, 15, 5, step=2)
                params = {"kernel_size": kernel_size}
                
            elif kategori == "Ruang Warna":
                operasi = st.selectbox(
                    "Jenis Operasi:",
                    ["Pisah RGB", "Konversi HSV", "Konversi YIQ"]
                )
                params = {}
                
            elif kategori == "Segmentasi":
                operasi = st.selectbox(
                    "Jenis Operasi:",
                    ["Thresholding Binary", "Thresholding Iteratif"]
                )
                if operasi == "Thresholding Binary":
                    threshold_value = st.slider("Nilai Threshold:", 0, 255, 127)
                    params = {"threshold_value": threshold_value}
                else:
                    params = {}
            
            # Tombol proses
            st.markdown("---")
            process_button = st.button("🔄 Proses Gambar", type="primary", use_container_width=True)
            reset_button = st.button("♻️ Reset", use_container_width=True)
            
        else:
            st.info("👆 Silakan upload gambar terlebih dahulu")
    
    # Area konten utama
    if uploaded_file is not None:
        # Load gambar
        original_image = load_image(uploaded_file)
        
        if reset_button:
            st.rerun()
        
        if process_button:
            with st.spinner("🔄 Memproses gambar..."):
                # Proses gambar berdasarkan operasi yang dipilih
                try:
                    if operasi == "Mean Filtering":
                        result_image = mean_filtering(original_image, **params)
                    elif operasi == "Median Filtering":
                        result_image = median_filtering(original_image, **params)
                    elif operasi == "Adaptive Filtering":
                        result_image = adaptive_filtering(original_image, **params)
                    elif operasi == "Dilasi":
                        result_image = dilasi(original_image, **params)
                    elif operasi == "Erosi":
                        result_image = erosi(original_image, **params)
                    elif operasi == "Closing":
                        result_image = closing(original_image, **params)
                    elif operasi == "Opening":
                        result_image = opening(original_image, **params)
                    elif operasi == "Konversi HSV":
                        result_image = konversi_hsv(original_image)
                    elif operasi == "Konversi YIQ":
                        result_image = konversi_yiq(original_image)
                    elif operasi == "Thresholding Binary":
                        result_image = thresholding_binary(original_image, **params)
                    elif operasi == "Thresholding Iteratif":
                        result_image = thresholding_iteratif(original_image)
                    elif operasi == "Pisah RGB":
                        # Kasus khusus untuk pisah RGB
                        red, green, blue = pisah_rgb(original_image)
                        
                        st.subheader("📊 Hasil Pemisahan Channel RGB")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            display_image(red, "🔴 Red Channel")
                        with col2:
                            display_image(green, "🟢 Green Channel")
                        with col3:
                            display_image(blue, "🔵 Blue Channel")
                        
                        st.success(f"✅ {operasi} berhasil diterapkan!")
                        return
                    
                    # Tampilkan hasil (untuk operasi selain Pisah RGB)
                    st.subheader("📊 Hasil Pengolahan")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 🖼️ Citra Awal")
                        display_image(original_image, "Gambar Original")
                    
                    with col2:
                        st.markdown("### ✨ Hasil Deteksi")
                        display_image(result_image, f"Hasil {operasi}")
                    
                    st.success(f"✅ {operasi} berhasil diterapkan!")
                    
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan: {str(e)}")
        else:
            # Tampilkan preview gambar original
            st.subheader("👀 Preview Gambar")
            col1, col2 = st.columns([1, 1])
            with col1:
                display_image(original_image, "Gambar Original - Siap Diproses")
            with col2:
                st.info("""
                ### 📝 Cara Penggunaan:
                1. Pilih **Kategori** operasi di sidebar
                2. Pilih **Jenis Operasi** yang diinginkan
                3. Atur parameter jika diperlukan
                4. Klik tombol **🔄 Proses Gambar**
                5. Lihat hasilnya di sini!
                """)
    else:
        # Tampilan awal ketika belum ada gambar
        st.info("""
        ### 🚀 Selamat Datang di Aplikasi Pengolahan Citra!
        
        **Fitur yang tersedia:**
        
        **1. 🔍 Filtering & Restorasi**
        - Mean Filtering
        - Median Filtering
        - Adaptive Filtering
        
        **2. 🔬 Morfologi**
        - Dilasi
        - Erosi
        - Closing
        - Opening
        
        **3. 🎨 Ruang Warna**
        - Pisah Channel RGB
        - Konversi HSV
        - Konversi YIQ
        
        **4. 📐 Segmentasi**
        - Thresholding Binary
        - Thresholding Iteratif
        
        ---
        
        **Untuk memulai, silakan upload gambar melalui sidebar di sebelah kiri! 👈**
        """)

if __name__ == "__main__":
    main()