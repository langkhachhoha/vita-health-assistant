import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import logging
from convert import convert_patient_data_to_text_segments

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# OpenAI Configuration
BASE_URL = os.getenv('BASE_URL', 'https://mkp-api.fptcloud.com')
API_KEY = os.getenv('FPT_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-oss-20b')

if not API_KEY:
    raise ValueError("API_KEY not found in environment variables")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def create_health_chatbot_system_prompt(patient_segments):
    """
    Tạo system prompt cho chatbot tư vấn sức khỏe cá nhân hóa
    """
    
    system_prompt = f"""BẠN LÀ BÁC SĨ TƯ VẤN SỨC KHỎE THÔNG MINH - Dr. HealthBot

🎯 VAI TRÒ VÀ NHIỆM VỤ:
Bạn là một trợ lý AI chuyên nghiệp trong lĩnh vực y tế, có khả năng tư vấn sức khỏe cá nhân hóa dựa trên thông tin bệnh nhân được cung cấp. Bạn có thể trả lời mọi câu hỏi về sức khỏe, y tế và các vấn đề đời sống, không chỉ giới hạn trong thông tin cá nhân.

📋 THÔNG TIN BỆNH NHÂN HIỆN TẠI:

{patient_segments.get('segment_1_personal_info', 'Chưa có thông tin cá nhân')}

{patient_segments.get('segment_2_lifestyle_health', 'Chưa có thông tin lối sống')}

{patient_segments.get('segment_3_health_metrics', 'Chưa có chỉ số sức khỏe')}

{patient_segments.get('segment_4_ai_analysis', 'Chưa có phân tích AI')}

{patient_segments.get('segment_5_doctor_recommendations', 'Chưa có khuyến nghị bác sĩ')}

🔍 NGUYÊN TẮC HOẠT ĐỘNG:

1. **TƯ VẤN CÁ NHÂN HÓA:**
   - Khi được hỏi về sức khỏe cá nhân, LUÔN tham khảo thông tin bệnh nhân đã cung cấp
   - Đưa ra lời khuyên phù hợp với tuổi, giới tính, BMI, tình trạng sức khỏe hiện tại
   - Kết hợp kết quả phân tích AI và khuyến nghị của bác sĩ đã có

2. **TƯ VẤN TỔNG QUÁT:**
   - Với các câu hỏi y tế chung, trả lời dựa trên kiến thức y học hiện đại
   - Không bắt buộc phải sử dụng thông tin cá nhân nếu câu hỏi mang tính tổng quát
   - Cung cấp thông tin chính xác, khoa học và dễ hiểu

3. **AN TOÀN VÀ CHUYÊN NGHIỆP:**
   - KHÔNG tự chẩn đoán hoặc kê đơn thuốc
   - Luôn khuyến nghị gặp bác sĩ chuyên khoa khi cần thiết
   - Đưa ra cảnh báo phù hợp về các triệu chứng nghiêm trọng

🎨 PHONG CÁCH GIAO TIẾP:
- Thân thiện, ấm áp như một bác sĩ gia đình
- Sử dụng tiếng Việt tự nhiên, dễ hiểu
- Giải thích thuật ngữ y khoa khi cần thiết
- Động viên và tích cực
- Sử dụng emoji phù hợp để tạo không khí thân thiện

📝 CẤU TRÚC PHẢN HỒI:
1. **Lời chào/Thể hiện sự quan tâm**
2. **Phân tích câu hỏi và liên kết với thông tin cá nhân (nếu có)**
3. **Đưa ra lời khuyên cụ thể và thực tế**
4. **Cảnh báo an toàn (nếu cần)**
5. **Động viên và đề xuất bước tiếp theo**

⚠️ GIỚI HẠN VÀ LƯU Ý:
- Không thay thế việc khám bác sĩ trực tiếp
- Với triệu chứng cấp tính hoặc nghiêm trọng, ưu tiên khuyến nghị đến cơ sở y tế
- Thông tin chỉ mang tính tham khảo và giáo dục
- Tôn trọng quyền riêng tư và bảo mật thông tin bệnh nhân

🔄 XỬ LÝ CÁC TÌNH HUỐNG:
- **Câu hỏi về tình trạng cá nhân:** Tham khảo đầy đủ 5 đoạn thông tin
- **Câu hỏi y tế tổng quát:** Trả lời dựa trên kiến thức chuyên môn
- **Câu hỏi ngoài y tế:** Trả lời lịch sự và chuyển hướng về sức khỏe nếu phù hợp
- **Thông tin không rõ ràng:** Yêu cầu làm rõ một cách nhẹ nhàng

Hãy bắt đầu cuộc trò chuyện bằng việc chào hỏi thân thiện và sẵn sàng hỗ trợ bệnh nhân về mọi vấn đề sức khỏe!"""
    print(system_prompt)
    return system_prompt

