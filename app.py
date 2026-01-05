import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(
    page_title="UAS PCD - Kelompok 1",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Sora:wght@400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', sans-serif;
        }

        /* Sembunyikan Branding Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Background Elegan Dark Gradient */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 25%, #0f3460 50%, #1a1a2e 100%);
            background-size: 400% 400%;
            animation: gradientFlow 15s ease infinite;
            color: #e4e4e7;
        }

        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Sidebar Modern Glassmorphism */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(26, 26, 46, 0.95) 0%, rgba(15, 52, 96, 0.95) 100%);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 4px 0 30px rgba(0, 0, 0, 0.5);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1.5rem;
        }

        /* Header Judul Premium */
        h1 {
            font-family: 'Sora', sans-serif;
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3rem !important;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
            text-align: center;
        }

        h2 {
            color: #60a5fa;
            font-weight: 600;
            font-size: 1.4rem !important;
            margin-top: 1.5rem;
        }

        h3 {
            color: #a78bfa;
            font-weight: 500;
            font-size: 1.1rem !important;
        }

        /* Banner Hero Premium */
        .hero-banner {
            position: relative;
            text-align: center;
            padding: 5rem 3rem;
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.1) 0%, rgba(167, 139, 250, 0.1) 100%);
            backdrop-filter: blur(30px);
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 3rem;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        }

        .hero-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(96, 165, 250, 0.15) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .hero-title {
            position: relative;
            font-family: 'Sora', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            letter-spacing: -1px;
        }

        .hero-subtitle {
            position: relative;
            font-size: 1.15rem;
            color: #94a3b8;
            font-weight: 400;
        }

        /* Kartu Fitur Premium */
        .feature-card {
            position: relative;
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.08) 0%, rgba(167, 139, 250, 0.08) 100%);
            backdrop-filter: blur(20px);
            padding: 2.5rem 2rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            text-align: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            height: 100%;
            min-height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 20px;
            padding: 1px;
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            opacity: 0;
            transition: opacity 0.4s ease;
        }

        .feature-card:hover {
            transform: translateY(-8px) scale(1.02);
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.15) 0%, rgba(167, 139, 250, 0.15) 100%);
            box-shadow: 0 20px 60px rgba(96, 165, 250, 0.3);
        }

        .feature-card:hover::before {
            opacity: 1;
        }

        .feature-icon {
            font-size: 4rem;
            margin-bottom: 1.5rem;
            filter: drop-shadow(0 0 20px rgba(96, 165, 250, 0.5));
            transition: transform 0.5s ease;
        }

        .feature-card:hover .feature-icon {
            transform: scale(1.2) rotateY(360deg);
        }

        .feature-title {
            font-family: 'Sora', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }

        .feature-desc {
            color: #94a3b8;
            font-size: 0.95rem;
            line-height: 1.7;
        }

        /* Kontainer Gambar Premium */
        .glass-container {
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.05) 0%, rgba(167, 139, 250, 0.05) 100%);
            backdrop-filter: blur(25px);
            padding: 2rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4);
            margin-bottom: 2rem;
        }

        .glass-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .glass-title {
            font-family: 'Sora', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .neon-badge {
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 20px rgba(96, 165, 250, 0.4);
        }

        /* Tombol Modern */
        div.stButton > button {
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            color: white;
            border: none;
            padding: 0.9rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            box-shadow: 0 8px 25px rgba(96, 165, 250, 0.3);
            width: 100%;
            text-transform: none;
            letter-spacing: 0.3px;
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 35px rgba(167, 139, 250, 0.5);
            background: linear-gradient(135deg, #a78bfa, #60a5fa);
        }

        /* Tombol Download */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #10b981, #059669) !important;
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3) !important;
        }

        .stDownloadButton > button:hover {
            box-shadow: 0 12px 35px rgba(16, 185, 129, 0.5) !important;
        }

        /* File Uploader Stylish */
        [data-testid="stFileUploader"] {
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.08) 0%, rgba(167, 139, 250, 0.08) 100%);
            backdrop-filter: blur(15px);
            border: 2px dashed rgba(96, 165, 250, 0.4);
            border-radius: 16px;
            padding: 2rem;
            transition: all 0.3s ease;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: rgba(167, 139, 250, 0.6);
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.12) 0%, rgba(167, 139, 250, 0.12) 100%);
        }

        [data-testid="stFileUploader"] label {
            color: #e4e4e7 !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
        }

        [data-testid="stFileUploader"] section {
            border: none !important;
            background: transparent !important;
        }

        [data-testid="stFileUploader"] section button {
            background: linear-gradient(135deg, #60a5fa, #a78bfa) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.7rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }

        [data-testid="stFileUploader"] section button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(96, 165, 250, 0.4) !important;
        }

        [data-testid="stFileUploader"] small {
            color: #94a3b8 !important;
            font-size: 0.85rem !important;
        }

        /* File yang sudah diupload */
        .uploadedFile {
            background: rgba(96, 165, 250, 0.1) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(96, 165, 250, 0.3) !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            margin-top: 1rem !important;
        }

        .uploadedFile button {
            background: transparent !important;
            color: #ef4444 !important;
        }

        /* Success Message Styling */
        .stSuccess {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.15) 100%) !important;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(16, 185, 129, 0.4) !important;
            border-radius: 12px !important;
            color: #10b981 !important;
            padding: 1rem !important;
            font-weight: 500 !important;
        }

        /* Selectbox Modern */
        div[data-baseweb="select"] {
            background: rgba(96, 165, 250, 0.08);
            backdrop-filter: blur(15px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        div[data-baseweb="select"] > div {
            background: transparent !important;
            border: none !important;
            color: #e4e4e7 !important;
        }

        /* Slider Elegan */
        .stSlider > div > div > div > div {
            background: linear-gradient(90deg, #60a5fa, #a78bfa) !important;
        }

        .stSlider > div > div > div > div > div {
            background: white !important;
            box-shadow: 0 0 10px rgba(96, 165, 250, 0.5);
        }

        /* Info Box */
        .stInfo {
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.12) 0%, rgba(167, 139, 250, 0.12) 100%) !important;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(96, 165, 250, 0.3) !important;
            border-radius: 12px !important;
            color: #93c5fd !important;
            padding: 1rem !important;
        }

        /* Alert Box */
        .stAlert {
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.12) 0%, rgba(167, 139, 250, 0.12) 100%);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(96, 165, 250, 0.3);
            border-radius: 12px;
            color: #93c5fd;
        }

        /* Tab Modern */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(96, 165, 250, 0.05);
            backdrop-filter: blur(15px);
            padding: 0.8rem;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 10px;
            color: #94a3b8;
            font-weight: 500;
            padding: 0.6rem 1.5rem;
            transition: all 0.3s ease;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            color: white;
            box-shadow: 0 4px 20px rgba(96, 165, 250, 0.4);
        }

        /* Kotak Statistik */
        .stats-box {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(5, 150, 105, 0.12) 100%);
            backdrop-filter: blur(15px);
            padding: 1.3rem;
            border-radius: 14px;
            border: 1px solid rgba(16, 185, 129, 0.3);
            text-align: center;
            margin-top: 1rem;
        }

        .stats-label {
            color: #94a3b8;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }

        .stats-value {
            font-family: 'Sora', sans-serif;
            color: #10b981;
            font-size: 1.3rem;
            font-weight: 700;
        }

        /* Badge Kelompok Modern */
        .team-badge {
            text-align: center;
            padding: 1.8rem;
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.08) 0%, rgba(167, 139, 250, 0.08) 100%);
            backdrop-filter: blur(20px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }

        .team-badge p {
            color: #94a3b8;
            font-size: 0.9rem;
            margin: 0;
            line-height: 2;
        }

        .team-badge strong {
            font-family: 'Sora', sans-serif;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.15rem;
            font-weight: 800;
        }

        /* Panel Kontrol Sidebar */
        .control-panel-title {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: linear-gradient(135deg, rgba(96, 165, 250, 0.1) 0%, rgba(167, 139, 250, 0.1) 100%);
            backdrop-filter: blur(15px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .control-panel-title h2 {
            font-size: 1.8rem;
            margin-bottom: 0.3rem;
            font-family: 'Sora', sans-serif;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }

        .control-panel-title p {
            color: #94a3b8;
            font-size: 0.85rem;
            margin: 0;
        }

        /* Section Headers di Sidebar */
        .sidebar-section-header {
            color: #93c5fd;
            font-size: 0.95rem;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            padding-left: 0.5rem;
            border-left: 3px solid #60a5fa;
        }

        /* Footer Premium */
        .footer {
            text-align: center;
            padding: 2.5rem;
            color: #64748b;
            font-size: 0.9rem;
            margin-top: 4rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }

        .footer-link {
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }

        /* Expander Styling */
        .streamlit-expanderHeader {
            background: rgba(96, 165, 250, 0.08);
            backdrop-filter: blur(15px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #e4e4e7 !important;
        }

        .streamlit-expanderHeader:hover {
            background: rgba(96, 165, 250, 0.12);
        }

        /* Label Styling */
        label {
            color: #e4e4e7 !important;
            font-weight: 500 !important;
        }

        /* Divider */
        hr {
            border-color: rgba(255, 255, 255, 0.08) !important;
            margin: 1.5rem 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==================== FUNGSI PEMROSESAN (CACHED) ====================

@st.cache_data
def mean_filtering(image, kernel_size=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.blur(gray, (kernel_size, kernel_size))
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

@st.cache_data
def median_filtering(image, kernel_size=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.medianBlur(gray, kernel_size)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

@st.cache_data
def adaptive_filtering(image, kernel_size=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    k = kernel_size if kernel_size % 2 == 1 else kernel_size + 1
    result = cv2.bilateralFilter(gray, k, 75, 75)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

@st.cache_data
def dilasi(image, kernel_size=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    result = cv2.dilate(thresh, kernel, iterations=1)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

@st.cache_data
def erosi(image, kernel_size=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    result = cv2.erode(thresh, kernel, iterations=1)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

@st.cache_data
def closing(image, kernel_size=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    result = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

@st.cache_data
def opening(image, kernel_size=5):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    result = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

@st.cache_data
def pisah_rgb(image):
    RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    r, g, b = RGB[:,:,0], RGB[:,:,1], RGB[:,:,2]
    return (cv2.cvtColor(r, cv2.COLOR_GRAY2BGR), 
            cv2.cvtColor(g, cv2.COLOR_GRAY2BGR), 
            cv2.cvtColor(b, cv2.COLOR_GRAY2BGR))

@st.cache_data
def konversi_hsv(image):
    RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    HSV = cv2.cvtColor(RGB, cv2.COLOR_RGB2HSV)
    h, s, v = HSV[:,:,0], HSV[:,:,1], HSV[:,:,2]
    return (cv2.cvtColor(h, cv2.COLOR_GRAY2BGR), 
            cv2.cvtColor(s, cv2.COLOR_GRAY2BGR), 
            cv2.cvtColor(v, cv2.COLOR_GRAY2BGR))

@st.cache_data
def konversi_yiq(image):
    RGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    im_array = np.array(RGB, dtype=np.float32)
    trans_matrix = np.array([[0.299, 0.587, 0.114], 
                             [0.596, -0.274, -0.322], 
                             [0.211, -0.523, 0.312]])
    im_yiq = np.dot(im_array, trans_matrix.T)
    y = np.uint8(np.clip(im_yiq[:, :, 0], 0, 255))
    i = np.uint8(np.clip(im_yiq[:, :, 1], 0, 255))
    q = np.uint8(np.clip(im_yiq[:, :, 2], 0, 255))
    return (cv2.cvtColor(y, cv2.COLOR_GRAY2BGR), 
            cv2.cvtColor(i, cv2.COLOR_GRAY2BGR), 
            cv2.cvtColor(q, cv2.COLOR_GRAY2BGR))

@st.cache_data
def thresholding_binary(image, threshold_value=127):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, result = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

@st.cache_data
def thresholding_iteratif(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

# ==================== FUNGSI HELPER ====================

def load_image(uploaded_file):
    image = Image.open(uploaded_file)
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def convert_image_to_bytes(image_array):
    image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(image_rgb)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# ==================== APLIKASI UTAMA ====================

def main():
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("""
            <div class='control-panel-title'>
                <h2>🎛️ Panel Kontrol</h2>
                <p>Pusat Pengolahan Citra</p>
            </div>
        """, unsafe_allow_html=True)
        
        # File Uploader
        st.markdown("<div class='sidebar-section-header'>📁 Unggah Gambar</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Pilih file gambar",
            type=["jpg", "jpeg", "png"],
            help="Format: JPG, JPEG, PNG (Maks. 200MB)",
            label_visibility="collapsed"
        )

        params = {}
        operasi = None
        kategori = None

        if uploaded_file:
            st.success("✅ Gambar Berhasil Dimuat!")
            
            st.markdown("---")
            
            # Kategori Pemrosesan
            st.markdown("<div class='sidebar-section-header'>🛠️ Pilih Operasi</div>", unsafe_allow_html=True)
            kategori = st.selectbox(
                "Kategori Pemrosesan",
                ["Filtering", "Morfologi", "RGB", "Segmentasi"],
                help="Pilih kategori pemrosesan",
                label_visibility="collapsed"
            )

            st.markdown("---")

            if kategori == "Filtering":
                st.markdown("<div class='sidebar-section-header'>🔍 Mode Filtering</div>", unsafe_allow_html=True)
                operasi = st.selectbox("Metode Filter", ["Mean", "Median", "Adaptive"])
                
                st.markdown("**Intensitas Kernel**")
                kernel_size = st.slider("Ukuran", 3, 15, 5, step=2, label_visibility="collapsed")
                params = {"kernel_size": kernel_size}
                st.info(f"Ukuran kernel: {kernel_size}x{kernel_size}")
            
            elif kategori == "Morfologi":
                st.markdown("<div class='sidebar-section-header'>🧬 Mode Morfologi</div>", unsafe_allow_html=True)
                operasi = st.selectbox("Operasi Morfologi", ["Dilasi", "Erosi", "Closing", "Opening"])
                
                st.markdown("**Ukuran Kernel**")
                kernel_size = st.slider("Ukuran", 3, 21, 5, step=2, label_visibility="collapsed")
                params = {"kernel_size": kernel_size}
                st.info(f"Ukuran kernel: {kernel_size}x{kernel_size}")
            
            elif kategori == "RGB":
                st.markdown("<div class='sidebar-section-header'>🎨 RGB</div>", unsafe_allow_html=True)
                operasi = st.selectbox("Konversi Warna", ["Pisah RGB", "Konversi HSV", "Konversi YIQ"])
            
            elif kategori == "Segmentasi":
                st.markdown("<div class='sidebar-section-header'>📐 Mode Segmentasi</div>", unsafe_allow_html=True)
                operasi = st.selectbox("Metode Segmentasi", ["Binary Threshold", "Otsu Threshold"])
                if operasi == "Binary Threshold":
                    st.markdown("**Nilai Threshold**")
                    thresh = st.slider("Threshold", 0, 255, 127, label_visibility="collapsed")
                    params = {"threshold_value": thresh}
                    st.info(f"Threshold: {thresh}")

        st.markdown("---")
        st.markdown("""
            <div class='team-badge'>
                <p>
                    <strong>KELOMPOK 1</strong><br>
                    Praktikum Pengolahan<br>
                    Citra Digital
                </p>
            </div>
        """, unsafe_allow_html=True)

    # --- Halaman Utama ---
    
    if uploaded_file is None:
        # ========== LANDING PAGE ==========
        st.markdown("""
            <div class='hero-banner'>
                <div class='hero-title'>✨ PENGOLAHAN CITRA DIGITAL</div>
                <div class='hero-subtitle'>Platform Computer Vision dengan Teknologi Terkini</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        features = [
            ("🔍", "Filtering", "Reduksi noise dan penghalusan gambar menggunakan teknik filtering canggih"),
            ("🧬", "Morfologi", "Analisis bentuk dengan operasi morfologi untuk deteksi objek"),
            ("🎨", "RGB", "Konversi dan analisis RGB melalui berbagai model"),
            ("📐", "Segmentasi", "Pemisahan objek menggunakan algoritma thresholding cerdas")
        ]
        
        for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
            with col:
                st.markdown(f"""
                    <div class='feature-card'>
                        <div class='feature-icon'>{icon}</div>
                        <div class='feature-title'>{title}</div>
                        <div class='feature-desc'>{desc}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("👋 Unggah gambar melalui sidebar untuk memulai pemrosesan")
        
    else:
        # ========== MODE EDITOR ==========
        original_image = load_image(uploaded_file)
        height, width, channels = original_image.shape
        
        # Layout Berdampingan
        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            st.markdown("""
                <div class='glass-container'>
                    <div class='glass-header'>
                        <div class='glass-title'>📷 Gambar Asli</div>
                        <div class='neon-badge'>Input</div>
                    </div>
            """, unsafe_allow_html=True)
            
            st.image(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB), use_container_width=True)
            
            st.markdown(f"""
                <div class='stats-box'>
                    <div class='stats-label'>Dimensi</div>
                    <div class='stats-value'>{width} × {height} px</div>
                </div>
                </div>
            """, unsafe_allow_html=True)

        # Proses Gambar
        result_image = None
        results_list = []
        labels = []

        if operasi:
            try:
                if kategori == "Filtering":
                    if operasi == "Mean": result_image = mean_filtering(original_image, **params)
                    elif operasi == "Median": result_image = median_filtering(original_image, **params)
                    elif operasi == "Adaptive": result_image = adaptive_filtering(original_image, **params)
                
                elif kategori == "Morfologi":
                    if operasi == "Dilasi": result_image = dilasi(original_image, **params)
                    elif operasi == "Erosi": result_image = erosi(original_image, **params)
                    elif operasi == "Closing": result_image = closing(original_image, **params)
                    elif operasi == "Opening": result_image = opening(original_image, **params)

                elif kategori == "Segmentasi":
                    if operasi == "Binary Threshold": result_image = thresholding_binary(original_image, **params)
                    elif operasi == "Otsu Threshold": result_image = thresholding_iteratif(original_image)

                elif kategori == "RGB":
                    if operasi == "Pisah RGB": 
                        results_list = pisah_rgb(original_image)
                        labels = ["🔴 Kanal Merah", "🟢 Kanal Hijau", "🔵 Kanal Biru"]
                    elif operasi == "Konversi HSV": 
                        results_list = konversi_hsv(original_image)
                        labels = ["🌈 Hue", "💧 Saturation", "☀️ Value"]
                    elif operasi == "Konversi YIQ": 
                        results_list = konversi_yiq(original_image)
                        labels = ["💡 Luminance (Y)", "📊 In-phase (I)", "📈 Quadrature (Q)"]

            except Exception as e:
                st.error(f"❌ Kesalahan: {e}")

        # Hasil di Kolom Kanan
        with col_right:
            st.markdown(f"""
                <div class='glass-container'>
                    <div class='glass-header'>
                        <div class='glass-title'>✨ Hasil: {operasi if operasi else 'Menunggu'}</div>
                        <div class='neon-badge'>Output</div>
                    </div>
            """, unsafe_allow_html=True)
            
            if result_image is not None:
                st.image(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB), use_container_width=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                download_byte = convert_image_to_bytes(result_image)
                st.download_button(
                    label="📥 Unduh Hasil",
                    data=download_byte,
                    file_name=f"hasil_{operasi}.png",
                    mime="image/png",
                    use_container_width=True
                )
            
            elif results_list:
                tabs = st.tabs(labels)
                for i, tab in enumerate(tabs):
                    with tab:
                        st.image(cv2.cvtColor(results_list[i], cv2.COLOR_BGR2RGB), use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            else:
                st.info("⏳ Pilih operasi dari sidebar untuk melihat hasil")
                st.markdown('</div>', unsafe_allow_html=True)

        # Informasi Tambahan
        if operasi:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("ℹ️ Informasi Operasi"):
                operation_info = {
                    "Mean": "Filter mean menggunakan nilai rata-rata pixel dalam kernel untuk mengurangi noise.",
                    "Median": "Filter median mengganti pixel dengan nilai median dari kernel, efektif untuk noise salt-and-pepper.",
                    "Adaptive": "Filter adaptif (Bilateral) mempertahankan tepi sambil mengurangi noise.",
                    "Dilasi": "Dilasi memperluas area terang pada citra biner.",
                    "Erosi": "Erosi mengikis area terang pada citra biner.",
                    "Closing": "Closing adalah dilasi diikuti erosi, menutup celah kecil.",
                    "Opening": "Opening adalah erosi diikuti dilasi, menghilangkan noise kecil.",
                    "Pisah RGB": "Memisahkan citra menjadi kanal Merah, Hijau, dan Biru.",
                    "Konversi HSV": "Mengonversi ke model warna Hue, Saturation, Value.",
                    "Konversi YIQ": "Mengonversi ke model warna YIQ yang digunakan dalam broadcasting.",
                    "Binary Threshold": "Segmentasi dengan nilai threshold manual.",
                    "Otsu Threshold": "Segmentasi otomatis menggunakan metode Otsu."
                }
                st.write(operation_info.get(operasi, "Informasi tidak tersedia."))

    # Footer
    st.markdown("""
        <div class='footer'>
            <p>Dibuat oleh <span class='footer-link'>Kelompok 1</span> | 
            Laboratorium Pengolahan Citra Digital</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()