import json
import requests
import os
from pathlib import Path
import time
from urllib.parse import urlparse
import shutil

def download_image(url, save_path):
    """
    Tải ảnh từ URL và lưu vào file
    Returns True nếu thành công, False nếu thất bại
    """
    try:
        # Kiểm tra nếu URL rỗng hoặc không hợp lệ
        if not url or url.strip() == "https://www.vinmec.com/static/":
            return False
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Kiểm tra content type có phải là ảnh không
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            return False
            
        # Lưu file
        with open(save_path, 'wb') as f:
            f.write(response.content)
            
        print(f"✅ Tải thành công: {save_path}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi tải {url}: {str(e)}")
        return False

def copy_previous_image(doctor_id, avatar_folder):
    """
    Copy ảnh từ bác sĩ trước đó nếu không tải được ảnh hiện tại
    """
    if doctor_id == 0:
        return False
        
    # Tìm ảnh từ các bác sĩ trước đó
    for prev_id in range(doctor_id - 1, -1, -1):
        prev_image_path = avatar_folder / f"Doctor_{prev_id}.jpg"
        if prev_image_path.exists():
            current_image_path = avatar_folder / f"Doctor_{doctor_id}.jpg"
            try:
                shutil.copy2(prev_image_path, current_image_path)
                print(f"📋 Copy ảnh từ Doctor_{prev_id} -> Doctor_{doctor_id}")
                return True
            except Exception as e:
                print(f"❌ Lỗi copy ảnh: {str(e)}")
                continue
    
    return False

def get_file_extension(url):
    """
    Lấy phần mở rộng file từ URL
    """
    try:
        parsed = urlparse(url)
        path = parsed.path
        extension = Path(path).suffix
        if extension.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            return extension.lower()
        else:
            return '.jpg'  # Default
    except:
        return '.jpg'

def main():
    # Đường dẫn tới các file
    current_dir = Path(__file__).parent
    database_path = current_dir / "vinmec_doctors_database.json"
    avatar_folder = current_dir.parent / "Doctor_avatar"
    
    # Tạo folder nếu chưa tồn tại
    avatar_folder.mkdir(exist_ok=True)
    
    # Đọc database
    try:
        with open(database_path, 'r', encoding='utf-8') as f:
            doctors_data = json.load(f)
    except Exception as e:
        print(f"❌ Không thể đọc file database: {str(e)}")
        return
    
    print(f"🔍 Tìm thấy {len(doctors_data)} bác sĩ trong database")
    
    # Tải ảnh cho từng bác sĩ
    for doctor_id, doctor in enumerate(doctors_data):
        print(f"\n📋 Xử lý Doctor_{doctor_id}: {doctor.get('ten_bac_si', 'N/A')}")
        
        # Lấy URL ảnh
        avatar_url = doctor.get('anh_dai_dien', '')
        
        # Tạo tên file với extension phù hợp
        extension = get_file_extension(avatar_url)
        image_path = avatar_folder / f"Doctor_{doctor_id}{extension}"
        
        # Thử tải ảnh
        success = download_image(avatar_url, image_path)
        
        # Nếu không tải được, copy ảnh từ bác sĩ trước đó
        if not success:
            print(f"⚠️ Không thể tải ảnh cho Doctor_{doctor_id}")
            
            # Thử copy ảnh từ bác sĩ trước
            if not copy_previous_image(doctor_id, avatar_folder):
                print(f"❌ Không thể copy ảnh cho Doctor_{doctor_id}")
        
        # Nghỉ một chút để tránh spam server
        time.sleep(0.5)
    
    print(f"\n✅ Hoàn thành! Kiểm tra folder: {avatar_folder}")

if __name__ == "__main__":
    main()