import os
dir = os.getcwd()

def load_patient_data():
    """Load dữ liệu bệnh nhân từ file JSON"""
    try:
        json_file_path = os.path.join(dir, 'Doctor_app', 'patient_data.json')
        if os.path.exists(json_file_path):
            patient_segments = convert_patient_data_to_text_segments(json_file_path)
            if 'error' in patient_segments:
                logger.error(f"Error loading patient data: {patient_segments['error']}")
                return None
            return patient_segments
        else:
            logger.warning("Patient data file not found")
            return None
    except Exception as e:
        logger.error(f"Error loading patient data: {e}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model": MODEL_NAME
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for health consultation"""
    try:
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({"error": "Missing messages in request"}), 400
        
        messages = data['messages']
        stream = data.get('stream', False)
        
        # Load patient data and create system prompt
        patient_segments = load_patient_data()
        
        if patient_segments:
            system_prompt = create_health_chatbot_system_prompt(patient_segments)
        else:
            system_prompt = """Bạn là Dr. HealthBot - trợ lý tư vấn sức khỏe AI. 
            Hiện chưa có thông tin bệnh nhân cụ thể. 
            Hãy tư vấn dựa trên kiến thức y học chung và khuyến nghị bệnh nhân cung cấp thông tin cá nhân để được tư vấn tốt hơn."""
        
        # Prepare messages for API
        api_messages = [{"role": "system", "content": system_prompt}]
        api_messages.extend(messages)
        
        if stream:
            def generate():
                try:
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=api_messages,
                        temperature=0.7,
                        top_p=0.9,
                        max_tokens=2048,
                        stream=True
                    )
                    
                    for chunk in response:
                        if chunk.choices and chunk.choices[0].delta and hasattr(chunk.choices[0].delta, 'content'):
                            if chunk.choices[0].delta.content:
                                yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
                    
                    yield f"data: {json.dumps({'content': '[DONE]'})}\n\n"
                    
                except Exception as e:
                    logger.error(f"Error in streaming response: {e}")
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
            return Response(generate(), mimetype='text/plain')
        
        else:
            # Non-streaming response
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=api_messages,
                temperature=0.7,
                top_p=0.9,
                max_tokens=1024
            )
            
            return jsonify({
                "content": response.choices[0].message.content,
                "usage": response.usage.dict() if hasattr(response, 'usage') else None
            })
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/patient-info', methods=['GET'])
def get_patient_info():
    """Get current patient information"""
    try:
        patient_segments = load_patient_data()
        if patient_segments:
            return jsonify({
                "status": "success",
                "data": patient_segments
            })
        else:
            return jsonify({
                "status": "no_data",
                "message": "No patient data available"
            })
    except Exception as e:
        logger.error(f"Error getting patient info: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Dr. HealthBot Server...")
    logger.info(f"Model: {MODEL_NAME}")
    logger.info(f"Base URL: {BASE_URL}")
    
    port = int(os.getenv('CHATBOT_SERVER_PORT', 8502))
    host = os.getenv('CHATBOT_SERVER_HOST', 'localhost')
    
    app.run(host=host, port=port, debug=True)
