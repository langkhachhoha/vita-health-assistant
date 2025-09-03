import streamlit as st
import json
import os
from datetime import datetime
import base64
import os

dir = os.getcwd()
# Import CCCD OCR Client
try:
    from cccd_client import ocr_client, start_ocr_server_if_needed, display_extracted_info
    CCCD_OCR_AVAILABLE = True
except ImportError:
    CCCD_OCR_AVAILABLE = False

st.set_page_config(
    page_title="Doctor App - Trang Chủ",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Function to encode image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Get images for styling
doctor_image_path = os.path.join(dir, "image", "Homepage.png")
doctor_base64 = get_base64_image(doctor_image_path)

vinbig_logo_path = os.path.join(dir, "image", "logo_vinbig.png")
vinbig_logo_base64 = get_base64_image(vinbig_logo_path)

# Enhanced Medical Styling
if doctor_base64:
    background_style = f"background-image: url('data:image/png;base64,{doctor_base64}');"
else:
    background_style = "background: linear-gradient(135deg, #f0f8ff 0%, #e1f2ff 25%, #d1ecff 50%, #c1e6ff 75%, #b1e0ff 100%);"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
    /* Hide Streamlit UI Elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    [data-testid="stToolbar"] {{display: none;}}
    [data-testid="stDecoration"] {{display: none;}}
    [data-testid="stStatusWidget"] {{display: none;}}
    [data-testid="manage-app-button"] {{display: none;}}

    /* Global Scroll Animation Setup */
    html {{
        scroll-behavior: smooth;
    }}
    
    .stApp {{
        {background_style}
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: 'Outfit', 'Inter', sans-serif;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, 
            rgba(240, 248, 255, 0.85) 0%, 
            rgba(225, 242, 255, 0.8) 25%,
            rgba(209, 236, 255, 0.75) 50%,
            rgba(193, 230, 255, 0.8) 75%,
            rgba(177, 224, 255, 0.85) 100%);
        z-index: 0;
        pointer-events: none;
        animation: backgroundShift 20s ease-in-out infinite;
    }}
    
    @keyframes backgroundShift {{
        0%, 100% {{ 
            background: linear-gradient(135deg, 
                rgba(240, 248, 255, 0.85) 0%, 
                rgba(225, 242, 255, 0.8) 25%,
                rgba(209, 236, 255, 0.75) 50%,
                rgba(193, 230, 255, 0.8) 75%,
                rgba(177, 224, 255, 0.85) 100%);
        }}
        50% {{ 
            background: linear-gradient(135deg, 
                rgba(177, 224, 255, 0.85) 0%, 
                rgba(193, 230, 255, 0.8) 25%,
                rgba(209, 236, 255, 0.75) 50%,
                rgba(225, 242, 255, 0.8) 75%,
                rgba(240, 248, 255, 0.85) 100%);
        }}
    }}

    @keyframes shimmer {{
        0% {{ transform: translateX(-100%); }}
        100% {{ transform: translateX(100%); }}
    }}
    
    /* Advanced Animation Classes */
    .animate-on-scroll {{
        opacity: 0;
        transform: translateY(50px);
        transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }}
    
    .animate-on-scroll.animate {{
        opacity: 1;
        transform: translateY(0);
    }}
    
    .slide-in-left {{
        opacity: 0;
        transform: translateX(-100px);
        animation: slideInLeft 1.2s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
    }}
    
    .slide-in-right {{
        opacity: 0;
        transform: translateX(100px);
        animation: slideInRight 1.2s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
    }}
    
    .fade-in-up {{
        opacity: 0;
        transform: translateY(30px);
        animation: fadeInUp 1s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
    }}
    
    .scale-in {{
        opacity: 0;
        transform: scale(0.8);
        animation: scaleIn 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
    }}
    
    @keyframes slideInLeft {{
        0% {{
            opacity: 0;
            transform: translateX(-100px);
        }}
        100% {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes slideInRight {{
        0% {{
            opacity: 0;
            transform: translateX(100px);
        }}
        100% {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    @keyframes fadeInUp {{
        0% {{
            opacity: 0;
            transform: translateY(30px);
        }}
        100% {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes scaleIn {{
        0% {{
            opacity: 0;
            transform: scale(0.8);
        }}
        100% {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    /* Staggered Animation Delays */
    .delay-100 {{ animation-delay: 0.1s; }}
    .delay-200 {{ animation-delay: 0.2s; }}
    .delay-300 {{ animation-delay: 0.3s; }}
    .delay-400 {{ animation-delay: 0.4s; }}
    .delay-500 {{ animation-delay: 0.5s; }}
    .delay-600 {{ animation-delay: 0.6s; }}
    .delay-700 {{ animation-delay: 0.7s; }}
    .delay-800 {{ animation-delay: 0.8s; }}
    
    .main-container {{
        position: relative;
        z-index: 10;
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }}
    
    .hero-section {{
        text-align: center;
        margin-bottom: 3rem;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(248, 252, 255, 0.92) 50%, 
            rgba(240, 248, 255, 0.95) 100%);
        border-radius: 20px;
        position: relative;
        box-shadow: 
            0 15px 35px rgba(0, 102, 204, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        border: 3px solid transparent;
        background-clip: padding-box;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        overflow: hidden;
    }}
    
    .hero-section::before {{
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(45deg, 
            #87ceeb, #87cefa, #add8e6, #b0e0e6,
            #e0f6ff, #b0e0e6, #add8e6, #87ceeb);
        background-size: 400% 400%;
        border-radius: 23px;
        z-index: -1;
        animation: borderFlow 4s ease-in-out infinite;
    }}
    
    .hero-section:hover {{
        transform: translateY(-3px);
        box-shadow: 
            0 20px 40px rgba(0, 102, 204, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
    }}
    
    @keyframes borderFlow {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    .main-title {{
        font-size: 3.2rem;
        font-weight: 700;
        color: #003366;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0, 102, 204, 0.2);
    }}
    
    .subtitle {{
        font-size: 1.2rem;
        color: #0066cc;
        font-weight: 500;
        margin-bottom: 2rem;
        line-height: 1.5;
    }}
    
    /* Enhanced Medical Icons with Advanced Animations */
    .medical-icons {{
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
        font-size: 2.5rem;
    }}
    
    .medical-icon {{
        transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        filter: grayscale(30%);
        cursor: pointer;
        position: relative;
        display: inline-block;
    }}
    
    .medical-icon::after {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: all 0.3s ease;
        z-index: -1;
    }}
    
    .medical-icon:hover {{
        transform: translateY(-10px) scale(1.2) rotate(10deg);
        filter: grayscale(0%) brightness(1.2);
        text-shadow: 0 0 20px currentColor;
    }}
    
    .medical-icon:hover::after {{
        width: 60px;
        height: 60px;
    }}
    
    .medical-icon:nth-child(1) {{ 
        color: #e74c3c;
        animation: iconFloat 3s ease-in-out infinite;
    }}
    .medical-icon:nth-child(2) {{ 
        color: #f39c12;
        animation: iconFloat 3s ease-in-out infinite 0.6s;
    }}
    .medical-icon:nth-child(3) {{ 
        color: #3498db;
        animation: iconFloat 3s ease-in-out infinite 1.2s;
    }}
    .medical-icon:nth-child(4) {{ 
        color: #27ae60;
        animation: iconFloat 3s ease-in-out infinite 1.8s;
    }}
    .medical-icon:nth-child(5) {{ 
        color: #9b59b6;
        animation: iconFloat 3s ease-in-out infinite 2.4s;
    }}
    
    @keyframes iconFloat {{
        0%, 100% {{ transform: translateY(0) rotate(0deg); }}
        50% {{ transform: translateY(-10px) rotate(5deg); }}
    }}
    
    /* Scroll-triggered Info Cards */
    .info-card {{
        background: linear-gradient(135deg, 
            rgba(245, 245, 245, 0.95) 0%, 
            rgba(235, 235, 235, 0.9) 100%);
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 30px rgba(0, 102, 204, 0.15);
        border: 2px solid rgba(0, 102, 204, 0.2);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    
    .info-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.6), 
            transparent);
        transition: left 0.6s ease;
    }}
    
    .info-card:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 102, 204, 0.25);
        border-color: rgba(0, 102, 204, 0.4);
        background: linear-gradient(135deg, 
            rgba(250, 250, 250, 0.98) 0%, 
            rgba(240, 240, 240, 0.95) 100%);
    }}
    
    .info-card:hover::before {{
        left: 100%;
    }}
    
    .card-icon {{
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
        transition: all 0.3s ease;
    }}
    
    .info-card:hover .card-icon {{
        transform: scale(1.1) rotate(5deg);
        filter: drop-shadow(0 0 10px currentColor);
    }}
    
    .card-title {{
        font-size: 1.3rem;
        font-weight: 700;
        color: #003366;
        margin-bottom: 1rem;
        transition: color 0.3s ease;
    }}
    
    .info-card:hover .card-title {{
        color: #0066cc;
    }}
    
    .card-content {{
        color: #0066cc;
        line-height: 1.6;
        font-size: 1rem;
        transition: color 0.3s ease;
    }}
    
    .info-card:hover .card-content {{
        color: #003366;
    }}
    
    /* Advanced Form Animations */
    .form-container {{
        background: linear-gradient(135deg, 
            rgba(245, 245, 245, 0.95) 0%, 
            rgba(235, 235, 235, 0.9) 50%, 
            rgba(230, 230, 230, 0.95) 100%);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 
            0 20px 40px rgba(0, 102, 204, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
        border: 2px solid rgba(0, 102, 204, 0.25);
        backdrop-filter: blur(15px);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }}
    
    .form-container::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(
            transparent,
            rgba(0, 188, 212, 0.1),
            transparent,
            rgba(0, 102, 204, 0.1),
            transparent
        );
        animation: formRotate 20s linear infinite;
        z-index: -1;
    }}
    
    @keyframes formRotate {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    .form-title {{
        font-size: 2rem;
        font-weight: 800;
        color: #003366;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
    }}
    
    .form-title::after {{
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(45deg, #0066cc, #4da6ff);
        border-radius: 2px;
        animation: titleUnderline 2s ease-in-out infinite;
    }}
    
    @keyframes titleUnderline {{
        0%, 100% {{ width: 100px; }}
        50% {{ width: 150px; }}
    }}
    
    .success-message {{
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 15px 30px rgba(76, 175, 80, 0.3);
        animation: successPulse 2s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }}
    
    .success-message::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.3), 
            transparent);
        animation: successShine 3s ease-in-out infinite;
    }}
    
    @keyframes successPulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.02); }}
    }}
    
    @keyframes successShine {{
        0% {{ left: -100%; }}
        100% {{ left: 100%; }}
    }}
    
    /* Beautiful Sidebar Styling - Simplified */
    .css-1d391kg {{
        background: linear-gradient(145deg, 
            #1a237e 0%,
            #3949ab 25%, 
            #5c6bc0 50%, 
            #7986cb 75%, 
            #9fa8da 100%) !important;
        border-right: 4px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3) !important;
    }}
    
    /* Sidebar Text Colors */
    .css-1d391kg .stMarkdown p,
    .css-1d391kg .stMarkdown h1,
    .css-1d391kg .stMarkdown h2,
    .css-1d391kg .stMarkdown h3 {{
        color: #ffffff !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }}
    
    /* Sidebar Navigation */
    .css-1d391kg [data-testid="stSidebarNav"] {{
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
    }}
    
    .css-1d391kg [data-testid="stSidebarNav"] a {{
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 0.8rem 1.2rem !important;
        border-radius: 10px !important;
        background: rgba(255, 255, 255, 0.1) !important;
        margin: 0.3rem 0 !important;
        transition: all 0.3s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }}
    
    .css-1d391kg [data-testid="stSidebarNav"] a:hover {{
        background: rgba(255, 255, 255, 0.25) !important;
        transform: translateX(8px) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
    }}
    
    /* Sidebar Info and Success boxes */
    .css-1d391kg .stAlert {{
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }}
    
    .css-1d391kg .stAlert p {{
        color: #ffffff !important;
        font-weight: 500 !important;
    }}
    
    /* Advanced JavaScript Scroll Animations */
    .scroll-fade-in {{
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }}
    
    .scroll-fade-in.active {{
        opacity: 1;
        transform: translateY(0);
    }}
    
    .scroll-slide-left {{
        opacity: 0;
        transform: translateX(-50px);
        transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }}
    
    .scroll-slide-left.active {{
        opacity: 1;
        transform: translateX(0);
    }}
    
    .scroll-slide-right {{
        opacity: 0;
        transform: translateX(50px);
        transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }}
    
    .scroll-slide-right.active {{
        opacity: 1;
        transform: translateX(0);
    }}
    
    .scroll-scale-in {{
        opacity: 0;
        transform: scale(0.9);
        transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }}
    
    .scroll-scale-in.active {{
        opacity: 1;
        transform: scale(1);
    }}
    </style>
    
    <script>
    // Advanced Scroll Animation Script
    function initScrollAnimations() {{
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};
        
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('active');
                }}
            }});
        }}, observerOptions);
        
        // Observe elements with scroll animation classes
        document.querySelectorAll('.scroll-fade-in, .scroll-slide-left, .scroll-slide-right, .scroll-scale-in').forEach(el => {{
            observer.observe(el);
        }});
    }}
    
    // Enhanced Icon Hover Effects
    function addIconEffects() {{
        document.querySelectorAll('.medical-icon').forEach((icon, index) => {{
            icon.addEventListener('mouseenter', function() {{
                const randomRotation = (Math.random() * 20 - 10);
                this.style.transform = `translateY(-15px) scale(1.3) rotate(${{randomRotation}}deg)`;
                this.style.filter = 'grayscale(0%) brightness(1.3) drop-shadow(0 0 20px currentColor)';
            }});
            
            icon.addEventListener('mouseleave', function() {{
                this.style.transform = '';
                this.style.filter = '';
            }});
        }});
    }}
    
    // Initialize when page loads
    document.addEventListener('DOMContentLoaded', function() {{
        initScrollAnimations();
        addIconEffects();
        
        // Add parallax effect to background
        window.addEventListener('scroll', function() {{
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            document.querySelector('.stApp::before')?.style.setProperty('transform', `translateY(${{rate}}px)`);
        }});
    }});
    
    // Retry initialization for Streamlit's dynamic loading
    setTimeout(() => {{
        initScrollAnimations();
        addIconEffects();
    }}, 1000);
    
    setTimeout(() => {{
        initScrollAnimations();
        addIconEffects();
    }}, 3000);
    </script>
    """,
    unsafe_allow_html=True
)

# Header with logo
if vinbig_logo_base64:
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <img src="data:image/png;base64,{vinbig_logo_base64}" 
                 style="height: 80px; border-radius: 10px; box-shadow: 0 10px 25px rgba(0,102,204,0.3);"
                 alt="VinBig Logo"/>
        </div>
        """,
        unsafe_allow_html=True
    )

