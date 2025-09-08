import streamlit as st
import requests
import json
import os
import re
import base64
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="VITA - Doctor Recommendation",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get directory path
dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_base64_image(image_path):
    """Convert image to base64 string for embedding in CSS"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        print(f"Image not found: {image_path}")
        return None

def load_doctor_database():
    """Load doctor database from JSON file"""
    try:
        db_path = os.path.join(dir, "Doctor_vinmec", "vinmec_doctors_database.json")
        with open(db_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ Không thể tải database bác sĩ: {str(e)}")
        return []

def get_doctor_by_id(doctor_id, database):
    """Get doctor information by ID (doc_xxx format)"""
    try:
        # Extract number from doc_xxx format
        if doctor_id.startswith('doc_'):
            index = int(doctor_id.split('_')[1])  # Convert to 0-based index
            if 0 <= index < len(database):
                return database[index]
    except (ValueError, IndexError):
        pass
    return None

def get_doctor_image_base64(doctor_id, dir):
    """Get base64 encoded image for a doctor by ID"""
    try:
        doc_index = int(doctor_id.split('_')[1])
        # Try .jpg first
        image_path = os.path.join(dir, "Doctor_avatar", f"Doctor_{doc_index}.jpg")
        image_base64 = get_base64_image(image_path)
        if image_base64:
            return image_base64
        
        # Try .png if .jpg doesn't exist
        image_path = os.path.join(dir, "Doctor_avatar", f"Doctor_{doc_index}.png")
        return get_base64_image(image_path)
    except:
        return None

def create_related_doctors_grid(another_doctors, main_doctor_id, doctor_database, dir):
    """Create HTML grid for related doctors (excluding main doctor)"""
    if not another_doctors or len(another_doctors) < 2:
        return ""
    
    # Filter out the main doctor from the list
    related_doctors = [doc_id for doc_id in another_doctors if doc_id != main_doctor_id][:4]
    
    if not related_doctors:
        return ""
    
    grid_html = """
    <div class="related-doctors-section">
        <div class="related-doctors-title">👨‍⚕️ Các bác sĩ liên quan khác</div>
        <div class="doctors-grid">
    """
    
    for doc_id in related_doctors:
        doctor_info = get_doctor_by_id(doc_id, doctor_database)
        if doctor_info:
            # Get doctor image
            doctor_image_base64 = get_doctor_image_base64(doc_id, dir)
            image_html = ""
            if doctor_image_base64:
                image_html = f'<img src="data:image/jpeg;base64,{doctor_image_base64}" class="doctor-mini-image" alt="Doctor">'
            
            # Get doctor info - escape HTML special characters
            name = doctor_info.get('ten_bac_si', 'Không xác định').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            specialty_list = doctor_info.get('chuyen_mon', [])
            specialty = ', '.join(specialty_list)
            if len(specialty) > 50:
                specialty = specialty[:50] + '...'
            specialty = specialty.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            
            workplace = doctor_info.get('noi_lam_viec', '')
            if len(workplace) > 60:
                workplace = workplace[:60] + '...'
            workplace = workplace.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
            
            grid_html += f"""
            <div class="doctor-mini-card">
                {image_html}
                <div class="doctor-info-content">
                    <div class="doctor-mini-name">{name}</div>
                    <div class="doctor-mini-specialty">{specialty}</div>
                    <div class="doctor-mini-workplace">{workplace}</div>
                </div>
            </div>
            """
    
    grid_html += """
        </div>
    </div>
    """
    return grid_html

def clean_html_text(text):
    """Remove HTML tags and clean up text"""
    if not text:
        return "Không có thông tin"
    
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Replace HTML entities
    clean = clean.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    # Clean up extra whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    return clean if clean else "Không có thông tin"

def check_server_status():
    """Check if doctor recommendation server is running"""
    try:
        response = requests.get("http://localhost:5002/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def send_recommendation_request(symptoms):
    """Send symptoms to recommendation server and get doctor suggestions"""
    try:
        response = requests.post(
            "http://localhost:5002/recommend",
            json={"message": symptoms},
            timeout=90
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Server error: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Yêu cầu quá thời gian chờ. Vui lòng thử lại.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("🔌 Không thể kết nối với server. Vui lòng kiểm tra server có đang chạy không.")
        return None
    except Exception as e:
        st.error(f"❌ Lỗi: {str(e)}")
        return None

# Get Doctor_7 image for background
doctor_7_image_path = os.path.join(dir, "image", "Doctor_7.png")
doctor_7_base64 = get_base64_image(doctor_7_image_path)

# Get Doctor_1 image for header
# doctor_1_image_path = os.path.join(dir, "Doctor_image", "Doctor_1.png")
# doctor_1_base64 = get_base64_image(doctor_1_image_path)

# Simple, clean CSS with Doctor_7 background
if doctor_7_base64:
    background_style = f"background-image: url('data:image/png;base64,{doctor_7_base64}'); background-size: cover; background-position: center; background-attachment: fixed;"
else:
    background_style = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"

st.markdown(f"""
<style>
    .stApp {{
        {background_style}
    }}
        /* Hide Streamlit UI Elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    [data-testid="stToolbar"] {{display: none;}}
    [data-testid="stDecoration"] {{display: none;}}
    [data-testid="stStatusWidget"] {{display: none;}}
    [data-testid="manage-app-button"] {{display: none;}}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(248, 250, 252, 0.85);
        z-index: -1;
    }}
    
    .main .block-container {{
        max-width: 900px !important;
        padding: 2rem !important;
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15) !important;
        margin: 2rem auto !important;
    }}
    
    
    .hero-title {{
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        letter-spacing: -0.02em;
        line-height: 1.1;
        position: relative;
    }}
    
    .hero-title::before {{
        content: '';
        position: absolute;
        top: -5px;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        height: 3px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
        border-radius: 2px;
        opacity: 0.7;
    }}
    
    .hero-subtitle {{
        font-size: 1.3rem;
        font-weight: 500;
        color: #4a5568;
        text-align: center;
        margin-bottom: 3rem;
        line-height: 1.6;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        padding: 1.2rem 2rem;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        position: relative;
    }}
    
    .hero-subtitle::before {{
        content: '✨';
        position: absolute;
        top: -8px;
        right: 20px;
        font-size: 1.5rem;
        animation: float 3s ease-in-out infinite;
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    .hero-section {{
        position: relative;
        padding: 2rem 0 3rem;
        text-align: center;
        overflow: hidden;
    }}
    
    .doctor-image {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        margin: 0 auto 2rem;
        display: block;
        animation: doctorFloat 4s ease-in-out infinite;
        position: relative;
        z-index: 10;
    }}
    
    .doctor-image::before {{
        content: '';
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
        z-index: -1;
        animation: rotate 3s linear infinite;
    }}
    
    @keyframes doctorFloat {{
        0%, 100% {{ transform: translateY(0px) scale(1); }}
        50% {{ transform: translateY(-8px) scale(1.05); }}
    }}
    
    @keyframes rotate {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    .status-online {{
        background: rgba(209, 250, 229, 0.9);
        color: #065f46;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #a7f3d0;
        backdrop-filter: blur(5px);
    }}
    
    .status-offline {{
        background: rgba(254, 226, 226, 0.9);
        color: #991b1b;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        border: 1px solid #fca5a5;
        backdrop-filter: blur(5px);
    }}
    
    .stButton > button {{
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        backdrop-filter: blur(5px) !important;
    }}
    
    .stButton > button:hover {{
        background: #2563eb !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }}
    
    .doctor-card {{
        background: rgba(59, 130, 246, 0.9);
        color: white;
        padding: 2rem;
        border-radius: 12px 12px 0 0;
        text-align: center;
        margin: 2rem 0 0 0;
        backdrop-filter: blur(10px);
        position: relative;
    }}
    
    .doctor-result-image {{
        width: 250px;
        height: auto;
        max-height: 200px;
        border-radius: 12px;
        object-fit: contain;
        border: 3px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        margin: 0 auto 1.5rem;
        display: block;
        animation: slideInScale 0.8s ease-out;
        background: rgba(255, 255, 255, 0.1);
    }}
    
    @keyframes slideInScale {{
        0% {{ 
            opacity: 0; 
            transform: translateY(20px) scale(0.9); 
        }}
        100% {{ 
            opacity: 1; 
            transform: translateY(0) scale(1); 
        }}
    }}
    
    .doctor-name {{
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}
    
    .doctor-specialty {{
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }}
    
    .doctor-info {{
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid #e5e7eb;
        border-top: none;
        border-radius: 0 0 12px 12px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }}
    
    /* Custom divider styling */
    hr {{
        border: none !important;
        height: 3px !important;
        background: linear-gradient(90deg, transparent, #fbbf24, #f59e0b, #d97706, #fbbf24, transparent) !important;
        border-radius: 2px !important;
        margin: 2rem 0 !important;
        animation: shimmer 2s ease-in-out infinite !important;
        box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3) !important;
    }}
    
    @keyframes shimmer {{
        0%, 100% {{ opacity: 0.7; }}
        50% {{ opacity: 1; }}
    }}
    
    /* Related doctors grid styling */
    .related-doctors-section {{
        margin: 2rem 0;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(229, 231, 235, 0.5);
    }}
    
    .related-doctors-title {{
        font-size: 1.4rem;
        font-weight: 700;
        color: #1f2937;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }}
    
    .doctors-grid {{
        display: flex;
        flex-direction: column;
        gap: 1rem;
        max-width: 100%;
    }}
    
    .doctor-mini-card {{
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 8px;
        padding: 1rem;
        display: flex;
        align-items: center;
        text-align: left;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
        position: relative;
        overflow: hidden;
    }}
    
    .doctor-mini-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.4);
    }}
    
    .doctor-mini-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }}
    
    .doctor-mini-card:hover::before {{
        left: 100%;
    }}
    
    .doctor-mini-image {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid rgba(59, 130, 246, 0.3);
        margin-right: 1rem;
        flex-shrink: 0;
        transition: all 0.3s ease;
        position: relative;
        z-index: 1;
    }}
    
    .doctor-mini-card:hover .doctor-mini-image {{
        border-color: rgba(59, 130, 246, 0.6);
        transform: scale(1.05);
    }}
    
    .doctor-info-content {{
        flex: 1;
        position: relative;
        z-index: 1;
    }}
    
    .doctor-mini-name {{
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }}
    
    .doctor-mini-specialty {{
        font-size: 0.9rem;
        color: #3b82f6;
        font-weight: 500;
        margin-bottom: 0.3rem;
    }}
    
    .doctor-mini-workplace {{
        font-size: 0.8rem;
        color: #6b7280;
        line-height: 1.3;
    }}
    
    /* Responsive design for mobile */
    @media (max-width: 768px) {{
        .main .block-container {{
            max-width: 95% !important;
            padding: 1rem !important;
            margin: 1rem auto !important;
        }}
        
        .doctors-grid {{
            gap: 0.8rem;
        }}
        
        .doctor-mini-card {{
            padding: 0.8rem;
            flex-direction: column;
            text-align: center;
        }}
        
        .doctor-mini-image {{
            width: 60px;
            height: 60px;
            margin-right: 0;
            margin-bottom: 0.5rem;
        }}
        
        .doctor-mini-name {{
            font-size: 0.9rem;
        }}
        
        .doctor-mini-specialty {{
            font-size: 0.75rem;
        }}
        
        .doctor-mini-workplace {{
            font-size: 0.7rem;
        }}
        
        .related-doctors-title {{
            font-size: 1.2rem;
        }}
    }}
    
    @media (max-width: 480px) {{
        .doctor-mini-card {{
            padding: 0.6rem;
        }}
        
        .doctor-mini-image {{
            width: 50px;
            height: 50px;
        }}
        
        .doctor-mini-name {{
            font-size: 0.85rem;
        }}
        
        .doctor-mini-specialty {{
            font-size: 0.7rem;
        }}
        
        .doctor-mini-workplace {{
            font-size: 0.65rem;
        }}
    }}
    
    /* Footer divider - special styling */
    .footer-divider {{
        border: none;
        height: 4px;
        background: linear-gradient(90deg, 
            rgba(251, 191, 36, 0) 0%, 
            rgba(251, 191, 36, 0.5) 20%, 
            #fbbf24 50%, 
            rgba(251, 191, 36, 0.5) 80%, 
            rgba(251, 191, 36, 0) 100%);
        border-radius: 2px;
        margin: 3rem 0 2rem 0;
        box-shadow: 0 3px 12px rgba(251, 191, 36, 0.4);
        animation: glow 3s ease-in-out infinite;
    }}
    
    @keyframes glow {{
        0%, 100% {{ 
            box-shadow: 0 3px 12px rgba(251, 191, 36, 0.4);
            transform: scaleX(1);
        }}
        50% {{ 
            box-shadow: 0 4px 16px rgba(251, 191, 36, 0.6);
            transform: scaleX(1.02);
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recommendation_history' not in st.session_state:
    st.session_state.recommendation_history = []

# Load doctor database
doctor_database = load_doctor_database()

# Page Header
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🩺 VITA Doctor Finder</div>
    <div class="hero-subtitle">
        Tìm kiếm bác sĩ chuyên khoa phù hợp với triệu chứng của bạn
    </div>
</div>
""", unsafe_allow_html=True)

# Check server status
server_online = check_server_status()

# Server status indicator
if server_online:
    st.markdown('<div class="status-online">🟢 Server đang hoạt động - Sẵn sàng tư vấn</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-offline">🔴 Server không khả dụng</div>', unsafe_allow_html=True)
    st.error("⚠️ **Server đang offline!** Vui lòng khởi động Doctor_Recommendation_Server.py trước khi sử dụng.")

# Search form
if server_online:
    with st.form(key="symptom_form"):
        st.markdown("### 🔍 Mô tả triệu chứng của bạn")
        
        user_symptoms = st.text_input(
            "Nhập triệu chứng:",
            placeholder="Ví dụ: đau đầu liên tục, sốt cao, ho khan kéo dài...",
            label_visibility="collapsed"
        )
        
        submitted = st.form_submit_button("🔍 Tìm bác sĩ phù hợp")
        
        if submitted:
            if not user_symptoms.strip():
                st.warning("⚠️ Vui lòng mô tả triệu chứng của bạn.")
            else:
                with st.spinner("🔍 Đang tìm kiếm bác sĩ phù hợp..."):
                    result = send_recommendation_request(user_symptoms.strip())
                
                if result and result.get('status') == 'success':
                    doctor_id = result.get('ID', '')
                    think_result = result.get('Think', '')
                    another_doctors = result.get('another_doctor', [])
                    
                    # Get doctor information
                    doctor_info = get_doctor_by_id(doctor_id, doctor_database)
                    
                    if doctor_info:
                        # Display doctor card with image
                        doctor_image_html = ""
                        
                        doctor_1_image_path = os.path.join(dir, "Doctor_avatar", f"Doctor_{int(doctor_id.split('_')[1])}.jpg")
                        doctor_1_base64 = get_base64_image(doctor_1_image_path)
                        if not doctor_1_base64:
                            doctor_1_image_path = os.path.join(dir, "Doctor_avatar", f"Doctor_{int(doctor_id.split('_')[1])}.png")
                            doctor_1_base64 = get_base64_image(doctor_1_image_path)
                        if doctor_1_base64:
                            doctor_image_html = f'<img src="data:image/png;base64,{doctor_1_base64}" class="doctor-result-image" alt="Doctor">'
                        
                        st.markdown(f'''
                        <div class="doctor-card">
                            {doctor_image_html}
                            <div class="doctor-name">{doctor_info.get('ten_bac_si', 'Không xác định')}</div>
                            <div class="doctor-specialty">{', '.join(doctor_info.get('chuyen_mon', []))}</div>
                            <div>{doctor_info.get('noi_lam_viec', '')}</div>
                        </div>
                        <div class="doctor-info">
                        ''', unsafe_allow_html=True)
                        
                        # Doctor introduction
                        gioi_thieu = doctor_info.get('gioi_thieu', '')
                        if gioi_thieu and gioi_thieu.strip():
                            st.markdown("**📋 Giới thiệu:**")
                            st.write(gioi_thieu)
                            st.markdown("---")
                        
                        # Education
                        dao_tao = doctor_info.get('dao_tao', [])
                        if dao_tao:
                            st.markdown("**🎓 Đào tạo:**")
                            for item in dao_tao:
                                if item.strip():
                                    st.write(f"• {item}")
                            st.markdown("---")
                        
                        # Experience
                        kinh_nghiem = doctor_info.get('kinh_nghiem_lam_viec', [])
                        if kinh_nghiem:
                            st.markdown("**💼 Kinh nghiệm:**")
                            for item in kinh_nghiem:
                                if item.strip():
                                    st.write(f"• {item}")
                            st.markdown("---")
                        
                        # Services
                        services = doctor_info.get('dich_vu', [])
                        if services:
                            st.markdown("**🏥 Dịch vụ:**")
                            for item in services:
                                if item.strip():
                                    st.write(f"• {item}")
                            st.markdown("---")
                        
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Display related doctors grid
                        if another_doctors and len(another_doctors) > 1:
                            st.markdown("---")
                            st.markdown("### 👨‍⚕️ Các bác sĩ liên quan khác")
                            
                            # Filter out the main doctor from the list
                            related_doctors = [doc_id for doc_id in another_doctors if doc_id != doctor_id][:4]
                            
                            for doc_id in related_doctors:
                                doctor_info = get_doctor_by_id(doc_id, doctor_database)
                                if doctor_info:
                                    col1, col2 = st.columns([1, 3])
                                    
                                    with col1:
                                        # Try to display doctor image
                                        try:
                                            doc_index = int(doc_id.split('_')[1])
                                            img_path = os.path.join(dir, "Doctor_avatar", f"Doctor_{doc_index}.jpg")
                                            if os.path.exists(img_path):
                                                st.image(img_path, width=80)
                                            else:
                                                img_path = os.path.join(dir, "Doctor_avatar", f"Doctor_{doc_index}.png")
                                                if os.path.exists(img_path):
                                                    st.image(img_path, width=80)
                                                else:
                                                    st.write("🩺")
                                        except:
                                            st.write("🩺")
                                    
                                    with col2:
                                        st.markdown(f"**{doctor_info.get('ten_bac_si', 'Không xác định')}**")
                                        specialty = ', '.join(doctor_info.get('chuyen_mon', []))
                                        if len(specialty) > 1500:
                                            specialty = specialty[:1500] + '...'
                                        st.markdown(f"*{specialty}*")
                                        workplace = doctor_info.get('noi_lam_viec', '')
                                        if len(workplace) > 6000:
                                            workplace = workplace[:6000] + '...'
                                        st.markdown(f"📍 {workplace}")
                                    
                                    st.markdown("---")
                        
                        # Timestamp
                        st.info(f"⏰ {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}")
                        st.success("✅ Đã tìm thấy bác sĩ phù hợp!")
                        
                    else:
                        st.error(f"❌ Không tìm thấy thông tin bác sĩ với ID: {doctor_id}")
                
                elif result:
                    st.error(f"❌ Lỗi: {result.get('error', 'Không thể xử lý yêu cầu')}")
                else:
                    st.error("❌ Không nhận được phản hồi từ server")

# Footer
st.markdown('<hr class="footer-divider">', unsafe_allow_html=True)
st.markdown("### 🏥 VITA Health Assistant")
st.markdown("Hệ thống tư vấn y tế thông minh - Tìm kiếm bác sĩ chuyên khoa phù hợp")
st.markdown("_Powered by VinBig AI Technology_")
