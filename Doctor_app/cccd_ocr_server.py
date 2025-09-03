"""
CCCD OCR Server
Server API để xử lý trích xuất thông tin từ ảnh CCCD
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import json
import tempfile
import os
from datetime import datetime
import traceback

# Import OCR model
try:
    from cccd_ocr_model import extract_cccd_from_uploaded_file, extract_cccd_info
except ImportError:
    print("❌ Không thể import OCR model. Đảm bảo file cccd_ocr_model.py tồn tại.")

app = Flask(__name__)
CORS(app)  # Cho phép CORS để Streamlit có thể gọi API

# Cấu hình
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max


def allowed_file(filename):
    """Kiểm tra file có được phép upload không"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint kiểm tra sức khỏe server"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "CCCD OCR Server đang hoạt động"
    })


@app.route('/extract-cccd', methods=['POST'])
def extract_cccd():
    """
    Endpoint trích xuất thông tin CCCD từ ảnh
    """
    try:
        # Kiểm tra request
        if 'image' not in request.files:
            return jsonify({
                "success": False,
                "message": "Không tìm thấy file ảnh trong request",
                "data": {}
            }), 400
        
        file = request.files['image']
        
        # Kiểm tra file
        if file.filename == '':
            return jsonify({
                "success": False,
                "message": "Không có file nào được chọn",
                "data": {}
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "message": f"Định dạng file không được hỗ trợ. Chỉ chấp nhận: {', '.join(ALLOWED_EXTENSIONS)}",
                "data": {}
            }), 400
        
        # Trích xuất thông tin
        print(f"📸 Đang xử lý file: {file.filename}")
        
        # Đọc file content
        file_content = file.read()
        
        # Gọi model OCR
        result = extract_cccd_info(file_content, is_file_path=False)
        
        print(f"✅ Kết quả xử lý: {result['success']}")
        print(result)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        error_msg = f"Lỗi server: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        
        return jsonify({
            "success": False,
            "message": error_msg,
            "data": {}
        }), 500


@app.route('/extract-cccd-base64', methods=['POST'])
def extract_cccd_base64():
    """
    Endpoint trích xuất thông tin CCCD từ ảnh base64
    """
    try:
        # Lấy dữ liệu JSON
        data = request.get_json()
        
        if not data or 'image_base64' not in data:
            return jsonify({
                "success": False,
                "message": "Thiếu dữ liệu image_base64 trong request",
                "data": {}
            }), 400
        
        # Decode base64
        try:
            image_data = base64.b64decode(data['image_base64'])
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Lỗi decode base64: {str(e)}",
                "data": {}
            }), 400
        
        # Trích xuất thông tin
        print("📸 Đang xử lý ảnh base64")
        
        result = extract_cccd_info(image_data, is_file_path=False)
        
        print(f"✅ Kết quả xử lý: {result['success']}")
        
        return jsonify(result), 200 if result['success'] else 500
            
    except Exception as e:
        error_msg = f"Lỗi server: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        
        return jsonify({
            "success": False,
            "message": error_msg,
            "data": {}
        }), 500


@app.route('/test-extract', methods=['GET'])
def test_extract():
    """
    Endpoint test trích xuất với ảnh mẫu
    """
    try:
        test_image_path = "/Users/apple/Desktop/LLM-apps/image.jpeg"
        
        if not os.path.exists(test_image_path):
            return jsonify({
                "success": False,
                "message": f"Không tìm thấy file test: {test_image_path}",
                "data": {}
            }), 404
        
        # Trích xuất với file test
        result = extract_cccd_info(test_image_path, is_file_path=True)
        
        return jsonify(result), 200 if result['success'] else 500
        
    except Exception as e:
        error_msg = f"Lỗi test: {str(e)}"
        print(f"❌ {error_msg}")
        
        return jsonify({
            "success": False,
            "message": error_msg,
            "data": {}
        }), 500


if __name__ == '__main__':
    print("🚀 Khởi động CCCD OCR Server...")
    print("=" * 50)
    print("📋 Các endpoint có sẵn:")
    print("  - GET  /health        : Kiểm tra sức khỏe server")
    print("  - POST /extract-cccd  : Trích xuất CCCD từ file upload")
    print("  - POST /extract-cccd-base64 : Trích xuất CCCD từ base64")
    print("  - GET  /test-extract  : Test với ảnh mẫu")
    print("=" * 50)
    
    # Chạy server
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True,
        threaded=True
    )