# Sidebar với thông tin liên hệ và animation bác sĩ
with st.sidebar:
    # Doctor Animation - simplified
    st.markdown("### 🏥 VinBig Doctor App")
    
    # Animated doctor section
    st.markdown(
        """
        <div style="text-align: center; margin: 2rem 0;">
            <div style="font-size: 4rem; animation: bounce 2s infinite;">🧬🦠🧪🌡️</div>
            <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem;">
                <span style="font-size: 2rem; animation: float 3s infinite;">👩‍⚕️</span>
                <span style="font-size: 2rem; animation: float 3s infinite 0.5s;">🩺</span>
                <span style="font-size: 2rem; animation: float 3s infinite 1s;">⚕️🏩</span>
            </div>
        </div>
        
        <style>
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        @keyframes float {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-5px) scale(1.1); }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Contact Information - using Streamlit components
    st.markdown("### 📞 **THÔNG TIN LIÊN HỆ**")
    
    # Contact details
    st.info("""
    **📱 Hotline 24/7**  
    091-606-1368
    
    **📧 Email Hỗ Trợ**  
    haminhhieu1005@gmail.com 
    
    **🏢 Địa Chỉ**  
    Century Tower, Hà Nội
    
    **🕒 Giờ Làm Việc**  
    24/7 - Luôn sẵn sàng
    
    **🚨 Cấp Cứu**  
    115 - Miễn phí
    """)
    
    st.markdown("---")
    
    # Additional info
    st.success("✅ Hệ thống AI hỗ trợ chẩn đoán")
    st.warning("⚠️ Chỉ mang tính chất tham khảo")
    
    # Medical icons animation
    st.markdown(
        """
        <div style="text-align: center; margin: 1rem 0; font-size: 1.5rem;">
            <span style="animation: pulse 2s infinite;">🩺</span>
            <span style="animation: pulse 2s infinite 0.3s;">💊</span>
            <span style="animation: pulse 2s infinite 0.6s;">💉</span>
            <span style="animation: pulse 2s infinite 0.9s;">🔬</span>
            <span style="animation: pulse 2s infinite 1.2s;">🏥</span>
        </div>
        
        <style>
        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 0.7; }
            50% { transform: scale(1.2); opacity: 1; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Enhanced Hero Section với animation slide-in từ trái
st.markdown(
    """
    <div class="hero-section slide-in-left">
        <h1 class="main-title">🏥 VITA – VinBig Intelligent Treatment Assistant</h1>
        <p class="subtitle fade-in-up delay-300">Nền tảng AI hỗ trợ chẩn đoán và chăm sóc sức khỏe thông minh</p>
        <div class="medical-icons fade-in-up delay-500">
            <span class="medical-icon delay-100">🩺</span>
            <span class="medical-icon delay-200">💊</span>
            <span class="medical-icon delay-300">🏥</span>
            <span class="medical-icon delay-400">⚕️</span>
            <span class="medical-icon delay-500">💉</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# App Description Section với scroll animations
st.markdown('<div class="scroll-fade-in">', unsafe_allow_html=True)
st.markdown("## 🎯 Giới thiệu về ứng dụng")
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="scroll-slide-left">', unsafe_allow_html=True)
    st.markdown("""
    ### 🌟 **VITA** - Giải pháp y tế thông minh của tương lai

    **VITA** là nền tảng **AI y tế tiên tiến**, được phát triển bởi **VinBig AI**, 
    với sứ mệnh hỗ trợ bác sĩ trong chẩn đoán, tư vấn và cá nhân hóa chăm sóc sức khỏe.

    #### 🔬 **Hệ sinh thái AI y tế:**
    - **🎯 Intelligent Diagnosis**: AI hỗ trợ chẩn đoán đa chuyên khoa
    - **🤖 Virtual Health Assistant**: Trợ lý sức khỏe cá nhân thông minh
    - **📈 Predictive Healthcare**: Phân tích xu hướng và dự báo rủi ro
    - **🔗 Integrated Platform**: Kết nối đa dịch vụ trong một hệ thống

    #### 🎯 **Sứ mệnh:**
    Mang đến giải pháp y tế **an toàn**, **chính xác** và **hiệu quả**, 
    giúp bác sĩ đưa ra quyết định điều trị tối ưu và đồng hành cùng bệnh nhân trong hành trình chăm sóc sức khỏe.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="scroll-slide-right">', unsafe_allow_html=True)
    st.info("""
    📊 **Điểm nổi bật:**

    • Được hàng nghìn bệnh nhân và bác sĩ tin tưởng sử dụng  
    • Độ chính xác cao nhờ công nghệ AI tiên tiến  
    • Hỗ trợ 24/7, luôn đồng hành cùng người dùng  
    • Cam kết bảo mật và tuân thủ tiêu chuẩn quốc tế về y tế và dữ liệu  

    🏆 **Uy tín & Chất lượng:**  
    Được phát triển bởi **VinBig AI**, với nền tảng công nghệ hiện đại và quy trình đạt chuẩn toàn cầu.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Detailed User Guide Section với animations
st.markdown("---")
st.markdown('<div class="scroll-fade-in">', unsafe_allow_html=True)
# st.markdown("## 📚 Hướng dẫn sử dụng chi tiết")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="scroll-scale-in">', unsafe_allow_html=True)
st.markdown("""
## 🚀 **Hệ sinh thái y tế thông minh toàn diện**

**VITA** là nền tảng hỗ trợ toàn diện cho **bác sĩ** và **bệnh nhân**, tích hợp AI để nâng cao chất lượng chăm sóc sức khỏe.

### 🌟 **TÍNH NĂNG HIỆN TẠI**
*Khám phá các công cụ AI đang hoạt động trong hệ sinh thái VITA*
""")
st.markdown('</div>', unsafe_allow_html=True)

# CSS cho hover effects và card styling
st.markdown("""
<style>
.feature-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 15px;
    margin: 10px 0;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    position: relative;
    overflow: hidden;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    border: 2px solid #00f5ff;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s;
}

.feature-card:hover::before {
    left: 100%;
}

.feature-title {
    color: white;
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.feature-description {
    color: rgba(255,255,255,0.9);
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 15px;
}

.feature-details {
    background: rgba(255,255,255,0.1);
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
    opacity: 0;
    max-height: 0;
    overflow: hidden;
    transition: all 0.3s ease;
}

.feature-card:hover .feature-details {
    opacity: 1;
    max-height: 300px;
}

.feature-arrow {
    margin-left: auto;
    font-size: 24px;
    transition: transform 0.3s ease;
}

.feature-card:hover .feature-arrow {
    transform: rotate(90deg);
}

.cccd-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.diabetes-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.chatbot-card {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.future-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 20px;
    margin: 30px 0;
    text-align: center;
    color: white;
}

.future-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 15px;
}

.future-description {
    font-size: 16px;
    opacity: 0.9;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# Feature Cards với hover effects
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card cccd-card">
        <div class="feature-title">
            📄 Trích xuất CCCD thông minh
            <span class="feature-arrow">▶</span>
        </div>
        <div class="feature-description">
            AI tự động nhận dạng và trích xuất thông tin từ Căn cước công dân Việt Nam
        </div>
        <div class="feature-details">
            <strong>✨ Tính năng:</strong><br>
            • OCR chính xác 98%+<br>
            • Nhận dạng tự động các trường thông tin<br>
            • Tự động tạo ID bệnh nhân<br>
            • Xác thực tính hợp lệ<br>
            • Bảo mật thông tin cá nhân<br><br>
            <strong>🎯 Kết quả:</strong> Tiết kiệm 90% thời gian nhập liệu
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card diabetes-card">
        <div class="feature-title">
            🔬 Dự đoán tiểu đường AI
            <span class="feature-arrow">▶</span>
        </div>
        <div class="feature-description">
            Phân tích 15+ yếu tố nguy cơ để đánh giá khả năng mắc bệnh tiểu đường
        </div>
        <div class="feature-details">
            <strong>✨ Tính năng:</strong><br>
            • Thuật toán Machine Learning<br>
            • Phân tích đa chiều (tuổi, BMI, tiền sử...)<br>
            • Báo cáo chi tiết nguy cơ<br>
            • Khuyến nghị cá nhân hóa<br>
            • Theo dõi lịch sử sức khỏe<br><br>
            <strong>🎯 Độ chính xác:</strong> 93%+ tin cậy y khoa
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card chatbot-card">
        <div class="feature-title">
            🤖 Dr. HealthBot 24/7
            <span class="feature-arrow">▶</span>
        </div>
        <div class="feature-description">
            Chatbot AI tư vấn sức khỏe cá nhân hóa dựa trên hồ sơ bệnh nhân
        </div>
        <div class="feature-details">
            <strong>✨ Tính năng:</strong><br>
            • Tư vấn dựa trên hồ sơ cá nhân<br>
            • Trả lời câu hỏi y khoa<br>
            • Giải thích kết quả xét nghiệm<br>
            • Hướng dẫn chăm sóc tại nhà<br>
            • Kết nối bác sĩ khi cần thiết<br><br>
            <strong>🎯 Khả năng:</strong> Phản hồi tức thì, ngôn ngữ tự nhiên
        </div>
    </div>
    """, unsafe_allow_html=True)

# Future Development Section
st.markdown("""
<div class="future-section">
    <div class="future-title">🚀 TƯƠNG LAI - HỆ SINH THÁI TOÀN DIỆN</div>
    <div class="future-description">
        Chúng tôi đang phát triển các module chuyên khoa (tim mạch, nội tiết, thần kinh), 
        tích hợp thiết bị IoT để theo dõi sức khỏe realtime, và kết nối trực tiếp với 
        các bệnh viện - phòng khám để tạo nên hệ sinh thái y tế hoàn chỉnh.
        <br><br>
        <strong>🌟 Tầm nhìn:</strong> Trở thành nền tảng chăm sóc sức khỏe thông minh hàng đầu Việt Nam
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Initialize session state for CCCD data
if 'cccd_extracted_data' not in st.session_state:
    st.session_state.cccd_extracted_data = {}



# Initialize session state for CCCD data
if 'cccd_extracted_data' not in st.session_state:
    st.session_state.cccd_extracted_data = {}

# Patient Information Section with CCCD Upload Side by Side
st.markdown('<div class="scroll-fade-in">', unsafe_allow_html=True)
st.markdown('<h2 class="form-title">👤 Thông tin bệnh nhân</h2>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Create two main columns: CCCD Upload (left) and Patient Form (right)
cccd_col, form_col = st.columns([1, 2])

# Left Column - CCCD Upload Section
with cccd_col:
    st.markdown('<div class="scroll-slide-left">', unsafe_allow_html=True)
    
    # Enhanced CCCD Upload UI
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%); 
        padding: 25px; 
        border-radius: 20px; 
        margin: 10px 0; 
        border: 2px solid #0066cc;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.2) 50%, transparent 70%);
            animation: shimmer 3s ease-in-out infinite;
        "></div>
        <div style="position: relative; z-index: 1;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h3 style="color: #1976d2; margin-bottom: 10px; font-weight: 600;">📷 Trích xuất thông tin từ CCCD</h3>
                <p style="color: #666; font-size: 14px; margin: 0;">
                    Upload ảnh căn cước công dân để tự động điền thông tin bệnh nhân
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if CCCD_OCR_AVAILABLE:
        # Server status check (compact)
        with st.expander("🔧 Cài đặt server", expanded=False):
            if st.button("🔄 Kiểm tra kết nối", key="check_server"):
                start_ocr_server_if_needed()
        
        # CCCD Upload
        uploaded_file = st.file_uploader(
            "Chọn ảnh CCCD",
            type=['png', 'jpg', 'jpeg'],
            help="Định dạng hỗ trợ: PNG, JPG, JPEG",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Display uploaded image (compact)
            st.image(uploaded_file, caption=f"📎 {uploaded_file.name}", use_column_width=True)
            
            # Extract button
            if st.button("🤖 Trích xuất thông tin", type="primary", use_container_width=True):
                with st.spinner("🔄 Đang xử lý..."):
                    # Call OCR API
                    result = ocr_client.extract_from_uploaded_file(uploaded_file)
                    
                    if result['success']:
                        st.session_state.cccd_extracted_data = result['data']
                        st.success("✅ Trích xuất thành công!")
                        
                        # Compact display of extracted info
                        st.markdown("**📋 Thông tin đã trích xuất:**")
                        data = result['data']
                        if data.get('ho_ten'):
                            st.write(f"👤 **{data.get('ho_ten')}**")
                        if data.get('ngay_sinh'):
                            st.write(f"🎂 {data.get('ngay_sinh')}")
                        if data.get('gioi_tinh'):
                            st.write(f"⚥ {data.get('gioi_tinh')}")
                        
                        st.info("➡️ Thông tin sẽ tự động điền vào form!")
                        
                    else:
                        st.error(f"❌ {result['message']}")
                        if "server" in result['message'].lower():
                            st.code("cd Doctor_app && python cccd_ocr_server.py", language="bash")
        
    else:
        st.warning("⚠️ Tính năng OCR chưa sẵn sàng")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Right Column - Patient Information Form
with form_col:
    # Initialize session state for form success
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False

    st.markdown('<div class="scroll-scale-in">', unsafe_allow_html=True)
    with st.form("patient_info_form"):
        # Get extracted CCCD data for auto-fill
        cccd_data = st.session_state.cccd_extracted_data
        
        # Show auto-fill status
        if cccd_data:
            st.success("🤖 **Thông tin tự động điền từ CCCD** - Bạn có thể chỉnh sửa nếu cần")
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input(
                "**👤 Họ và tên**",
                value=cccd_data.get('ho_ten', ''),
                placeholder="Nhập họ và tên đầy đủ",
                help="Vui lòng nhập họ và tên đầy đủ của bệnh nhân"
            )
            
            # Auto-fill birth date from CCCD
            default_birth_date = None
            if cccd_data.get('ngay_sinh'):
                try:
                    from datetime import datetime
                    # Try different date formats
                    date_str = cccd_data.get('ngay_sinh', '')
                    for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']:
                        try:
                            default_birth_date = datetime.strptime(date_str, fmt).date()
                            break
                        except:
                            continue
                except:
                    pass
            
            birth_date = st.date_input(
                "**🎂 Ngày sinh**",
                value=default_birth_date,
                help="Chọn ngày sinh của bệnh nhân"
            )
            
            # Auto-fill address from CCCD
            default_address = cccd_data.get('noi_thuong_tru', '')
            if not default_address and cccd_data.get('que_quan'):
                default_address = cccd_data.get('que_quan', '')
            
            address = st.text_area(
                "**🏠 Địa chỉ**",
                value=default_address,
                placeholder="Nhập địa chỉ đầy đủ",
                help="Địa chỉ nơi ở hiện tại"
            )
        
        with col2:
            # Auto-fill gender from CCCD
            gender_options = ["Nam", "Nữ", "Khác"]
            default_gender_index = 0  # Default to Nam
            if cccd_data.get('gioi_tinh'):
                gender_cccd = cccd_data.get('gioi_tinh', '').lower()
                if 'nữ' in gender_cccd or 'female' in gender_cccd:
                    default_gender_index = 1
                elif 'nam' in gender_cccd or 'male' in gender_cccd:
                    default_gender_index = 0
            
            gender = st.selectbox(
                "**⚥ Giới tính**",
                options=gender_options,
                index=default_gender_index,
                help="Chọn giới tính"
            )
            
            id_number = st.text_input(
                "**🆔 CCCD/CMND**",
                value=cccd_data.get('so_cccd', ''),
                placeholder="Số căn cước công dân",
                help="Số căn cước công dân hoặc chứng minh nhân dân"
            )
            
            # Add nationality and place of origin from CCCD
            nationality = st.text_input(
                "**🏁 Quốc tịch**",
                value=cccd_data.get('quoc_tich', 'Việt Nam'),
                help="Quốc tịch từ CCCD"
            )
            
            place_origin = st.text_input(
                "**🏞️ Quê quán**",
                value=cccd_data.get('que_quan', ''),
                help="Quê quán từ CCCD"
            )
        
        # Medical Analysis Section - AI Personalization Data
        st.markdown("---")
        st.markdown("### 🧬 Thông tin phân tích AI")
        
        col3, col4 = st.columns(2)
        
        with col3:
            current_symptoms = st.text_area(
                "**🤒 Triệu chứng hiện tại**",
                placeholder="Mô tả chi tiết các triệu chứng: đau đầu, sốt, ho, khó thở, đau bụng...",
                help="Thông tin này giúp AI phân tích và đề xuất chẩn đoán ban đầu"
            )
            
            pain_level = st.selectbox(
                "**😴 Chất lượng giấc ngủ**",
                options=[
                    "Rất tốt - ngủ sâu giấc 7-8 tiếng",
                    "Tốt - ngủ đủ giấc, thỉnh thoảng thức giữa đêm",
                    "Trung bình - ngủ được nhưng không sâu giấc",
                    "Kém - thường xuyên mất ngủ, ngủ không đủ giấc",
                    "Rất kém - mất ngủ triền miên, ngủ dưới 5 tiếng"
                ],
                help="Chất lượng giấc ngủ ảnh hưởng trực tiếp đến sức khỏe tổng thể"
            )
            
            family_history = st.text_area(
                "**👨‍👩‍👧‍👦 Tiền sử gia đình**",
                placeholder="Bệnh di truyền, ung thư, tim mạch, tiểu đường trong gia đình...",
                help="Thông tin di truyền giúp AI đánh giá yếu tố nguy cơ"
            )
        
        with col4:
            lifestyle_habits = st.text_area(
                "**🏃‍♂️ Thói quen sống**",
                placeholder="Hút thuốc, uống rượu, tập thể dục, chế độ ăn, giấc ngủ...",
                help="Lối sống ảnh hưởng lớn đến sức khỏe và khả năng hồi phục"
            )
            
            work_environment = st.selectbox(
                "**🏢 Môi trường làm việc**",
                options=[
                    "Văn phòng - ít vận động",
                    "Lao động chân tay",
                    "Y tế - tiếp xúc bệnh nhân",
                    "Giáo dục",
                    "Công nghiệp - hóa chất",
                    "Nông nghiệp",
                    "Dịch vụ - tiếp xúc đông người",
                    "Công nghệ thông tin",
                    "Khác"
                ],
                help="Môi trường làm việc có thể là nguyên nhân gây bệnh"
            )
            
            stress_anxiety_level = st.selectbox(
                "**😰 Mức độ căng thẳng/lo âu**",
                options=[
                    "Rất thấp - cuộc sống bình yên",
                    "Thấp - thỉnh thoảng căng thẳng",
                    "Trung bình - căng thẳng công việc",
                    "Cao - thường xuyên lo lắng",
                    "Rất cao - áp lực liên tục"
                ],
                help="Tâm lý ảnh hưởng trực tiếp đến sức khỏe thể chất"
            )
            
            additional_info = st.text_area(
                "**💭 Thông tin thêm**",
                placeholder="Chia sẻ bất kỳ điều gì bạn muốn bác sĩ biết: cảm xúc, lo lắng, kỳ vọng, câu hỏi...",
                help="Không gian tự do để bạn chia sẻ những điều quan trọng khác mà bạn muốn bác sĩ biết",
                height=100
            )
        
        # Submit button
        submitted = st.form_submit_button(
            "💾 Lưu thông tin bệnh nhân", 
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            # Validate required fields
            if not full_name or not birth_date:
                st.error("❌ Vui lòng điền đầy đủ thông tin bắt buộc: Họ tên, Ngày sinh")
            else:
                # Create patient data
                patient_data = {
                    "patient_id": f"BN_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "personal_info": {
                        "full_name": full_name,
                        "birth_date": birth_date.strftime("%Y-%m-%d"),
                        "gender": gender,
                        "id_number": id_number,
                        "address": address,
                        "nationality": nationality,
                        "place_origin": place_origin
                    },
                    "cccd_info": {
                        "extracted_from_image": bool(cccd_data),
                        "so_cccd": cccd_data.get('so_cccd', id_number),
                        "ho_ten": cccd_data.get('ho_ten', full_name),
                        "ngay_sinh": cccd_data.get('ngay_sinh', ''),
                        "gioi_tinh": cccd_data.get('gioi_tinh', ''),
                        "quoc_tich": cccd_data.get('quoc_tich', nationality),
                        "que_quan": cccd_data.get('que_quan', place_origin),
                        "noi_thuong_tru": cccd_data.get('noi_thuong_tru', ''),
                    },
                    "medical_analysis": {
                        "current_symptoms": current_symptoms,
                        "sleep_quality": pain_level,
                        "family_history": family_history,
                        "lifestyle_habits": lifestyle_habits,
                        "work_environment": work_environment,
                        "stress_anxiety_level": stress_anxiety_level,
                        "additional_info": additional_info
                    },
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Save to JSON file - Replace old file with new patient data
                json_file_path = os.path.join(dir, "Doctor_app", "patient_data.json")
                # Create new patient data structure (replace old file completely)
                patient_file_data = {
                    "current_patient": patient_data,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Save new patient data (overwrite existing file)
                try:
                    with open(json_file_path, 'w', encoding='utf-8') as f:
                        json.dump(patient_file_data, f, ensure_ascii=False, indent=2)
                    
                    st.session_state.form_submitted = True
                    st.success(
                        f"""
                        ✅ **Thông tin bệnh nhân đã được lưu thành công!**
                        
                        **Mã bệnh nhân:** {patient_data['patient_id']}
                        
                        **Thông tin đã lưu:**
                        - Họ tên: {full_name}
                        - Ngày sinh: {birth_date.strftime("%d/%m/%Y")}
                        - Ngày tạo: {patient_data['created_at']}
                        """
                    )
                    
                    # Store patient data in session for DiabeteDoctor
                    st.session_state.current_patient = patient_data
                    
                except Exception as e:
                    st.error(f"❌ Lỗi khi lưu dữ liệu: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Information Cards using Streamlit columns với animations
st.markdown('<div class="scroll-fade-in">', unsafe_allow_html=True)
st.markdown("### 🏥 Dịch vụ của chúng tôi")
st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="scroll-slide-left">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-card">
            <div class="card-icon">🩺</div>
            <div class="card-title">Khám bệnh chuyên nghiệp</div>
            <div class="card-content">
                Đội ngũ bác sĩ giàu kinh nghiệm, sử dụng công nghệ AI hỗ trợ chẩn đoán chính xác
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="info-card">
            <div class="card-icon">🔐</div>
            <div class="card-title">Bảo mật tuyệt đối</div>
            <div class="card-content">
                Thông tin bệnh nhân được mã hóa và bảo vệ theo tiêu chuẩn y tế quốc tế
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="scroll-slide-right">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-card">
            <div class="card-icon">📝</div>
            <div class="card-title">Quản lý hồ sơ thông minh</div>
            <div class="card-content">
                Hệ thống lưu trữ và quản lý thông tin bệnh nhân an toàn, tiện lợi
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="info-card">
            <div class="card-icon">⚡</div>
            <div class="card-title">Phản hồi nhanh chóng</div>
            <div class="card-content">
                Hệ thống xử lý thông tin nhanh chóng, hỗ trợ bác sĩ đưa ra quyết định kịp thời
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Copyright and legal footer với animation
st.markdown('<div class="scroll-fade-in">', unsafe_allow_html=True)
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
            animation: footerShine 3s ease-in-out infinite;
        "></div>
        <h3 style="margin-bottom: 1rem; color: white; position: relative; z-index: 1;">🏥 VITA – VinBig Intelligent Treatment Assistant</h3>
        <p style="font-size: 1.1rem; margin-bottom: 1rem; position: relative; z-index: 1;">
            Nền tảng AI hỗ trợ chẩn đoán và chăm sóc sức khỏe thông minh
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-bottom: 1rem; position: relative; z-index: 1;">
            <span>📞 Hotline: 091-606-1368</span>
            <span>📧 Email: v.hieuhm7@vinbigdata.org</span>
            <span>🌐 Website: vinbig.ai</span>
        </div>
        <hr style="border: 1px solid rgba(255,255,255,0.3); margin: 1rem 0;">
        <div style="font-size: 0.9rem; opacity: 0.8; position: relative; z-index: 1;">
            <p>© 2025 VinBig AI Corporation. All rights reserved.</p>
            <p>Bảo mật dữ liệu • Tuân thủ GDPR • Chứng nhận ISO 27001</p>
            <p style="font-style: italic;">
                "Công nghệ AI phục vụ sức khỏe cộng đồng"
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)
