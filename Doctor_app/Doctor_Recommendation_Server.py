import os
import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Ngrok tunnel URL - cập nhật URL này từ Colab
NGROK_TUNNEL_URL = "https://8632e6940133.ngrok-free.app"  # Cập nhật URL từ ảnh

@app.route('/recommend', methods=['POST'])
def recommend_doctor():
    """
    Endpoint để nhận yêu cầu gợi ý bác sĩ từ người dùng
    """
#     # result = {'ID': 'doc_120', 'Name': 'Bác sĩ 2', 'Reason': 'Bác sĩ 2 có chuyên môn sâu rộng về các bệnh lý Nhãn khoa, bao gồm điều trị các bệnh về mắt như glôcôm, và thực hiện các phẫu thuật, thủ thuật liên quan đến mắt. Điều này phù hợp với chẩn đoán sơ bộ về các khả năng bệnh lý tiềm ẩn như viêm kết mạc, viêm giác mạc, glaucôm, và các bệnh lý khác liên quan đến mắt.', 'Services': ['Khám, tư vấn và điều trị các bệnh lý Nhãn khoa', 'Điều trị tật khúc xạ, tư vấn chuyên sâu về kiểm soát cận thị, bệnh lý thủy tinh thể, Glocom', 'Thực hiện các thủ thuật, tiểu phẫu, trung phẫu, laser và phẫu thuật thay thủy tinh thể bằng phương pháp Phaco'], 'Specialty': ['Giám đốc Chuyên môn, Bệnh viện chuyên khoa Mắt Alina', 'Giám đốc Chuyên môn, Trung tâm Mắt Vinmec - Alina, Bệnh viện ĐKQT Vinmec Times City'], 'Think': 'Đầu vào là một bản tóm tắt triệu chứng và thông tin bệnh nhân. Bệnh nhân có triệu chứng đau mắt, nhưng không có thông tin cụ thể về nguyên nhân, thời gian khởi phát, hoặc các triệu chứng kèm theo.\n\nQuá trình phân tích:\n1. Triệu chứng đau mắt có thể do nhiều nguyên nhân gây ra, bao gồm các vấn đề về kết mạc, giác mạc, nông nghiệp hoặc thậm chí các bệnh lý hệ thống.\n2. Do thiếu thông tin chi tiết, cần phải thu thập thêm dữ liệu về tiền sử bệnh, các triệu chứng đi kèm và tình trạng sức khỏe tổng thể của bệnh nhân.\n\nKết quả:\n- Các khả năng bệnh lý tiềm ẩn bao gồm viêm kết mạc, viêm giác mạc, glaucôm, hoặc các bệnh lý khác liên quan đến mắt.\n- Cần thực hiện các dịch vụ và xét nghiệm như khám mắt chuyên sâu, xét nghiệm hỗ trợ để xác định nguyên nhân gây đau mắt.\nCân nhắc dựa trên chuyên môn và dịch vụ của các bác sĩ để chọn ra người phù hợp nhất cho bệnh nhân bị đau mắt.'}
#     return jsonify({
#         'ID': 'doc_10',
#         'Think': """
# Bác sĩ 2 có chuyên môn sâu rộng về các bệnh lý Nhãn khoa, bao gồm điều trị các bệnh về mắt như glôcôm, và thực hiện các phẫu thuật, thủ thuật liên quan đến mắt. Điều này phù hợp với chẩn đoán sơ bộ về các khả năng bệnh lý tiềm ẩn như viêm kết mạc, viêm giác mạc, glaucôm, và các bệnh lý khác liên quan đến mắt.', 'Services': ['Khám, tư vấn và điều trị các bệnh lý Nhãn khoa', 'Điều trị tật khúc xạ, tư vấn chuyên sâu về kiểm soát cận thị, bệnh lý thủy tinh thể, Glocom', 'Thực hiện các thủ thuật, tiểu phẫu, trung phẫu, laser và phẫu thuật thay thủy tinh thể bằng phương pháp Phaco'], 'Specialty': ['Giám đốc Chuyên môn, Bệnh viện chuyên khoa Mắt Alina', 'Giám đốc Chuyên môn, Trung tâm Mắt Vinmec - Alina, Bệnh viện ĐKQT Vinmec Times City'], 'Think': 'Đầu vào là một bản tóm tắt triệu chứng và thông tin bệnh nhân. Bệnh nhân có triệu chứng đau mắt, nhưng không có thông tin cụ thể về nguyên nhân, thời gian khởi phát, hoặc các triệu chứng kèm theo.\n\nQuá trình phân tích:\n1. Triệu chứng đau mắt có thể do nhiều nguyên nhân gây ra, bao gồm các vấn đề về kết mạc, giác mạc, nông nghiệp hoặc thậm chí các bệnh lý hệ thống.\n2. Do thiếu thông tin chi tiết, cần phải thu thập thêm dữ liệu về tiền sử bệnh, các triệu chứng đi kèm và tình trạng sức khỏe tổng thể của bệnh nhân.\n\nKết quả:\n- Các khả năng bệnh lý tiềm ẩn bao gồm viêm kết mạc, viêm giác mạc, glaucôm, hoặc các bệnh lý khác liên quan đến mắt.\n- Cần thực hiện các dịch vụ và xét nghiệm như khám mắt chuyên sâu, xét nghiệm hỗ trợ để xác định nguyên nhân gây đau mắt.\nCân nhắc dựa trên chuyên môn và dịch vụ của các bác sĩ để chọn ra người phù hợp nhất cho bệnh nhân bị đau mắt.
# """,
#         'status': 'success',
#         'timestamp': datetime.now().isoformat()
#     })
    try:
        # Lấy thông tin từ request
        user_message = request.json.get('message', '')
        
        if not user_message:
            return jsonify({
                'error': 'Message is required',
                'status': 'error'
            }), 400
        
        logger.info(f"Received recommendation request: {user_message}")
        
        # Tạo payload để gửi đến server ngrok
        payload = {
            "message": {
                "content": user_message
            }
        }
        
        # Gửi request đến ngrok tunnel
        try:
            response = requests.post(
                f"{NGROK_TUNNEL_URL}/chat",
                json=payload,
                headers={
                    'Content-Type': 'application/json',
                    'ngrok-skip-browser-warning': 'true'  # Bỏ qua cảnh báo browser của ngrok
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Received response from ngrok server: {result}")
                
                # Kiểm tra format response
                if 'ID' in result and 'Think' in result:
                    return jsonify({
                        'ID': result['ID'],
                        'Think': result['Think'],
                        'status': 'success',
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    # Nếu response không đúng format, trả về response gốc
                    return jsonify({
                        'ID': result.get('ID', 'Unknown'),
                        'Think': result.get('Think', str(result)),
                        'status': 'success',
                        'timestamp': datetime.now().isoformat()
                    })
            else:
                logger.error(f"Error from ngrok server: {response.status_code} - {response.text}")
                return jsonify({
                    'error': f'Server error: {response.status_code}',
                    'status': 'error',
                    'details': response.text
                }), 500
                
        except requests.exceptions.Timeout:
            logger.error("Request timeout to ngrok server")
            return jsonify({
                'error': 'Request timeout. Please try again.',
                'status': 'timeout'
            }), 504
            
        except requests.exceptions.ConnectionError:
            logger.error("Connection error to ngrok server")
            return jsonify({
                'error': 'Unable to connect to recommendation server.',
                'status': 'connection_error'
            }), 503
            
        except Exception as e:
            logger.error(f"Error connecting to ngrok server: {str(e)}")
            return jsonify({
                'error': f'Connection error: {str(e)}',
                'status': 'error'
            }), 500
        
    except Exception as e:
        logger.error(f"Error in recommend_doctor endpoint: {str(e)}")
        return jsonify({
            'error': f'Server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Doctor Recommendation Server',
        'timestamp': datetime.now().isoformat(),
        'ngrok_url': NGROK_TUNNEL_URL
    })

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Doctor Recommendation Server is running',
        'endpoints': {
            '/recommend': 'POST - Get doctor recommendation',
            '/health': 'GET - Health check',
        },
        'ngrok_tunnel': NGROK_TUNNEL_URL,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🏥 Starting Doctor Recommendation Server...")
    print(f"📡 Ngrok Tunnel URL: {NGROK_TUNNEL_URL}")
    print("📍 Server endpoints:")
    print("   - POST /recommend - Get doctor recommendation")
    print("   - GET /health - Health check")
    print("   - GET / - Home page")
    
    app.run(host='0.0.0.0', port=5002, debug=True)
