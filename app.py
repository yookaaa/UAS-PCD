import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Konfigurasi halaman
st.set_page_config(
    page_title="Aplikasi Pengolahan Citra",
    page_icon="🖼️",
    layout="wide"
)

# ==================== FUNGSI PEMROSESAN CITRA ====================

# --- Kelompok 1: Filtering & Restorasi ---
def mean_filtering(image, kernel_size=5):
    """Logika: Mengaburkan gambar dengan merata-ratakan piksel dalam kernel"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.blur(gray, (kernel_size, kernel_size))
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

def median_filtering(image, kernel_size=5):
    """Logika: Mengambil nilai tengah (median) untuk menghilangkan noise bintik"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.medianBlur(gray, kernel_size)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

def adaptive_filtering(image, kernel_size=5):
    """Logika: Bilateral filter untuk smoothing dengan mempertahankan edge"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.bilateralFilter(gray, kernel_size, 75, 75)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

# --- Kelompok 2: Morfologi ---
def dilasi(image, kernel_size=5):
    """Logika: Mempertebal objek putih (harus grayscale + threshold dulu)"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    result = cv2.dilate(thresh, kernel, iterations=1)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

def erosi(image, kernel_size=5):
    """Logika: Mengikis objek putih (harus grayscale + threshold dulu)"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    result = cv2.erode(thresh, kernel, iterations=1)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

def closing(image, kernel_size=5):
    """Logika Closing: Dilasi -> Erosi (Menutup lubang hitam kecil)"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    result = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

def opening(image, kernel_size=5):
    """Logika Opening: Erosi -> Dilasi (Menghilangkan noise putih kecil)"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    result = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

# --- Kelompok 3: Ruang Warna ---
def pisah_rgb(image):
    """Logika RGB: Menampilkan setiap channel dalam grayscale"""
    RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Ambil setiap channel dan tampilkan dalam grayscale
    red_channel = RGB[:,:,0]
    green_channel = RGB[:,:,1]
    blue_channel = RGB[:,:,2]
    
    # Konversi kembali ke BGR untuk display
    red_display = cv2.cvtColor(red_channel, cv2.COLOR_GRAY2BGR)
    green_display = cv2.cvtColor(green_channel, cv2.COLOR_GRAY2BGR)
    blue_display = cv2.cvtColor(blue_channel, cv2.COLOR_GRAY2BGR)
    
    return red_display, green_display, blue_display

def konversi_hsv(image):
    """Logika HSV: Konversi RGB ke HSV dan tampilkan per channel dalam grayscale"""
    RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    HSV = cv2.cvtColor(RGB, cv2.COLOR_RGB2HSV)
    
    # Ambil setiap channel
    hue = HSV[:,:,0]
    saturation = HSV[:,:,1]
    value = HSV[:,:,2]
    
    # Konversi ke BGR untuk display
    hue_display = cv2.cvtColor(hue, cv2.COLOR_GRAY2BGR)
    sat_display = cv2.cvtColor(saturation, cv2.COLOR_GRAY2BGR)
    val_display = cv2.cvtColor(value, cv2.COLOR_GRAY2BGR)
    
    return hue_display, sat_display, val_display

def konversi_yiq(image):
    """Logika NTSC / YIQ: Perhitungan matriks manual dengan clipping"""
    RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    im_array = np.array(RGB, dtype=np.float32)
    
    # Matriks konversi RGB ke YIQ
    trans_matrix = np.array([[0.299, 0.587, 0.114], 
                             [0.596, -0.274, -0.322], 
                             [0.211, -0.523, 0.312]])
    
    # Perkalian Dot Product
    im_yiq = np.dot(im_array, trans_matrix.T)
    
    # Clipping nilai agar tetap dalam range 0-255
    y = np.uint8(np.clip(im_yiq[:, :, 0], 0, 255))
    i = np.uint8(np.clip(im_yiq[:, :, 1], 0, 255))
    q = np.uint8(np.clip(im_yiq[:, :, 2], 0, 255))
    
    # Konversi ke BGR untuk display
    y_display = cv2.cvtColor(y, cv2.COLOR_GRAY2BGR)
    i_display = cv2.cvtColor(i, cv2.COLOR_GRAY2BGR)
    q_display = cv2.cvtColor(q, cv2.COLOR_GRAY2BGR)
    
    return y_display, i_display, q_display

# --- Kelompok 4: Segmentasi (Thresholding) ---
def thresholding_binary(image, threshold_value=127):
    """Logika: Thresholding untuk mengubah gambar jadi biner (Hitam/Putih)"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, result = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

