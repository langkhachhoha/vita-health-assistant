# 🌟 VITA - VinBig Intelligent Treatment Assistant  
> 🚀 *AI đồng hành cùng sức khỏe của bạn*  
<img src="asset/image.png" alt="Homepage" width="600" style="border-radius: 10px;">

## 🎯 Giới thiệu  

**VITA** là nền tảng **trợ lý y tế thông minh** ứng dụng trí tuệ nhân tạo, được phát triển bởi **VinBig AI**.  
Ứng dụng hướng đến việc **hỗ trợ bác sĩ** và **cá nhân hóa trải nghiệm chăm sóc sức khỏe** cho từng người dùng.  

## 🚀 Tính năng chính  

- 🩺 **Phân tích nguy cơ sức khỏe** (ví dụ: tiểu đường, bệnh mãn tính) với độ chính xác cao  
- 💬 **Chatbot tư vấn y tế thông minh** – trò chuyện tự nhiên, cá nhân hóa theo từng bệnh nhân  
- 🆔 **Nhận dạng thông tin cá nhân (CCCD)** – nhanh chóng, an toàn và tiện lợi  
- 📊 **Theo dõi & quản lý tình trạng sức khỏe** – giúp người dùng chủ động trong hành trình chăm sóc sức khỏe  

## 🔬 Công nghệ AI tích hợp  

- Ứng dụng trí tuệ nhân tạo toàn diện trong y tế  
- Phân tích dữ liệu y tế đa chiều để hỗ trợ quyết định lâm sàng  
- Trợ lý ảo thông minh, linh hoạt và dễ mở rộng  
- Cam kết bảo mật và tuân thủ các tiêu chuẩn quốc tế  

## 🎯 Sứ mệnh  

VITA cam kết mang đến một **giải pháp y tế an toàn, chính xác và hiệu quả**,  
giúp bác sĩ đưa ra quyết định điều trị tối ưu và đồng hành cùng bệnh nhân trong hành trình chăm sóc sức khỏe.  

---
✨ *VITA – AI đồng hành cùng sức khỏe của bạn.*


---

## 🖼️ Giao diện ứng dụng

<div align="center">

### 🏠 **Trang chủ**
<img src="asset/Homepage_2.jpeg" alt="Homepage" width="600" style="border-radius: 10px;">

### 🩺 **Phân tích nguy cơ tiểu đường**
<img src="asset/Diabete_1.jpeg" alt="Diabetes Doctor" width="600" style="border-radius: 10px;">

### 💬 **Chatbot tư vấn y tế**
<img src="asset/Chatbot_1.jpeg" alt="Chatbot" width="600" style="border-radius: 10px;">

### 📱 **Các tính năng khác**
<div style="display: flex; justify-content: center; gap: 20px;">
  <img src="asset/Homepage_3.jpeg" alt="Feature 1" width="250" style="border-radius: 10px;">
  <img src="asset/Diabete_2.jpeg" alt="Feature 2" width="250" style="border-radius: 10px;">
  <img src="asset/Chatbot_2.jpeg" alt="Feature 3" width="250" style="border-radius: 10px;">
</div>

</div>

---

## 🚀 Hướng dẫn cài đặt và sử dụng

### 📋 **Yêu cầu**
- **Python 3.9** trở lên
- **4GB RAM** trở lên
- **Kết nối internet** để sử dụng AI

### 🛠️ **Cài đặt**

**Bước 1: Tải về và cài đặt**
```bash
# Tải project về máy
git clone https://github.com/your-repo/doctor-ai.git
cd doctor-ai

# Cài đặt các thư viện cần thiết
pip install -r Doctor_app/requirements.txt
```

## ⚙️ Cấu hình môi trường (.env)

Ứng dụng **VITA** cần một file cấu hình `.env` để kết nối với các dịch vụ AI trên **FPT Cloud Marketplace**.  

👉 Tạo file `.env` trong thư mục gốc của **Doctor_app** với nội dung mẫu sau:

```bash
# API Configuration for Health Chatbot
BASE_URL=https://mkp-api.fptcloud.com
MODEL_NAME=gpt-oss-20b             # Model cho Chatbot Y tế

# API Configuration for OCR
OCR_MODEL_NAME=llama-4-scout-17b-16e   # Model cho OCR CCCD

# Server Configuration
CHATBOT_SERVER_HOST=localhost
CHATBOT_SERVER_PORT=8502

# FPT API Key
FPT_API_KEY=your_api_key_here
```

### 🎮 Cách chạy hệ thống

Mở **1 terminal** và chạy lần lượt các lệnh sau để khởi động toàn bộ hệ thống:

```bash
# Chạy server OCR CCCD
python Doctor_app/cccd_ocr_server.py

# Chạy server phân tích tiểu đường
python Doctor_app/DiabeteDoctor-Server.py

# Chạy server Chatbot y tế
python Doctor_app/Doctor_chatbot_server.py

# Cuối cùng, chạy giao diện chính
streamlit run Doctor_app/Homepage.py
```

➡️ **Truy cập:** http://localhost:8501
<img src="asset/Homepage_1.jpeg" alt="Diabetes Doctor" width="600" style="border-radius: 10px;">

### � **Cách sử dụng**

#### **🏠 Trang chủ**
- Chọn chức năng muốn sử dụng từ menu bên trái

#### **🩺 Phân tích nguy cơ tiểu đường**
1. Nhập thông tin cá nhân (tuổi, giới tính, cân nặng...)
2. Chụp ảnh CCCD (tùy chọn) để hệ thống tự điền thông tin
3. Nhấn **"Phân tích nguy cơ"**
4. Xem kết quả và khuyến nghị từ AI

#### **💬 Chatbot tư vấn y tế**
1. Nhập câu hỏi về sức khỏe
2. AI sẽ tư vấn và đưa ra lời khuyên
3. Có thể hỏi tiếp các câu hỏi liên quan

#### **🆔 Quản lý hồ sơ**
- Chụp ảnh CCCD để tạo hồ sơ bệnh nhân tự động
- Lưu trữ và tra cứu thông tin y tế

---

## 🔮 Tính năng sắp ra mắt

### 🚧 **Đang phát triển**
- 📱 **Ứng dụng di động** cho iOS và Android
- 🔬 **Phân tích thêm bệnh**: tim mạch, huyết áp, tiểu đường type 1
- 🌍 **Giao diện tiếng Anh** 
- � **Kết nối bệnh viện** để lưu hồ sơ trực tiếp
- 🎤 **Tư vấn bằng giọng nói**
- 📊 **Theo dõi sức khỏe dài hạn**

---

## ❓ Hỗ trợ

### 🐛 **Gặp lỗi?**
- Kiểm tra lại API keys trong file `.env`
- Đảm bảo đã cài đủ 4 servers
- Kiểm tra kết nối internet

### 📞 **Liên hệ**
📧 **Hỗ trợ kỹ thuật:** haminhhieu1005@gmail.com 

📧 **Tư vấn y tế:** 0916061368

---

<div align="center">
  <img src="asset/Homepage_4.jpeg" alt="Doctor AI Team" width="500" style="border-radius: 15px;">
  
  **🏥 Doctor AI - Sức khỏe thông minh cho mọi người**
  
  **© 2025 Doctor AI. Bản quyền thuộc về nhà phát triển.**
</div>
