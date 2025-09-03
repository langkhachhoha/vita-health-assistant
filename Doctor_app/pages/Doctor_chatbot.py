import streamlit as st
import requests
import json
import base64
import os
from datetime import datetime
import time

dir = os.getcwd()
st.set_page_config(
    page_title="VITA Health Assistant - AI Medical Consultant",
    page_icon="👨🏼‍⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to encode image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Get doctor images
doctor_image_path = os.path.join(dir, "image", "Doctor.png")
doctor_base64 = get_base64_image(doctor_image_path)

doctor_1_image_path = os.path.join(dir, "image", "Doctor_1.png")
doctor_1_base64 = get_base64_image(doctor_1_image_path)

# Get VinBig logo for header
vinbig_logo_path = os.path.join(dir, "image", "logo_vinbig.png")
vinbig_logo_base64 = get_base64_image(vinbig_logo_path)

# Enhanced Medical Styling with Modern Healthcare Design
if doctor_base64:
    background_style = f"background-image: url('data:image/png;base64,{doctor_base64}');"
else:
    background_style = "background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #334155 50%, #475569 75%, #64748b 100%);"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700;800;900&family=Poppins:wght@200;300;400;500;600;700;800;900&family=JetBrains+Mono:wght@200;300;400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    /* Hide Streamlit UI Elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    [data-testid="stToolbar"] {{display: none;}}
    [data-testid="stDecoration"] {{display: none;}}
    [data-testid="stStatusWidget"] {{display: none;}}
    [data-testid="manage-app-button"] {{display: none;}}
    /* Global Variables */
    :root {{
        --primary-color: #0ea5e9;
        --primary-dark: #0284c7;
        --primary-light: #38bdf8;
        --accent-color: #06d6a0;
        --accent-dark: #059669;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --success-color: #10b981;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-muted: #94a3b8;
        --bg-glass: rgba(255, 255, 255, 0.95);
        --bg-card: rgba(255, 255, 255, 0.98);
        --shadow-soft: 0 10px 40px rgba(0, 0, 0, 0.08);
        --shadow-medium: 0 20px 60px rgba(0, 0, 0, 0.12);
        --shadow-strong: 0 30px 80px rgba(0, 0, 0, 0.15);
        --border-radius: 24px;
        --border-radius-lg: 32px;
        --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .stApp {{
        {background_style}
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: 'Inter', 'Space Grotesk', sans-serif;
        min-height: 100vh;
        position: relative;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, 
            rgba(14, 165, 233, 0.03) 0%,
            rgba(6, 214, 160, 0.05) 25%,
            rgba(16, 185, 129, 0.03) 50%,
            rgba(59, 130, 246, 0.05) 75%,
            rgba(14, 165, 233, 0.03) 100%);
        backdrop-filter: blur(20px);
        z-index: -1;
    }}
    
    /* Enhanced Header Styling */
    .medical-hero {{
        text-align: center;
        padding: 3rem 1rem 2rem;
        background: var(--bg-glass);
        border-radius: var(--border-radius-lg);
        margin: 1rem auto 2rem;
        max-width: 1200px;
        box-shadow: var(--shadow-medium);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(30px);
        position: relative;
        overflow: hidden;
    }}
    
    .medical-hero::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, 
            transparent 30%, 
            rgba(14, 165, 233, 0.05) 50%, 
            transparent 70%);
        animation: heroShine 8s ease-in-out infinite;
        pointer-events: none;
    }}
    
    @keyframes heroShine {{
        0%, 100% {{ transform: translateX(-100%) translateY(-100%) rotate(45deg); }}
        50% {{ transform: translateX(100%) translateY(100%) rotate(45deg); }}
    }}
    
    .medical-title {{
        font-family: 'Space Grotesk', 'Inter', sans-serif;
        font-size: clamp(2.5rem, 6vw, 4rem);
        font-weight: 800;
        background: linear-gradient(135deg, 
            var(--primary-color) 0%, 
            var(--accent-color) 40%,
            var(--primary-dark) 80%,
            var(--accent-dark) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        text-shadow: none;
        position: relative;
        z-index: 2;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }}
    
    .medical-subtitle {{
        font-family: 'Inter', sans-serif;
        font-size: clamp(1.1rem, 3vw, 1.4rem);
        font-weight: 600;
        color: var(--text-secondary);
        margin: 1.5rem auto;
        max-width: 800px;
        line-height: 1.6;
        position: relative;
        z-index: 2;
    }}
    
    .hero-tagline {{
        font-family: 'Inter', sans-serif;
        font-size: clamp(1rem, 2.5vw, 1.2rem);
        font-weight: 500;
        color: var(--text-muted);
        margin-top: 1rem;
        font-style: italic;
        position: relative;
        z-index: 2;
    }}
    
    .hero-features {{
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
        flex-wrap: wrap;
        position: relative;
        z-index: 2;
    }}
    
    .feature-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.7rem 1.2rem;
        background: var(--bg-card);
        border: 1px solid rgba(14, 165, 233, 0.1);
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--text-primary);
        box-shadow: var(--shadow-soft);
        transition: var(--transition);
    }}
    
    .feature-badge:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
        border-color: var(--primary-color);
        background: rgba(14, 165, 233, 0.05);
    }}
    
    /* Chat Container Styling */
    .chat-container {{
        max-width: 1000px;
        margin: 0 auto;
        padding: 0 1rem;
    }}
    
    /* Enhanced Chat Message Styling */
    .chat-message {{
        padding: 2rem 2.5rem;
        margin: 2rem 0;
        border-radius: var(--border-radius);
        max-width: 85%;
        word-wrap: break-word;
        font-size: 1.05rem;
        line-height: 1.7;
        box-shadow: var(--shadow-medium);
        position: relative;
        backdrop-filter: blur(30px);
        transition: var(--transition);
        border: 1px solid rgba(255,255,255,0.1);
        font-family: 'Inter', sans-serif;
    }}
    
    .chat-message:hover {{
        transform: translateY(-3px);
        box-shadow: var(--shadow-strong);
    }}
    
    /* User Messages - Premium Design */
    .user-message {{
        background: linear-gradient(135deg, 
            var(--bg-card) 0%, 
            rgba(14, 165, 233, 0.02) 100%);
        border-left: 4px solid var(--primary-color);
        color: var(--text-primary);
        margin-left: auto;
        border-bottom-right-radius: 8px;
        animation: slideInRight 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .user-message::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    }}
    
    /* Bot Messages - Professional Medical Design */
    .bot-message {{
        background: linear-gradient(135deg, 
            var(--bg-card) 0%, 
            rgba(6, 214, 160, 0.02) 100%);
        border-left: 4px solid var(--accent-color);
        color: var(--text-primary);
        margin-right: auto;
        border-bottom-left-radius: 8px;
        animation: slideInLeft 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .bot-message::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--accent-color) 0%, var(--accent-dark) 100%);
    }}
    
    /* Enhanced Message Header */
    .message-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    }}
    
    .message-avatar {{
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        color: white;
        font-weight: 700;
        box-shadow: var(--shadow-soft);
        border: 2px solid rgba(255, 255, 255, 0.2);
        font-family: 'Inter', sans-serif;
    }}
    
    .user-avatar {{
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    }}
    
    .bot-avatar {{
        background: linear-gradient(135deg, var(--accent-color) 0%, var(--accent-dark) 100%);
    }}
    
    .message-info {{
        display: flex;
        flex-direction: column;
        margin-left: 1rem;
    }}
    
    .message-name {{
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 2px;
    }}
    
    .message-role {{
        color: var(--text-muted);
        font-size: 0.85rem;
        font-weight: 500;
    }}
    
    .message-time {{
        color: var(--text-muted);
        font-size: 0.85rem;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }}
    
    .message-content {{
        color: var(--text-primary);
        font-size: 1.05rem;
        line-height: 1.7;
        font-weight: 400;
    }}
    
    /* Enhanced Typing Indicator */
    .typing-indicator {{
        background: linear-gradient(135deg, 
            var(--bg-card) 0%, 
            rgba(6, 214, 160, 0.02) 100%);
        border-left: 4px solid var(--accent-color);
        padding: 2rem 2.5rem;
        border-radius: var(--border-radius);
        border-bottom-left-radius: 8px;
        margin: 2rem 0;
        max-width: 85%;
        animation: typingPulse 2s infinite ease-in-out;
        box-shadow: var(--shadow-medium);
        position: relative;
        backdrop-filter: blur(30px);
    }}
    
    @keyframes slideInRight {{
        from {{
            opacity: 0;
            transform: translateX(60px) scale(0.95);
        }}
        to {{
            opacity: 1;
            transform: translateX(0) scale(1);
        }}
    }}
    
    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-60px) scale(0.95);
        }}
        to {{
            opacity: 1;
            transform: translateX(0) scale(1);
        }}
    }}
    
    @keyframes typingPulse {{
        0%, 100% {{
            transform: scale(1);
            box-shadow: var(--shadow-medium);
        }}
        50% {{
            transform: scale(1.01);
            box-shadow: var(--shadow-strong);
        }}
    }}
    
    @keyframes doctorThinking {{
        0%, 100% {{ transform: scale(1) rotate(0deg); }}
        50% {{ transform: scale(1.05) rotate(2deg); }}
    }}
    
    @keyframes typingDot1 {{
        0%, 80%, 100% {{ transform: scale(0.8); opacity: 0.4; }}
        40% {{ transform: scale(1.2); opacity: 1; }}
    }}
    
    @keyframes typingDot2 {{
        0%, 80%, 100% {{ transform: scale(0.8); opacity: 0.4; }}
        50% {{ transform: scale(1.2); opacity: 1; }}
    }}
    
    @keyframes typingDot3 {{
        0%, 80%, 100% {{ transform: scale(0.8); opacity: 0.4; }}
        60% {{ transform: scale(1.2); opacity: 1; }}
    }}
    
    /* Enhanced Input Styling */
    .stTextInput > div > div > input {{
        border-radius: var(--border-radius);
        border: 2px solid rgba(14, 165, 233, 0.1);
        padding: 18px 24px;
        font-size: 1.05rem;
        font-weight: 400;
        transition: var(--transition);
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        box-shadow: var(--shadow-soft);
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: var(--primary-color);
        box-shadow: 0 0 0 4px rgba(14, 165, 233, 0.1), var(--shadow-medium);
        transform: translateY(-1px);
        background: rgba(255, 255, 255, 1);
        outline: none;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: var(--text-muted);
        font-weight: 400;
    }}
    
    /* Enhanced Button Styling */
    .stButton > button {{
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 18px 36px;
        font-size: 1.05rem;
        font-weight: 600;
        transition: var(--transition);
        box-shadow: var(--shadow-soft);
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::before {{
        content: '💬';
        margin-right: 8px;
        font-size: 1.1rem;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--accent-color) 100%);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* Patient Info Card Styling */
    .patient-info-card {{
        background: var(--bg-card);
        border-radius: var(--border-radius);
        padding: 1.8rem;
        margin: 1rem 0;
        border-left: 4px solid var(--primary-color);
        box-shadow: var(--shadow-soft);
        backdrop-filter: blur(20px);
        transition: var(--transition);
    }}
    
    .patient-info-card:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
    }}
    
    .patient-info-card h4 {{
        color: var(--primary-color);
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 1.1rem;
    }}
    
    .patient-info-card p {{
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }}
    
    /* Status Indicators */
    .status-indicator {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.8rem 1.5rem;
        border-radius: 20px;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 1rem 0;
        backdrop-filter: blur(20px);
        transition: var(--transition);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    .status-online {{
        background: rgba(16, 185, 129, 0.1);
        color: var(--success-color);
        border-color: rgba(16, 185, 129, 0.2);
    }}
    
    .status-offline {{
        background: rgba(239, 68, 68, 0.1);
        color: var(--danger-color);
        border-color: rgba(239, 68, 68, 0.2);
    }}
    
    /* Sidebar Styling */
    .css-1d391kg {{
        background: var(--bg-glass);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}
    
    /* Footer Styling */
    .medical-footer {{
        text-align: center;
        padding: 2rem 1rem;
        margin-top: 3rem;
        background: var(--bg-glass);
        border-radius: var(--border-radius);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        color: var(--text-secondary);
        line-height: 1.6;
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .medical-hero {{
            padding: 2rem 1rem 1.5rem;
            margin: 0.5rem auto 1rem;
        }}
        
        .hero-features {{
            gap: 1rem;
        }}
        
        .feature-badge {{
            padding: 0.5rem 1rem;
            font-size: 0.85rem;
        }}
        
        .chat-message {{
            padding: 1.5rem 1.8rem;
            max-width: 95%;
        }}
        
        .message-avatar {{
            width: 38px;
            height: 38px;
            font-size: 1rem;
        }}
    }}
    
    /* Dark theme support */
    @media (prefers-color-scheme: dark) {{
        :root {{
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --bg-glass: rgba(15, 23, 42, 0.95);
            --bg-card: rgba(30, 41, 59, 0.98);
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Load patient data
@st.cache_data
def load_patient_data():
    """Load patient data from JSON file"""
    try:
        json_file_path = os.path.join(dir, "Doctor_app", "patient_data.json")

        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading patient data: {e}")
    return None

def check_server_status():
    """Check if chatbot server is running"""
    try:
        response = requests.get("http://localhost:8502/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def send_chat_message(messages):
    """Send message to chatbot server and get streaming response"""
    try:
        response = requests.post(
            "http://localhost:8502/chat",
            json={
                "messages": messages,
                "stream": True
            },
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            return response
        else:
            st.error(f"Server error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("🔌 Không thể kết nối đến server chatbot. Vui lòng khởi động server trước.")
        return None
    except Exception as e:
        st.error(f"❌ Lỗi khi gửi tin nhắn: {e}")
        return None

# Page Header with Enhanced Design
st.markdown('''
<div class="medical-hero">
    <div class="medical-title">👨🏼‍⚕️ VITA Health Assistant</div>
    <div class="medical-subtitle">
        Trí tuệ nhân tạo tiên tiến cho chăm sóc sức khỏe cá nhân hóa
    </div>
    <div class="hero-tagline">
        "Hiểu bạn từng nhịp tim - Chăm sóc tận tâm mọi lúc"
    </div>
    <div class="hero-features">
        <div class="feature-badge">
            <span>🧠</span>
            <span>AI Thông minh</span>
        </div>
        <div class="feature-badge">
            <span>⚡</span>
            <span>Phản hồi tức thì</span>
        </div>
        <div class="feature-badge">
            <span>🎯</span>
            <span>Tư vấn cá nhân</span>
        </div>
        <div class="feature-badge">
            <span>🔒</span>
            <span>Bảo mật tuyệt đối</span>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

# Check server status
server_online = check_server_status()

if server_online:
    st.markdown('<div class="status-indicator status-online">🟢 Server đang hoạt động</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-indicator status-offline">🔴 Server không khả dụng</div>', unsafe_allow_html=True)
    st.warning("⚠️ Vui lòng khởi động chatbot server để sử dụng tính năng này.")
    st.code("python Doctor_chatbot_server.py", language="bash")

# Load patient data
patient_data = load_patient_data()

# Sidebar with patient information
with st.sidebar:
    st.markdown("### 👤 Thông tin bệnh nhân")
    
    if patient_data and 'current_patient' in patient_data:
        current_patient = patient_data['current_patient']
        personal_info = current_patient.get('personal_info', {})
        
        st.success("✅ Đã có dữ liệu bệnh nhân")
        
        # Basic info
        st.markdown(f"""
        <div class="patient-info-card">
            <h4>📋 Thông tin cơ bản</h4>
            <p><strong>Họ tên:</strong> {personal_info.get('full_name', 'N/A')}</p>
            <p><strong>Ngày sinh:</strong> {personal_info.get('birth_date', 'N/A')}</p>
            <p><strong>Giới tính:</strong> {personal_info.get('gender', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Health analysis if available
        diabetes_analysis = current_patient.get('diabetes_analysis', {})
        if diabetes_analysis:
            ai_diagnosis = diabetes_analysis.get('ai_diagnosis', {})
            st.markdown(f"""
            <div class="patient-info-card">
                <h4>🔬 Kết quả phân tích</h4>
                <p><strong>Nguy cơ tiểu đường:</strong> {ai_diagnosis.get('risk_level', 'N/A')}</p>
                <p><strong>Xác suất:</strong> {ai_diagnosis.get('probability', 0)*100:.1f}%</p>
                <p><strong>Độ tin cậy:</strong> {ai_diagnosis.get('confidence', 0):.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Chưa có thông tin bệnh nhân")
        st.info("Vui lòng đăng ký thông tin ở trang chính trước khi sử dụng chatbot.")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### ⚡ Hành động nhanh")
    if st.button("🔄 Làm mới cuộc trò chuyện"):
        st.session_state.chat_messages = []
        st.rerun()
    
    if st.button("🏠 Về trang chủ"):
        st.switch_page("Homepage.py")

# Initialize chat messages
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
    
    # Welcome message with enhanced content
    welcome_msg = """👋 Xin chào! Tôi là **Dr. VITA** - Trợ lý AI chăm sóc sức khỏe thông minh của bạn.

🎯 **Tôi có thể hỗ trợ bạn:**

� **Phân tích & Tư vấn**
- Giải thích kết quả phân tích y tế chi tiết
- Đánh giá nguy cơ sức khỏe dựa trên dữ liệu cá nhân
- Tư vấn cá nhân hóa theo tình trạng hiện tại

💡 **Hướng dẫn & Lời khuyên**
- Chế độ dinh dưỡng phù hợp với tình trạng sức khỏe
- Kế hoạch tập luyện an toàn và hiệu quả
- Lối sống lành mạnh và phòng ngừa bệnh tật

🏥 **Định hướng Y tế**
- Hướng dẫn khi nào cần gặp bác sĩ chuyên khoa
- Chuẩn bị thông tin trước khi khám bệnh
- Theo dõi và quản lý sức khỏe dài hạn

🔒 **Cam kết bảo mật**: Mọi thông tin của bạn được bảo vệ tuyệt đối và chỉ phục vụ mục đích tư vấn.

Hãy chia sẻ với tôi câu hỏi hoặc mối quan tâm về sức khỏe của bạn! 😊✨"""
    
    st.session_state.chat_messages.append({
        "role": "assistant",
        "content": welcome_msg
    })

# Chat container with enhanced layout
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages with enhanced modern styling
for message in st.session_state.chat_messages:
    timestamp = datetime.now().strftime("%H:%M")
    
    if message["role"] == "user":
        # Get user info
        user_name = "Bạn"
        user_initial = "👤"
        if patient_data and 'current_patient' in patient_data:
            personal_info = patient_data['current_patient'].get('personal_info', {})
            full_name = personal_info.get('full_name', '')
            if full_name:
                user_name = full_name.split()[-1] if full_name.split() else "Bạn"
                user_initial = full_name[0].upper() if full_name else "👤"
        
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-header">
                <div style="display: flex; align-items: center;">
                    <div class="message-avatar user-avatar">{user_initial}</div>
                    <div class="message-info">
                        <div class="message-name" style="color: #0ea5e9;">{user_name}</div>
                        <div class="message-role">Bệnh nhân</div>
                    </div>
                </div>
                <div class="message-time">{timestamp}</div>
            </div>
            <div class="message-content">
                {message["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <div class="message-header">
                <div style="display: flex; align-items: center;">
                    <div class="message-avatar bot-avatar">🩺</div>
                    <div class="message-info">
                        <div class="message-name" style="color: #06d6a0;">Dr. VITA</div>
                        <div class="message-role">AI Health Assistant</div>
                    </div>
                </div>
                <div class="message-time">{timestamp}</div>
            </div>
            <div class="message-content">
                {message["content"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
if server_online:
    # Use a form to handle input properly
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "💬 Hỏi Dr. VITA về sức khỏe...",
            placeholder="Ví dụ: Kết quả phân tích của tôi có ổn không? Tôi nên lưu ý điều gì?",
            key="user_input_form"
        )
        
        col1, col2 = st.columns([3, 1])
        with col2:
            send_button = st.form_submit_button("🤙 Gửi tin nhắn", type="primary")
    
    if send_button and user_input.strip():
        # Add user message
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Prepare messages for API (exclude welcome message for API)
        api_messages = []
        for msg in st.session_state.chat_messages[1:]:  # Skip welcome message
            api_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Show enhanced typing indicator with modern design
        typing_placeholder = st.empty()
        typing_placeholder.markdown("""
        <div class="typing-indicator">
            <div class="message-header">
                <div style="display: flex; align-items: center;">
                    <div class="message-avatar bot-avatar" style="animation: doctorThinking 1.5s infinite;">🩺</div>
                    <div class="message-info">
                        <div class="message-name" style="color: #06d6a0;">Dr. VITA</div>
                        <div class="message-role">AI Health Assistant</div>
                    </div>
                </div>
            </div>
            <div style="display: flex; align-items: center; color: #64748b; font-size: 1rem;">
                <span style="margin-right: 12px;">Đang phân tích và tư vấn</span>
                <div style="display: flex; gap: 6px;">
                    <div style="width: 10px; height: 10px; border-radius: 50%; background: #06d6a0; animation: typingDot1 1.4s infinite;"></div>
                    <div style="width: 10px; height: 10px; border-radius: 50%; background: #06d6a0; animation: typingDot2 1.4s infinite;"></div>
                    <div style="width: 10px; height: 10px; border-radius: 50%; background: #06d6a0; animation: typingDot3 1.4s infinite;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get response from server
        response = send_chat_message(api_messages)
        
        if response:
            # Stream response
            full_response = ""
            response_placeholder = st.empty()
            
            try:
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = json.loads(line[6:])
                            if 'content' in data:
                                if data['content'] == '[DONE]':
                                    break
                                full_response += data['content']
                                response_placeholder.markdown(f"""
                                <div class="chat-message bot-message">
                                    <div class="message-header">
                                        <div style="display: flex; align-items: center;">
                                            <div class="message-avatar bot-avatar">�</div>
                                            <div class="message-info">
                                                <div class="message-name" style="color: #06d6a0;">Dr. VITA</div>
                                                <div class="message-role">AI Health Assistant</div>
                                            </div>
                                        </div>
                                        <div class="message-time">{datetime.now().strftime("%H:%M")}</div>
                                    </div>
                                    <div class="message-content">{full_response}<span style="animation: blink 1s infinite;">▊</span></div>
                                </div>
                                <style>
                                @keyframes blink {{
                                    0%, 50% {{ opacity: 1; }}
                                    51%, 100% {{ opacity: 0; }}
                                }}
                                </style>
                                """, unsafe_allow_html=True)
                
                # Remove typing indicator and show final response
                typing_placeholder.empty()
                response_placeholder.markdown(f"""
                <div class="chat-message bot-message">
                    <div class="message-header">
                        <div style="display: flex; align-items: center;">
                            <div class="message-avatar bot-avatar">🩺</div>
                            <div class="message-info">
                                <div class="message-name" style="color: #06d6a0;">Dr. VITA</div>
                                <div class="message-role">AI Health Assistant</div>
                            </div>
                        </div>
                        <div class="message-time">{datetime.now().strftime("%H:%M")}</div>
                    </div>
                    <div class="message-content">{full_response}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Add to chat history
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": full_response
                })
                
            except Exception as e:
                typing_placeholder.empty()
                st.error(f"❌ Lỗi khi nhận phản hồi: {e}")
        else:
            typing_placeholder.empty()
        
        # Rerun to refresh the chat
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 1rem; margin-top: 3rem; background: rgba(255, 255, 255, 0.95); border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); color: #64748b; line-height: 1.6;">
    <div style="margin-bottom: 1.5rem;">
        <h3 style="color: #0ea5e9; margin-bottom: 1rem; font-size: 1.3rem; font-weight: 700;">
            ⚠️ Lưu ý quan trọng về sử dụng dịch vụ
        </h3>
        <p style="margin-bottom: 1rem; font-size: 1.05rem; line-height: 1.6; color: #1e293b;">
            <strong>Dr. VITA</strong> là trợ lý AI tư vấn sức khỏe chỉ mang tính <strong>tham khảo và giáo dục</strong>. 
            Thông tin được cung cấp không thay thế cho việc khám, chẩn đoán và điều trị của bác sĩ chuyên khoa.
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin: 1.5rem 0; flex-wrap: wrap;">
            <div style="background: rgba(239, 68, 68, 0.1); padding: 1rem 1.5rem; border-radius: 16px; border-left: 4px solid #ef4444;">
                <strong>🚨 Trường hợp khẩn cấp:</strong><br>
                Vui lòng gọi 115 hoặc đến cơ sở y tế gần nhất
            </div>
            <div style="background: rgba(245, 158, 11, 0.1); padding: 1rem 1.5rem; border-radius: 16px; border-left: 4px solid #f59e0b;">
                <strong>⚡ Tình trạng nghiêm trọng:</strong><br>
                Tham khảo ý kiến bác sĩ chuyên khoa ngay lập tức
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
