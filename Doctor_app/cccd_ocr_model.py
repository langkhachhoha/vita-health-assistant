"""
CCCD OCR Model
Mô-đun trích xuất thông tin từ ảnh căn cước công dân sử dụng FPT AI
"""

import base64
import json
import tempfile
import os
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file in parent directory
dir = os.getcwd()
load_dotenv(dotenv_path=os.path.join(dir, "Doctor_app", ".env"))

# Cấu hình API
BASE_URL = "https://api.together.xyz/v1"
FPT_API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL_NAME = 'meta-llama/Llama-4-Scout-17B-16E-Instruct'

# Khởi tạo client
client = OpenAI(
    api_key=FPT_API_KEY,
    base_url=BASE_URL
)


class CCCDInfo(BaseModel):
    """Mô hình dữ liệu thông tin CCCD"""
    id_number: str = Field(description="Citizen Identity Number")
    full_name: str = Field(description="Full name")
    date_of_birth: str = Field(description="Date of birth")
    sex: str = Field(description="Sex")
    nationality: str = Field(description="Nationality")
    place_of_origin: str = Field(description="Place of origin")
    place_of_residence: str = Field(description="Place of residence")


def encode_image_from_bytes(image_bytes: bytes) -> str:
    """Mã hóa ảnh từ bytes thành base64"""
    return base64.b64encode(image_bytes).decode("utf-8")


def encode_image_from_path(image_path: str) -> str:
    """Mã hóa ảnh từ đường dẫn thành base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_cccd_info(image_data, is_file_path: bool = False) -> Dict[str, Any]:
    """
    Trích xuất thông tin từ ảnh CCCD
    
    Args:
        image_data: Đường dẫn file hoặc bytes của ảnh
        is_file_path: True nếu image_data là đường dẫn file, False nếu là bytes
        
    Returns:
        Dict chứa thông tin trích xuất được
    """
    try:
        # Mã hóa ảnh
        if is_file_path:
            base64_image = encode_image_from_path(image_data)
        else:
            base64_image = encode_image_from_bytes(image_data)
        
        # Gọi API để trích xuất thông tin
        extract = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": (
                                "Trích xuất chính xác tất cả thông tin từ ảnh căn cước công dân Việt Nam. "
                                "Trả về thông tin bằng tiếng Việt có dấu đầy đủ. "
                                "Nếu không tìm thấy thông tin nào, để trống."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                },
            ],
            model=MODEL_NAME,
            response_format={
                "type": "json_object",
                "schema": CCCDInfo.model_json_schema(),
            },
        )
        
        # Phân tích kết quả
        output = json.loads(extract.choices[0].message.content)
        


        values = list(output.values())

        # Chuẩn hóa dữ liệu
        normalized_data = {
            "so_cccd": values[0] if values[0] is not None else "",
            "ho_ten": values[1] if values[1] is not None else "",
            "ngay_sinh": values[2] if values[2] is not None else "",
            "gioi_tinh": values[3] if values[3] is not None else "",
            "quoc_tich": values[4] if values[4] is not None else "",
            "que_quan": values[5] if values[5] is not None else "",
            "noi_thuong_tru": values[6] if values[6] is not None else "",
        }
        
        return {
            "success": True,
            "data": normalized_data,
            "message": "Trích xuất thông tin thành công"
        }
        
    except Exception as e:
        return {
            "success": False,
            "data": {},
            "message": f"Lỗi khi trích xuất thông tin: {str(e)}"
        }


def extract_cccd_from_uploaded_file(uploaded_file) -> Dict[str, Any]:
    """
    Trích xuất thông tin CCCD từ file upload của Streamlit
    
    Args:
        uploaded_file: File upload object từ Streamlit
        
    Returns:
        Dict chứa thông tin trích xuất được
    """
    try:
        # Đọc bytes từ uploaded file
        image_bytes = uploaded_file.read()
        
        # Trích xuất thông tin
        result = extract_cccd_info(image_bytes, is_file_path=False)
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "data": {},
            "message": f"Lỗi khi xử lý file upload: {str(e)}"
        }


def save_temp_image(uploaded_file) -> Optional[str]:
    """
    Lưu file upload vào thư mục tạm thời
    
    Args:
        uploaded_file: File upload object từ Streamlit
        
    Returns:
        Đường dẫn file tạm hoặc None nếu lỗi
    """
    try:
        # Tạo file tạm
        temp_dir = tempfile.gettempdir()
        temp_filename = f"cccd_{uploaded_file.name}"
        temp_path = os.path.join(temp_dir, temp_filename)
        
        # Lưu file
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
            
        return temp_path
        
    except Exception as e:
        print(f"Lỗi khi lưu file tạm: {e}")
        return None


def test_extraction():
    """Test function để kiểm tra trích xuất thông tin"""
    test_image_path = os.path.join(dir, "image.jpeg")

    if os.path.exists(test_image_path):
        result = extract_cccd_info(test_image_path, is_file_path=True)
        
        print("=" * 60)
        print("KẾT QUẢ TRÍCH XUẤT THÔNG TIN CCCD")
        print("=" * 60)
        
        if result["success"]:
            print("✅ Trích xuất thành công!")
            print("\n📋 Thông tin chi tiết:")
            for key, value in result["data"].items():
                print(f"  {key}: {value}")
        else:
            print("❌ Trích xuất thất bại!")
            print(f"Lỗi: {result['message']}")
            
        print("=" * 60)
        
        return result
    else:
        print(f"❌ Không tìm thấy file test: {test_image_path}")
        return None


if __name__ == "__main__":
    # Chạy test
    test_extraction()
