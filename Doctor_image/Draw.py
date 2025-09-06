import os
from PIL import Image, ImageDraw, ImageEnhance

def create_doctor_grid(
    background_path="Background.png",
    doctor_image_path="Doctor_1.png", 
    output_path="doctor_grid.png",
    rows=5,
    cols=5,
    spacing_ratio=0.15  # Tăng khoảng cách mặc định để thoáng hơn
):
    """
    Tạo lưới hình ảnh doctor trên background
    
    Args:
        background_path: Đường dẫn đến ảnh background
        doctor_image_path: Đường dẫn đến ảnh doctor
        output_path: Đường dẫn lưu ảnh kết quả
        rows: Số hàng (mặc định 10)
        cols: Số cột (mặc định 15)
        spacing_ratio: Tỷ lệ khoảng cách so với kích thước ảnh doctor (mặc định 0.15 để thoáng hơn)
    
    Returns:
        PIL.Image: Ảnh kết quả
    """
    
    # Đường dẫn tương đối từ thư mục hiện tại
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bg_path = os.path.join(current_dir, background_path)
    doc_path = os.path.join(current_dir, doctor_image_path)
    out_path = os.path.join(current_dir, output_path)
    
    # Tải ảnh background
    try:
        background = Image.open(bg_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Không tìm thấy file background: {bg_path}")
        return None
    
    # Tải ảnh doctor
    try:
        doctor_img = Image.open(doc_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Không tìm thấy file doctor: {doc_path}")
        return None
    
    # Lấy kích thước background
    bg_width, bg_height = background.size
    
    # Tính toán kích thước tối ưu cho mỗi ảnh doctor
    # Tính khoảng trống cần thiết cho spacing
    total_spacing_width = (cols + 1) * spacing_ratio * bg_width / cols
    total_spacing_height = (rows + 1) * spacing_ratio * bg_height / rows
    
    # Kích thước khả dụng cho các ảnh doctor
    available_width = bg_width - total_spacing_width
    available_height = bg_height - total_spacing_height
    
    # Kích thước mỗi ảnh doctor
    doctor_width = int(available_width / cols)
    doctor_height = int(available_height / rows)
    
    # Resize ảnh doctor để phù hợp với chất lượng cao nhất
    # Sử dụng LANCZOS cho chất lượng tốt nhất và tránh làm mờ ảnh
    doctor_resized = doctor_img.resize((doctor_width, doctor_height), Image.Resampling.LANCZOS)
    
    # Tăng cường độ sắc nét của ảnh nếu cần
    enhancer = ImageEnhance.Sharpness(doctor_resized)
    doctor_resized = enhancer.enhance(1.3)  # Tăng độ sắc nét 30%
    
    # Tạo ảnh kết quả từ background
    result = background.copy()
    
    # Tính khoảng cách thực tế
    spacing_x = int(spacing_ratio * doctor_width)
    spacing_y = int(spacing_ratio * doctor_height)
    
    # Tính vị trí bắt đầu để căn giữa lưới
    start_x = (bg_width - (cols * doctor_width + (cols - 1) * spacing_x)) // 2
    start_y = (bg_height - (rows * doctor_height + (rows - 1) * spacing_y)) // 2
    
    print(f"Kích thước background: {bg_width}x{bg_height}")
    print(f"Kích thước mỗi ảnh doctor: {doctor_width}x{doctor_height}")
    print(f"Khoảng cách: {spacing_x}x{spacing_y}")
    print(f"Vị trí bắt đầu: ({start_x}, {start_y})")
    
    # Đặt các ảnh doctor lên background
    for row in range(rows):
        for col in range(cols):
            # Tính vị trí của ảnh doctor hiện tại
            x = start_x + col * (doctor_width + spacing_x)
            y = start_y + row * (doctor_height + spacing_y)
            
            # Paste ảnh doctor lên background
            result.paste(doctor_resized, (x, y), doctor_resized)
    
    # Lưu ảnh kết quả
    result.save(out_path, "PNG")
    print(f"Đã lưu ảnh kết quả tại: {out_path}")
    
    return result

def create_doctor_grid_preserve_aspect(
    background_path="Background.png",
    doctor_image_path="Doctor_1.png", 
    output_path="doctor_grid_aspect.png",
    rows=5,
    cols=5,
    spacing_ratio=0.15,
    max_size_ratio=0.8  # Tỉ lệ tối đa của ảnh doctor so với ô lưới
):
    """
    Tạo lưới hình ảnh doctor trên background, giữ nguyên tỉ lệ gốc của ảnh doctor
    
    Args:
        background_path: Đường dẫn đến ảnh background
        doctor_image_path: Đường dẫn đến ảnh doctor
        output_path: Đường dẫn lưu ảnh kết quả
        rows: Số hàng
        cols: Số cột
        spacing_ratio: Tỷ lệ khoảng cách
        max_size_ratio: Tỉ lệ tối đa của ảnh doctor so với ô lưới
    
    Returns:
        PIL.Image: Ảnh kết quả
    """
    
    # Đường dẫn tương đối từ thư mục hiện tại
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bg_path = os.path.join(current_dir, background_path)
    doc_path = os.path.join(current_dir, doctor_image_path)
    out_path = os.path.join(current_dir, output_path)
    
    # Tải ảnh background
    try:
        background = Image.open(bg_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Không tìm thấy file background: {bg_path}")
        return None
    
    # Tải ảnh doctor
    try:
        doctor_img = Image.open(doc_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Không tìm thấy file doctor: {doc_path}")
        return None
    
    # Lấy kích thước background và ảnh doctor gốc
    bg_width, bg_height = background.size
    orig_doctor_width, orig_doctor_height = doctor_img.size
    orig_aspect_ratio = orig_doctor_width / orig_doctor_height
    
    print(f"Kích thước ảnh doctor gốc: {orig_doctor_width}x{orig_doctor_height}")
    print(f"Tỉ lệ khung hình gốc: {orig_aspect_ratio:.2f}")
    
    # Tính toán kích thước ô lưới
    total_spacing_width = (cols + 1) * spacing_ratio * bg_width / cols
    total_spacing_height = (rows + 1) * spacing_ratio * bg_height / rows
    
    available_width = bg_width - total_spacing_width
    available_height = bg_height - total_spacing_height
    
    # Kích thước mỗi ô lưới
    cell_width = int(available_width / cols)
    cell_height = int(available_height / rows)
    
    # Tính kích thước ảnh doctor để vừa trong ô lưới và giữ nguyên tỉ lệ
    max_width = int(cell_width * max_size_ratio)
    max_height = int(cell_height * max_size_ratio)
    
    # Tính kích thước thực tế dựa trên tỉ lệ gốc
    if max_width / orig_aspect_ratio <= max_height:
        # Giới hạn bởi width
        doctor_width = max_width
        doctor_height = int(max_width / orig_aspect_ratio)
    else:
        # Giới hạn bởi height
        doctor_height = max_height
        doctor_width = int(max_height * orig_aspect_ratio)
    
    # Resize ảnh doctor với tỉ lệ được giữ nguyên
    doctor_resized = doctor_img.resize((doctor_width, doctor_height), Image.Resampling.LANCZOS)
    
    # Tăng cường độ sắc nét
    enhancer = ImageEnhance.Sharpness(doctor_resized)
    doctor_resized = enhancer.enhance(1.3)
    
    # Tạo ảnh kết quả từ background
    result = background.copy()
    
    # Tính khoảng cách thực tế
    spacing_x = int(spacing_ratio * cell_width)
    spacing_y = int(spacing_ratio * cell_height)
    
    # Tính vị trí bắt đầu để căn giữa lưới
    grid_total_width = cols * cell_width + (cols - 1) * spacing_x
    grid_total_height = rows * cell_height + (rows - 1) * spacing_y
    start_x = (bg_width - grid_total_width) // 2
    start_y = (bg_height - grid_total_height) // 2
    
    print(f"Kích thước background: {bg_width}x{bg_height}")
    print(f"Kích thước ô lưới: {cell_width}x{cell_height}")
    print(f"Kích thước ảnh doctor đã resize: {doctor_width}x{doctor_height}")
    print(f"Tỉ lệ sau resize: {doctor_width/doctor_height:.2f}")
    print(f"Khoảng cách: {spacing_x}x{spacing_y}")
    print(f"Vị trí bắt đầu lưới: ({start_x}, {start_y})")
    
    # Đặt các ảnh doctor lên background
    for row in range(rows):
        for col in range(cols):
            # Tính vị trí của ô lưới
            cell_x = start_x + col * (cell_width + spacing_x)
            cell_y = start_y + row * (cell_height + spacing_y)
            
            # Tính vị trí căn giữa ảnh doctor trong ô
            doctor_x = cell_x + (cell_width - doctor_width) // 2
            doctor_y = cell_y + (cell_height - doctor_height) // 2
            
            # Paste ảnh doctor lên background
            result.paste(doctor_resized, (doctor_x, doctor_y), doctor_resized)
    
    # Lưu ảnh kết quả
    result.save(out_path, "PNG")
    print(f"Đã lưu ảnh kết quả tại: {out_path}")
    
    return result

def create_custom_grid(rows=10, cols=15, spacing_ratio=0.1):
    """
    Hàm tiện ích để tạo lưới với tham số tùy chỉnh
    
    Args:
        rows: Số hàng
        cols: Số cột  
        spacing_ratio: Tỷ lệ khoảng cách (0.1 = thoáng vừa, 0.15 = thoáng hơn)
    """
    return create_doctor_grid(
        rows=rows,
        cols=cols, 
        spacing_ratio=spacing_ratio,
        output_path=f"doctor_grid_{rows}x{cols}_spacing{spacing_ratio:.2f}.png"
    )

def main():
    """Hàm chính để test"""
    print("Đang tạo lưới 5x5 ảnh doctor với tỉ lệ gốc được giữ nguyên...")
    
    # Tạo lưới 5x5 với tỉ lệ gốc được giữ nguyên
    result = create_doctor_grid_preserve_aspect(
        rows=5,
        cols=5,
        spacing_ratio=0.15,
        output_path="doctor_grid_5x5_aspect.png"
    )
    
    if result:
        print("Hoàn thành! Kiểm tra file doctor_grid_5x5_aspect.png")
        print(f"Kích thước ảnh kết quả: {result.size}")
    
    # Tạo thêm biến thể với khoảng cách khác
    print("\nTạo biến thể với khoảng cách lớn hơn...")
    create_doctor_grid_preserve_aspect(
        rows=5,
        cols=5,
        spacing_ratio=0.2,
        output_path="doctor_grid_5x5_wide_spacing.png"
    )
    
    print("\nTạo biến thể với ảnh doctor lớn hơn trong ô...")
    create_doctor_grid_preserve_aspect(
        rows=5,
        cols=5,
        spacing_ratio=0.1,
        max_size_ratio=0.9,
        output_path="doctor_grid_5x5_large_image.png"
    )

if __name__ == "__main__":
    main()
