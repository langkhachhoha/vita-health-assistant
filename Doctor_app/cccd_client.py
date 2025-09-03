"""
CCCD OCR Client
Client để gọi CCCD OCR Server từ Streamlit
"""

import os
import requests
import json
import streamlit as st
from typing import Dict, Any, Optional
import base64
import io

dir = os.getcwd()


class CCCDOCRClient:
    """Client để gọi CCCD OCR Server"""
    
    def __init__(self, server_url: str = "http://127.0.0.1:5001"):
        self.server_url = server_url
        self.health_endpoint = f"{server_url}/health"
        self.extract_endpoint = f"{server_url}/extract-cccd"
        self.extract_base64_endpoint = f"{server_url}/extract-cccd-base64"
    
    def check_server_health(self) -> bool:
        """Kiểm tra server có hoạt động không"""
        try:
            response = requests.get(self.health_endpoint, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def extract_from_uploaded_file(self, uploaded_file) -> Dict[str, Any]:
        """
        Trích xuất thông tin CCCD từ file upload của Streamlit
        
        Args:
            uploaded_file: File upload object từ Streamlit
            
        Returns:
            Dict chứa thông tin trích xuất được
        """
        try:
            # Kiểm tra server
            if not self.check_server_health():
                return {
                    "success": False,
                    "message": "CCCD OCR Server không khả dụng. Vui lòng khởi động server.",
                    "data": {}
                }
            
            # Chuẩn bị file để upload
            files = {
                'image': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }
            
            # Gọi API
            response = requests.post(
                self.extract_endpoint,
                files=files,
                timeout=30
            )
            
            # Xử lý response
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json() if response.text else {}
                return {
                    "success": False,
                    "message": error_data.get("message", f"Lỗi server: {response.status_code}"),
                    "data": {}
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "Timeout khi gọi OCR server. Vui lòng thử lại.",
                "data": {}
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "Không thể kết nối đến OCR server. Vui lòng kiểm tra server có đang chạy.",
                "data": {}
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi không xác định: {str(e)}",
                "data": {}
            }
    
    def extract_from_base64(self, image_base64: str) -> Dict[str, Any]:
        """
        Trích xuất thông tin CCCD từ ảnh base64
        
        Args:
            image_base64: Ảnh được encode base64
            
        Returns:
            Dict chứa thông tin trích xuất được
        """
        try:
            # Kiểm tra server
            if not self.check_server_health():
                return {
                    "success": False,
                    "message": "CCCD OCR Server không khả dụng. Vui lòng khởi động server.",
                    "data": {}
                }
            
            # Chuẩn bị data
            data = {
                "image_base64": image_base64
            }
            
            # Gọi API
            response = requests.post(
                self.extract_base64_endpoint,
                json=data,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            # Xử lý response
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json() if response.text else {}
                return {
                    "success": False,
                    "message": error_data.get("message", f"Lỗi server: {response.status_code}"),
                    "data": {}
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "message": "Timeout khi gọi OCR server. Vui lòng thử lại.",
                "data": {}
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "message": "Không thể kết nối đến OCR server. Vui lòng kiểm tra server có đang chạy.",
                "data": {}
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi không xác định: {str(e)}",
                "data": {}
            }


def start_ocr_server_if_needed():
    """Khởi động OCR server nếu chưa chạy"""
    client = CCCDOCRClient()
    
    if not client.check_server_health():
        st.warning("🔄 CCCD OCR Server chưa khởi động. Vui lòng chạy server trước:")
        st.code("""
# Trong terminal mới:
cd /Users/apple/Desktop/LLM-apps/Doctor_app
python cccd_ocr_server.py
        """)
        return False
    else:
        st.success("✅ CCCD OCR Server đang hoạt động")
        return True


def display_extracted_info(extracted_data: Dict[str, Any]):
    """Hiển thị thông tin đã trích xuất"""
    if not extracted_data:
        return
    
    st.markdown("### 📋 Thông tin đã trích xuất:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**👤 Thông tin cá nhân:**")
        st.write(f"• **Họ tên:** {extracted_data.get('ho_ten', 'N/A')}")
        st.write(f"• **CCCD:** {extracted_data.get('so_cccd', 'N/A')}")
        st.write(f"• **Ngày sinh:** {extracted_data.get('ngay_sinh', 'N/A')}")
        st.write(f"• **Giới tính:** {extracted_data.get('gioi_tinh', 'N/A')}")
    
    with col2:
        st.markdown("**🏠 Thông tin địa chỉ:**")
        st.write(f"• **Quốc tịch:** {extracted_data.get('quoc_tich', 'N/A')}")
        st.write(f"• **Quê quán:** {extracted_data.get('que_quan', 'N/A')}")
        st.write(f"• **Nơi thường trú:** {extracted_data.get('noi_thuong_tru', 'N/A')}")


# Tạo instance global
ocr_client = CCCDOCRClient()
