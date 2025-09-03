# 🤖 Dr. HealthBot - AI Health Consultation System

Hệ thống tư vấn sức khỏe AI cá nhân hóa với kiến trúc client-server và streaming response.

## 📋 Tổng quan hệ thống

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Homepage.py   │    │ DiabeteDoctor.py │    │Doctor_chatbot.py│
│                 │    │                  │    │                 │
│ Đăng ký bệnh    │────▶│ Phân tích AI     │────▶│ Chat tư vấn     │
│ nhân + CCCD     │    │ + Chẩn đoán      │    │ sức khỏe        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        │
                       ┌─────────────────┐               │
                       │patient_data.json│               │
                       │                 │               │
                       │ Lưu trữ thông   │◀──────────────┘
                       │ tin bệnh nhân   │
                       └─────────────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │Doctor_chatbot_server│
                     │                     │
                     │ • System prompt     │
                     │ • OpenAI API        │
                     │ • Streaming         │
                     └─────────────────────┘
```

## 🚀 Cài đặt và khởi động

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình environment

File `.env` đã được cấu hình với:
```env
BASE_URL=https://mkp-api.fptcloud.com
MODEL_NAME=gpt-oss-20b
CHATBOT_SERVER_HOST=localhost
CHATBOT_SERVER_PORT=8502
FPT_API_KEY="sk-pkXO_SaUE_BIWGz3P-cTow"
```

### 3. Khởi động hệ thống

#### Cách 1: Khởi động tự động (Khuyến nghị)
```bash
./start_system.sh
```

#### Cách 2: Khởi động thủ công

**Terminal 1 - Chatbot Server:**
```bash
python Doctor_chatbot_server.py
```

**Terminal 2 - Streamlit App:**
```bash
streamlit run Homepage.py
```

## 📱 Cách sử dụng

### Bước 1: Đăng ký thông tin bệnh nhân
1. Mở `Homepage.py`
2. Upload ảnh CCCD để trích xuất thông tin tự động
3. Điền thông tin bổ sung
4. Lưu thông tin bệnh nhân

### Bước 2: Phân tích sức khỏe
1. Chuyển sang `DiabeteDoctor.py`
2. Điền thông tin triệu chứng và lối sống
3. Nhận kết quả phân tích AI và khuyến nghị bác sĩ
4. Thông tin được lưu vào `patient_data.json`

### Bước 3: Tư vấn với AI Chatbot
1. Chuyển sang `Doctor_chatbot.py`
2. Chat với Dr. HealthBot về các vấn đề sức khỏe
3. Nhận lời tư vấn cá nhân hóa dựa trên thông tin đã có

## 🔧 Kiểm tra hệ thống

### Test server chatbot:
```bash
python test_chatbot_server.py
```

### Kiểm tra endpoints thủ công:

**Health check:**
```bash
curl http://localhost:8502/health
```

**Patient info:**
```bash
curl http://localhost:8502/patient-info
```

**Chat test:**
```bash
curl -X POST http://localhost:8502/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Xin chào"}], "stream": false}'
```

## 🎯 Tính năng chính

### 🤖 AI Chatbot
- **Cá nhân hóa:** Tích hợp 5 đoạn thông tin bệnh nhân
- **Multi-turn conversation:** Hỗ trợ cuộc trò chuyện nhiều lượt
- **Streaming response:** Phản hồi real-time
- **An toàn y tế:** Không tự chẩn đoán, khuyến nghị gặp bác sĩ

### 📊 System Architecture
- **Client:** Streamlit interface với UI/UX chuyên nghiệp
- **Server:** Flask API với OpenAI integration
- **Data:** JSON file storage với 5 segments thông tin
- **Communication:** REST API với streaming support

### 🎨 UI/UX Features
- **Responsive design:** Tương thích mọi thiết bị
- **Medical styling:** Thiết kế y tế chuyên nghiệp
- **Animations:** Hiệu ứng mượt mà, thân thiện
- **Status indicators:** Hiển thị trạng thái server
- **Error handling:** Xử lý lỗi graceful

## 📂 Cấu trúc file

```
Doctor_app/
├── .env                          # Cấu hình API
├── convert.py                    # Convert JSON to text segments
├── patient_data.json            # Dữ liệu bệnh nhân
├── Doctor_chatbot_server.py     # Server chatbot
├── test_chatbot_server.py       # Test suite
├── requirements.txt             # Dependencies
├── start_system.sh              # Script khởi động hệ thống
├── start_chatbot_server.sh      # Script khởi động server
└── pages/
    ├── Homepage.py              # Đăng ký bệnh nhân
    ├── DiabeteDoctor.py        # Phân tích AI
    └── Doctor_chatbot.py       # Giao diện chatbot
```

## 🔍 API Endpoints

### GET /health
Kiểm tra trạng thái server
```json
{
  "status": "healthy",
  "timestamp": "2025-09-02T10:30:00",
  "model": "gpt-oss-20b"
}
```

### GET /patient-info
Lấy thông tin bệnh nhân
```json
{
  "status": "success",
  "data": {
    "segment_1_personal_info": "...",
    "segment_2_lifestyle_health": "...",
    "segment_3_health_metrics": "...",
    "segment_4_ai_analysis": "...",
    "segment_5_doctor_recommendations": "..."
  }
}
```

### POST /chat
Chat với AI (support streaming)
```json
{
  "messages": [
    {"role": "user", "content": "Chỉ số BMI của tôi thế nào?"}
  ],
  "stream": true
}
```

## ⚠️ Lưu ý quan trọng

1. **API Key:** Đảm bảo API key hợp lệ trong file `.env`
2. **Patient Data:** File `patient_data.json` cần tồn tại để chatbot hoạt động tối ưu
3. **Server Status:** Kiểm tra server chatbot đang chạy trước khi sử dụng
4. **Medical Disclaimer:** Chatbot chỉ mang tính tham khảo, không thay thế bác sĩ

## 🐛 Troubleshooting

### Server không khởi động được:
- Kiểm tra port 8502 có bị chiếm không
- Xác nhận API key trong `.env`
- Kiểm tra file `convert.py` tồn tại

### Chatbot không phản hồi:
- Kiểm tra kết nối internet
- Verify API endpoint hoạt động
- Check log server để debug

### UI không hiển thị đúng:
- Refresh browser
- Kiểm tra browser console
- Restart Streamlit app

## 🎉 Demo

Sau khi khởi động thành công:
1. **Homepage:** http://localhost:8501
2. **Chatbot Server:** http://localhost:8502
3. **Health Check:** http://localhost:8502/health

---

*Được phát triển bởi VinBig Doctor App Team - Công nghệ AI phục vụ sức khỏe cộng đồng* 🏥✨
