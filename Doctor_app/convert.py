import json
from datetime import datetime
import os

dir = os.getcwd()

def convert_patient_data_to_text_segments(json_file_path):
    """
    Chuyển đổi dữ liệu bệnh nhân từ file JSON thành 5 đoạn text tiếng Việt
    để sử dụng cho LLM agent cá nhân hóa
    """
    
    try:
        # Đọc file JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        patient_data = data['current_patient']
        
        # Đoạn 1: Thông tin cá nhân cơ bản
        personal_info = patient_data['personal_info']
        segment_1 = f"""Thông tin cá nhân của bệnh nhân:
- Họ và tên: {personal_info['full_name']}
- Ngày sinh: {personal_info['birth_date']} (tuổi: {calculate_age(personal_info['birth_date'])})
- Giới tính: {personal_info['gender']}
- Số CCCD: {personal_info['id_number']}
- Địa chỉ thường trú: {personal_info['address']}
- Quốc tịch: {personal_info['nationality']}
- Quê quán: {personal_info['place_origin']}"""

        # Đoạn 2: Thông tin y tế và lối sống
        medical_analysis = patient_data['medical_analysis']
        segment_2 = f"""Thông tin sức khỏe và lối sống hiện tại:
- Triệu chứng hiện tại: {medical_analysis['current_symptoms']}
- Chất lượng giấc ngủ: {medical_analysis['sleep_quality']}
- Tiền sử gia đình: {medical_analysis['family_history']}
- Thói quen sinh hoạt: {medical_analysis['lifestyle_habits']}
- Môi trường làm việc: {medical_analysis['work_environment']}
- Mức độ căng thẳng: {medical_analysis['stress_anxiety_level']}
- Thông tin bổ sung: {medical_analysis['additional_info']}"""

        # Đoạn 3: Dữ liệu sức khỏe chi tiết
        if 'diabetes_analysis' in patient_data and 'symptoms_data' in patient_data['diabetes_analysis']:
            symptoms_data = patient_data['diabetes_analysis']['symptoms_data']
            segment_3 = f"""Chỉ số sức khỏe chi tiết:
- Huyết áp cao: {'Có' if symptoms_data['high_bp'] == 1 else 'Không'}
- Cholesterol cao: {'Có' if symptoms_data['high_chol'] == 1 else 'Không'}
- Đã kiểm tra cholesterol trong 5 năm chưa: {'Có' if symptoms_data['chol_check'] == 1 else 'Không'}
- Chỉ số BMI: {symptoms_data['bmi']:.2f} ({get_bmi_status(symptoms_data['bmi'])})
- Đã từng hút ít nhất 100 điếu thuốc trong suốt cuộc đời mình chưa? {'Có' if symptoms_data['smoker'] == 1 else 'Không'}
- Tiền sử đột quỵ: {'Có' if symptoms_data['stroke'] == 1 else 'Không'}
- Bệnh tim: {'Có' if symptoms_data['heart_disease'] == 1 else 'Không'}
- Có tham gia hoạt động thể chất trong 30 ngày qua không? {'Có' if symptoms_data['phys_activity'] == 1 else 'Không'}
- Ăn trái cây thường xuyên: {'Có' if symptoms_data['fruits'] == 1 else 'Không'}
- Ăn rau củ thường xuyên: {'Có' if symptoms_data['veggies'] == 1 else 'Không'}
- Uống rượu nhiều: {'Có' if symptoms_data['hvy_alcohol'] == 1 else 'Không'}
- Có bảo hiểm y tế: {'Có' if symptoms_data['any_healthcare'] == 1 else 'Không'}
- Không đủ tiền khám bác sĩ: {'Có' if symptoms_data['no_doc_cost'] == 1 else 'Không'}
- Sức khỏe tổng quát: {get_health_status(symptoms_data['gen_hlth'])}
- Chiều cao: {symptoms_data['height']} cm
- Cân nặng: {symptoms_data['weight']} kg"""
        else:
            segment_3 = "Chưa có dữ liệu sức khỏe chi tiết được thu thập."

        # Đoạn 4: Kết quả phân tích AI về tiểu đường
        if 'diabetes_analysis' in patient_data and 'ai_diagnosis' in patient_data['diabetes_analysis']:
            ai_diagnosis = patient_data['diabetes_analysis']['ai_diagnosis']
            segment_4 = f"""Kết quả phân tích AI về nguy cơ tiểu đường:
- Dự đoán mắc bệnh: {'Có nguy cơ cao' if ai_diagnosis['prediction'] == 1 else 'Nguy cơ thấp'}
- Xác suất mắc bệnh: {ai_diagnosis['probability']:.4f} ({ai_diagnosis['probability']*100:.2f}%)
- Mức độ nguy cơ: {ai_diagnosis['risk_level'].capitalize()}
- Độ tin cậy của AI: {ai_diagnosis['confidence']:.2f}%
- Ngày phân tích: {patient_data['diabetes_analysis']['analysis_date']}"""
        else:
            segment_4 = "Chưa có kết quả phân tích AI về nguy cơ tiểu đường."

        # Đoạn 5: Đánh giá và khuyến nghị của bác sĩ
        if 'diabetes_analysis' in patient_data and 'doctor_notes' in patient_data['diabetes_analysis']:
            doctor_notes = patient_data['diabetes_analysis']['doctor_notes']
            recommendations_text = '\n'.join([f"  {rec}" for rec in doctor_notes['recommendations']])
            segment_5 = f"""Đánh giá và khuyến nghị của bác sĩ:
- Đánh giá nguy cơ: {doctor_notes['risk_assessment']}
- Các khuyến nghị chi tiết:
{recommendations_text}"""
        else:
            segment_5 = "Chưa có đánh giá và khuyến nghị từ bác sĩ."

        return {
            'segment_1_personal_info': segment_1,
            'segment_2_lifestyle_health': segment_2,
            'segment_3_health_metrics': segment_3,
            'segment_4_ai_analysis': segment_4,
            'segment_5_doctor_recommendations': segment_5
        }
        
    except FileNotFoundError:
        return {"error": "Không tìm thấy file JSON"}
    except KeyError as e:
        return {"error": f"Thiếu trường dữ liệu: {e}"}
    except Exception as e:
        return {"error": f"Lỗi xử lý dữ liệu: {e}"}

