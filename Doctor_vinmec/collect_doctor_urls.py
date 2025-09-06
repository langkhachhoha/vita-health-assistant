import requests
from bs4 import BeautifulSoup
import json
import time
import re

def collect_doctor_urls():
    """
    Thu thập tất cả URLs của bác sĩ từ trang chuyên gia y tế Vinmec
    Từ trang 2 đến trang 10
    """
    
    print("🚀 BẮT ĐẦU THU THẬP DANH SÁCH URL BÁC SĨ VINMEC")
    print("=" * 60)
    
    base_url = "https://www.vinmec.com/vie/chuyen-gia-y-te"
    all_doctor_urls = []
    
    # Headers để giả lập trình duyệt
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    # Thu thập từ trang 2 đến trang 20
    for page_num in range(2, 21):  # 2 đến 20
        if page_num == 2:
            url = f"{base_url}/page_2"
        else:
            url = f"{base_url}/page_{page_num}"
        
        print(f"\n📄 ĐANG THU THẬP TRANG {page_num}")
        print(f"🔗 URL: {url}")
        print("-" * 40)
        
        try:
            # Gửi request
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            print("✅ Tải trang thành công!")
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Tìm tất cả links bác sĩ
            doctor_links = extract_doctor_links(soup)
            
            if doctor_links:
                print(f"🔍 Tìm thấy {len(doctor_links)} bác sĩ")
                all_doctor_urls.extend(doctor_links)
                
                # In một vài URL mẫu
                for i, link in enumerate(doctor_links[:3], 1):
                    print(f"   {i}. {link}")
                if len(doctor_links) > 3:
                    print(f"   ... và {len(doctor_links) - 3} bác sĩ khác")
            else:
                print("⚠️ Không tìm thấy bác sĩ nào")
            
            # Delay giữa các trang
            if page_num < 100:
                print("⏳ Chờ 3 giây trước khi tải trang tiếp...")
                time.sleep(3)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Lỗi khi tải trang {page_num}: {e}")
            continue
        except Exception as e:
            print(f"❌ Lỗi không xác định trang {page_num}: {e}")
            continue
    
    # Loại bỏ URL trùng lặp
    unique_urls = list(set(all_doctor_urls))
    
    # Lưu kết quả
    if unique_urls:
        # Sắp xếp URLs
        unique_urls.sort()
        
        # Lưu vào JSON
        output_data = {
            "total_doctors": len(unique_urls),
            "collected_from_pages": list(range(2, 11)),
            "doctor_urls": unique_urls
        }
        
        with open('doctor_urls_list.json', 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        # Lưu vào file text đơn giản
        with open('doctor_urls.txt', 'w', encoding='utf-8') as f:
            for url in unique_urls:
                f.write(url + '\n')
        
        print("\n" + "=" * 60)
        print("📊 TỔNG KẾT THU THẬP:")
        print(f"📄 Đã kiểm tra: {9} trang (trang 2-10)")
        print(f"👨‍⚕️ Tổng số bác sĩ: {len(unique_urls)} URLs")
        print(f"💾 Đã lưu vào: doctor_urls_list.json")
        print(f"📝 Đã lưu vào: doctor_urls.txt")
        
        # Hiển thị một vài URL mẫu
        print(f"\n🔗 MẪU URLS (10 đầu tiên):")
        for i, url in enumerate(unique_urls[:10], 1):
            doctor_name = extract_doctor_name_from_url(url)
            print(f"{i:2d}. {doctor_name} - {url}")
        
        if len(unique_urls) > 10:
            print(f"    ... và {len(unique_urls) - 10} bác sĩ khác")
        
        print("=" * 60)
        print("🎉 HOÀN THÀNH THU THẬP URLS!")
        
        return unique_urls
    
    else:
        print("\n❌ Không thu thập được URL nào!")
        return None

def extract_doctor_links(soup):
    """
    Trích xuất tất cả links bác sĩ từ một trang
    """
    doctor_links = []
    
    try:
        # Tìm tất cả các link có href chứa '/vie/chuyen-gia-y-te/' và có class 'list_name_doctor'
        # Dựa trên structure HTML bạn cung cấp
        
        # Cách 1: Tìm trong các thẻ a có class chứa 'list_name_doctor'
        doctor_link_elements = soup.find_all('a', class_=lambda x: x and 'list_name_doctor' in x)
        
        for link in doctor_link_elements:
            href = link.get('href')
            if href and '/vie/chuyen-gia-y-te/' in href:
                # Tạo URL đầy đủ nếu cần
                if href.startswith('/'):
                    full_url = f"https://www.vinmec.com{href}"
                else:
                    full_url = href
                doctor_links.append(full_url)
        
        # Cách 2: Tìm tất cả links chứa pattern '/vie/chuyen-gia-y-te/'
        if not doctor_links:
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href')
                if href and '/vie/chuyen-gia-y-te/' in href and href.count('-') >= 2:  # URL bác sĩ thường có dạng name-id-vi
                    if href.startswith('/'):
                        full_url = f"https://www.vinmec.com{href}"
                    else:
                        full_url = href
                    doctor_links.append(full_url)
        
        # Cách 3: Tìm trong div có class chứa 'flex' và 'doctor'
        if not doctor_links:
            flex_divs = soup.find_all('div', class_=lambda x: x and 'flex' in x)
            for div in flex_divs:
                links = div.find_all('a', href=True)
                for link in links:
                    href = link.get('href')
                    if href and '/vie/chuyen-gia-y-te/' in href:
                        if href.startswith('/'):
                            full_url = f"https://www.vinmec.com{href}"
                        else:
                            full_url = href
                        doctor_links.append(full_url)
        
    except Exception as e:
        print(f"   ❌ Lỗi khi trích xuất links: {e}")
    
    # Loại bỏ duplicates trong trang này
    return list(set(doctor_links))

def extract_doctor_name_from_url(url):
    """
    Trích xuất tên bác sĩ từ URL
    """
    try:
        # URL có dạng: /vie/chuyen-gia-y-te/pham-nhat-an-50932-vi
        parts = url.split('/')
        if len(parts) > 0:
            name_part = parts[-1]  # Lấy phần cuối
            # Loại bỏ số và -vi
            name_clean = re.sub(r'-\d+-vi$', '', name_part)
            # Thay thế - bằng space và title case
            name_formatted = name_clean.replace('-', ' ').title()
            return name_formatted
    except:
        pass
    return "Unknown Doctor"

def create_url_list_for_crawler():
    """
    Tạo danh sách URL để sử dụng cho crawler chính
    """
    try:
        # Đọc file URLs đã thu thập
        with open('doctor_urls_list.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        urls = data.get('doctor_urls', [])
        
        if urls:
            print(f"\n🔧 TẠO FILE CẤU HÌNH CHO CRAWLER CHÍNH")
            print(f"📊 Có {len(urls)} URLs để crawl")
            
            # Tạo file Python config
            config_content = f'''# Auto-generated URL list for Vinmec doctor crawler
# Generated from {len(data.get("collected_from_pages", []))} pages
# Total doctors found: {len(urls)}

DOCTOR_URLS = [
'''
            
            for url in urls[:50]:  # Giới hạn 50 URLs đầu tiên để test
                config_content += f'    "{url}",\n'
            
            config_content += ''']

# Usage example:
# from doctor_urls_config import DOCTOR_URLS
# for url in DOCTOR_URLS:
#     crawl_single_doctor(url)
'''
            
            with open('doctor_urls_config.py', 'w', encoding='utf-8') as f:
                f.write(config_content)
            
            print("✅ Đã tạo file: doctor_urls_config.py")
            print(f"📝 Chứa {min(50, len(urls))} URLs đầu tiên")
            
        else:
            print("❌ Không có URLs để tạo config")
            
    except Exception as e:
        print(f"❌ Lỗi khi tạo config: {e}")

if __name__ == "__main__":
    # Thu thập URLs
    urls = collect_doctor_urls()
    
    if urls:
        # Tạo file config cho crawler chính
        create_url_list_for_crawler()
        
        print(f"\n🎯 BƯỚC TIẾP THEO:")
        print("1. Kiểm tra file doctor_urls_list.json")
        print("2. Sử dụng URLs này cho crawler chính")
        print("3. Hoặc import từ doctor_urls_config.py")
    else:
        print("\n💥 Không thu thập được URLs!")