def thresholding_iteratif(image):
    """Logika: Thresholding Iteratif menggunakan metode Otsu"""
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
                kernel_size = st.slider("Ukuran Kernel:", 3, 21, 5, step=2)
                params = {"kernel_size": kernel_size}
                st.info("ℹ️ Gambar akan di-threshold otomatis sebelum operasi morfologi")
                
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
                    threshold_value = st.slider("Nilai Threshold:", 0, 255, 100)
                    params = {"threshold_value": threshold_value}
                else:
                    params = {}
                    st.info("ℹ️ Menggunakan metode Otsu untuk threshold otomatis")
            
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
                        
                    elif operasi == "Thresholding Binary":
                        result_image = thresholding_binary(original_image, **params)
                        
                    elif operasi == "Thresholding Iteratif":
                        result_image = thresholding_iteratif(original_image)
                        
                    elif operasi == "Pisah RGB":
                        # Kasus khusus untuk pisah RGB
                        red, green, blue = pisah_rgb(original_image)
                        
                        st.subheader("📊 Hasil Pemisahan Channel RGB")
                        st.info("ℹ️ Setiap channel ditampilkan dalam grayscale")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            display_image(red, "🔴 Red Channel")
                        with col2:
                            display_image(green, "🟢 Green Channel")
                        with col3:
                            display_image(blue, "🔵 Blue Channel")
                        
                        st.success(f"✅ {operasi} berhasil diterapkan!")
                        return
                        
                    elif operasi == "Konversi HSV":
                        # Kasus khusus untuk HSV
                        hue, saturation, value = konversi_hsv(original_image)
                        
                        st.subheader("📊 Hasil Konversi HSV")
                        st.info("ℹ️ Setiap channel ditampilkan dalam grayscale")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            display_image(hue, "🌈 Hue Channel")
                        with col2:
                            display_image(saturation, "💧 Saturation Channel")
                        with col3:
                            display_image(value, "💡 Value Channel")
                        
                        st.success(f"✅ {operasi} berhasil diterapkan!")
                        return
                        
                    elif operasi == "Konversi YIQ":
                        # Kasus khusus untuk YIQ
                        y, i, q = konversi_yiq(original_image)
                        
                        st.subheader("📊 Hasil Konversi YIQ (NTSC)")
                        st.info("ℹ️ Setiap channel ditampilkan dalam grayscale")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            display_image(y, "📺 Y Channel (Luminance)")
                        with col2:
                            display_image(i, "🎨 I Channel (In-phase)")
                        with col3:
                            display_image(q, "🎭 Q Channel (Quadrature)")
                        
                        st.success(f"✅ {operasi} berhasil diterapkan!")
                        return
                    
                    # Tampilkan hasil (untuk operasi lainnya)
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
                
                ### 💡 Tips:
                - **Filtering**: Gunakan untuk mengurangi noise
                - **Morfologi**: Gambar akan di-threshold otomatis
                - **Ruang Warna**: Channel ditampilkan dalam grayscale
                - **Segmentasi**: Threshold Binary untuk binarisasi manual
                """)
    else:
        # Tampilan awal ketika belum ada gambar
        st.info("""
        ### 🚀 Selamat Datang di Aplikasi Pengolahan Citra!
        
        **Fitur yang tersedia:**
        
        **1. 🔍 Filtering & Restorasi**
        - Mean Filtering: Mengaburkan gambar dengan merata-ratakan piksel
        - Median Filtering: Menghilangkan salt & pepper noise
        - Adaptive Filtering: Bilateral filter untuk edge-preserving
        
        **2. 🔬 Morfologi**
        - Dilasi: Mempertebal objek putih
        - Erosi: Mengikis objek putih
        - Closing: Dilasi → Erosi (menutup lubang)
        - Opening: Erosi → Dilasi (hilangkan noise)
        
        **3. 🎨 Ruang Warna**
        - Pisah RGB: Tampilkan channel R, G, B dalam grayscale
        - Konversi HSV: Channel Hue, Saturation, Value
        - Konversi YIQ: Channel Y, I, Q (NTSC)
        
        **4. 📐 Segmentasi**
        - Thresholding Binary: Binarisasi dengan threshold manual
        - Thresholding Iteratif: Otomatis menggunakan metode Otsu
        
        ---
        
        **Untuk memulai, silakan upload gambar melalui sidebar di sebelah kiri! 👈**
        """)

if __name__ == "__main__":
    main()