def calculate_age(birth_date_str):
    """Tính tuổi từ ngày sinh"""
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age
    except:
        return "Không xác định"

def get_bmi_status(bmi):
    """Phân loại BMI"""
    if bmi < 18.5:
        return "Thiếu cân"
    elif 18.5 <= bmi < 25:
        return "Bình thường"
    elif 25 <= bmi < 30:
        return "Thừa cân"
    else:
        return "Béo phì"

def get_health_status(gen_hlth):
    """Chuyển đổi mã sức khỏe tổng quát thành text"""
    health_map = {
        1: "Xuất sắc",
        2: "Rất tốt", 
        3: "Tốt",
        4: "Khá",
        5: "Kém"
    }
    return health_map.get(gen_hlth, "Không xác định")

# Sử dụng function
def main():
    """Function chính để test"""
    json_file_path = os.path.join(dir, "Doctor_app", "patient_data.json")

    segments = convert_patient_data_to_text_segments(json_file_path)
    
    if 'error' in segments:
        print(f"Lỗi: {segments['error']}")
        return
    
    print("=" * 80)
    print("CÁC ĐOẠN THÔNG TIN BỆNH NHÂN CHO LLM AGENT")
    print("=" * 80)
    
    for i, (key, segment) in enumerate(segments.items(), 1):
        print(f"\n🔹 ĐOẠN {i}: {key.upper()}")
        print("-" * 60)
        print(segment)
        print()

if __name__ == "__main__":
    main()