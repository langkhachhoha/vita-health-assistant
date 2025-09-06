import requests
from bs4 import BeautifulSoup
import json
import re

def crawl_multiple_doctors():
    """
    Script crawl nhiều bác sĩ Vinmec từ danh sách URLs
    """
    
    print("🚀 BẮT ĐẦU CRAWL NHIỀU BÁC SĨ VINMEC")
    print("=" * 60)
    
    # Load danh sách URLs từ file đã thu thập
    try:
        with open('doctor_urls_list.json', 'r', encoding='utf-8') as f:
            urls_data = json.load(f)
        doctor_urls = urls_data.get('doctor_urls', [])
        print(f"📊 Đã load {len(doctor_urls)} URLs từ file doctor_urls_list.json")
        
        # Giới hạn số lượng bác sĩ để test (có thể thay đổi)
        max_doctors = 10  # Chỉ crawl 10 bác sĩ đầu tiên để test
        if len(doctor_urls) > max_doctors:
            doctor_urls = doctor_urls[:max_doctors]
            print(f"🔄 Giới hạn crawl {max_doctors} bác sĩ đầu tiên để test")
            
    except FileNotFoundError:
        print("⚠️ Không tìm thấy file doctor_urls_list.json, sử dụng URLs mặc định")
        doctor_urls = [
            "https://www.vinmec.com/vie/chuyen-gia-y-te/pham-nhat-an-50932-vi",
            "https://www.vinmec.com/vie/chuyen-gia-y-te/do-tat-cuong-416-vi"
        ]
    except Exception as e:
        print(f"❌ Lỗi khi đọc file URLs: {e}")
        return None
    
    all_doctors = []
    successful_crawls = 0
    
    for i, url in enumerate(doctor_urls, 1):
        print(f"\n📋 ĐANG CRAWL BÁC SĨ {i}/{len(doctor_urls)}")
        print(f"🔗 URL: {url}")
        print("-" * 50)
        
        try:
            doctor_info = crawl_single_doctor(url)
            if doctor_info and doctor_info.get('ten_bac_si'):
                all_doctors.append(doctor_info)
                successful_crawls += 1
                print(f"✅ Thành công: {doctor_info['ten_bac_si']}")
            else:
                print("❌ Không trích xuất được thông tin")
                
        except Exception as e:
            print(f"❌ Lỗi khi crawl: {e}")
        
        # Thêm delay giữa các request
        if i < len(doctor_urls):
            print("⏳ Chờ 2 giây trước khi crawl tiếp...")
            import time
            time.sleep(5)
    
    # Lưu tất cả thông tin bác sĩ
    if all_doctors:
        output_file = 'vinmec_doctors_database.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_doctors, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 60)
        print("📊 TỔNG KẾT:")
        print(f"✅ Crawl thành công: {successful_crawls}/{len(doctor_urls)} bác sĩ")
        print(f"💾 Đã lưu vào file: {output_file}")
        
        # In danh sách bác sĩ
        print("\n👨‍⚕️ DANH SÁCH BÁC SĨ:")
        for i, doctor in enumerate(all_doctors, 1):
            print(f"{i}. {doctor.get('ten_bac_si', 'N/A')} - {doctor.get('noi_lam_viec', 'N/A')}")
        
        print("=" * 60)
        print("🎉 HOÀN THÀNH TẤT CẢ!")
        
        return all_doctors
    else:
        print("\n❌ Không crawl được bác sĩ nào!")
        return None

def crawl_single_doctor(url):
    """
    Crawl thông tin một bác sĩ từ URL
    """
    
    try:
        # Headers để giả lập trình duyệt
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        # Gửi request
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Trích xuất thông tin bác sĩ
        doctor_info = extract_doctor_info(soup, url)
        
        return doctor_info
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi tải trang: {e}")
        return None
    except Exception as e:
        print(f"❌ Lỗi không xác định: {e}")
        return None

def crawl_vinmec_doctor_profile():
    """
    Script cũ để crawl một bác sĩ (giữ lại để tương thích)
    """
    url = "https://www.vinmec.com/vie/chuyen-gia-y-te/pham-nhat-an-50932-vi"
    return crawl_single_doctor(url)

def extract_doctor_info(soup, url=""):
    """
    Trích xuất thông tin chi tiết từ HTML
    """
    doctor_info = {
        "url": url,
        "ten_bac_si": "",
        "anh_dai_dien": "",
        "gioi_thieu": "",
        "chuyen_mon": [],
        "noi_lam_viec": "",
        "dich_vu": [],
        "dao_tao": [],
        "kinh_nghiem_lam_viec": []
    }
    
    try:
        print("🔍 Đang tìm section profile_doctor...")
        
        # Tìm section profile_doctor
        profile_section = soup.find('section', class_='profile_doctor')
        if not profile_section:
            print("⚠️ Không tìm thấy section profile_doctor")
            return doctor_info
        
        print("✅ Tìm thấy section profile_doctor")
        
        # Trích xuất từ col-5 (thông tin cơ bản)
        col_5 = profile_section.find("div", class_="col-5")
        if col_5:
            print("🔍 Đang trích xuất thông tin từ col-5...")
            extract_basic_info(col_5, doctor_info, soup)
        
        # Trích xuất từ col-7 (chi tiết)
        col_7 = profile_section.find("div", class_="col-7")
        if col_7:
            print("🔍 Đang trích xuất thông tin từ col-7...")
            extract_detailed_info(col_7, doctor_info)
        
    except Exception as e:
        print(f"❌ Lỗi khi trích xuất thông tin: {e}")
    
    return doctor_info

def extract_basic_info(col_5, doctor_info, soup):
    """
    Trích xuất thông tin cơ bản từ col-5
    """
    try:
        # 1. TÊN BÁC SĨ
        name_element = col_5.find('div', class_='f22 bold cl-blue mt1 mb1')
        if name_element:
            doctor_info["ten_bac_si"] = clean_text(name_element.get_text())
            print(f"   ✅ Tên: {doctor_info['ten_bac_si']}")
        
        # 2. ẢNH ĐẠI DIỆN
        avar_doctor_div = col_5.find('div', class_='flex avar_doctor')
        if avar_doctor_div:
            img_link = avar_doctor_div.find('a', class_='thumbblock thumb200x255')
            if img_link:
                img_element = img_link.find('img')
                if img_element and img_element.get('src'):
                    img_src = img_element.get('src')
                    if img_src.startswith('/'):
                        doctor_info["anh_dai_dien"] = f"https://www.vinmec.com{img_src}"
                    else:
                        doctor_info["anh_dai_dien"] = img_src
                    print(f"   ✅ Ảnh: {doctor_info['anh_dai_dien']}")
        
        # 3. GIỚI THIỆU ĐẦY ĐỦ
        desc_detail = col_5.find("div", class_="desc_detail")
        if desc_detail:
            paragraphs = desc_detail.find_all("p")
            full_intro = []
            for p in paragraphs:
                text = clean_text(p.get_text())
                if text:
                    full_intro.append(text)
            
            if full_intro:
                doctor_info["gioi_thieu"] = "\n\n".join(full_intro)
                print(f"   ✅ Giới thiệu: {len(doctor_info['gioi_thieu'])} ký tự")
        
    except Exception as e:
        print(f"   ❌ Lỗi khi trích xuất thông tin cơ bản: {e}")

def extract_detailed_info(col_7, doctor_info):
    """
    Trích xuất thông tin chi tiết từ col-7
    """
    try:
        # 1. CHUYÊN MÔN (positions)
        positions_section = col_7.find("div", {"id": "positions"})
        if positions_section:
            position_divs = positions_section.find_all('div', class_='mt1')
            for div in position_divs:
                text = clean_text(div.get_text())
                if text:
                    doctor_info["chuyen_mon"].append(text)
            print(f"   ✅ Chuyên môn: {len(doctor_info['chuyen_mon'])} mục")
        
        # 2. NƠI LÀM VIỆC (hospitals)
        hospitals_section = col_7.find("div", {"id": "hospitals"})
        if hospitals_section:
            workplace_link = hospitals_section.find('a')
            if workplace_link:
                doctor_info["noi_lam_viec"] = clean_text(workplace_link.get_text())
                print(f"   ✅ Nơi làm việc: {doctor_info['noi_lam_viec']}")
        
        # 3. DỊCH VỤ (services)
        services_section = col_7.find("div", {"id": "services"})
        if services_section:
            service_list = services_section.find('ul', class_='list_dot')
            if service_list:
                service_items = service_list.find_all('li')
                for li in service_items:
                    text = clean_text(li.get_text())
                    if text:
                        doctor_info["dich_vu"].append(text)
            print(f"   ✅ Dịch vụ: {len(doctor_info['dich_vu'])} mục")
        
        # 4. ĐÀO TẠO (educations)
        educations_section = col_7.find("div", {"id": "educations"})
        if educations_section:
            content_div = educations_section.find('div', class_='content')
            if content_div:
                education_paragraphs = content_div.find_all('p')
                for p in education_paragraphs:
                    text = clean_text(p.get_text())
                    if text and text != "...":
                        doctor_info["dao_tao"].append(text)
            print(f"   ✅ Đào tạo: {len(doctor_info['dao_tao'])} mục")
        
        # 5. KINH NGHIỆM LÀM VIỆC (experience)
        work_exp_section = col_7.find("div", {"id": "experience"})
        if work_exp_section:
            content_div = work_exp_section.find('div', class_='content')
            if content_div:
                work_paragraphs = content_div.find_all('p')
                for p in work_paragraphs:
                    text = clean_text(p.get_text())
                    if text and text != "...":
                        doctor_info["kinh_nghiem_lam_viec"].append(text)
            print(f"   ✅ Kinh nghiệm: {len(doctor_info['kinh_nghiem_lam_viec'])} mục")
        
    except Exception as e:
        print(f"   ❌ Lỗi khi trích xuất thông tin chi tiết: {e}")

def clean_text(text):
    """
    Làm sạch text: loại bỏ khoảng trắng thừa, ký tự đặc biệt
    """
    if not text:
        return ""
    
    # Loại bỏ khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Loại bỏ ký tự đặc biệt không mong muốn
    text = text.replace('\xa0', ' ')  # Non-breaking space
    text = text.replace('\u200b', '')  # Zero-width space
    
    return text

if __name__ == "__main__":
    # Chạy script crawl nhiều bác sĩ
    print("🤖 CHỌN CHỨC NĂNG:")
    print("1. Crawl nhiều bác sĩ (mặc định)")
    print("2. Crawl một bác sĩ")
    
    # Mặc định crawl nhiều bác sĩ
    result = crawl_multiple_doctors()
    
    if result:
        print(f"\n🎉 Đã crawl thành công {len(result)} bác sĩ!")
    else:
        print("\n💥 Script gặp lỗi!")
