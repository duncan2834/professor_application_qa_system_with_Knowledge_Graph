import re
import os

def get_main_subject(text: str, pattern: str):
    match = re.search(pattern, text)
    name = None
    if match:
        name = match.group(1).strip()
        print(f"Tên tìm được: '{name}'")
    return name

def normalize_name(filename):
    """
    Chuẩn hóa tên file: 
    - Bỏ đuôi file (.pdf, .json)
    - Chuyển thành viết hoa
    - Loại bỏ hậu tố số ở cuối (ví dụ _1, _2)
    - Thay thế dấu gạch dưới bằng khoảng trắng để so sánh chính xác hơn
    """
    # 1. Lấy tên file bỏ phần mở rộng
    name = os.path.splitext(filename)[0]
    
    # 2. Viết hoa toàn bộ
    name = name.upper()
    
    # 3. Loại bỏ hậu tố số ở cuối như _1, _2, -1...
    name = re.sub(r'[\s_-]+\d+$', '', name)
    
    # 4. Thay thế gạch dưới bằng khoảng trắng và trim
    name = name.replace('_', ' ').strip()
    
    return name

def check_file_exists_in_json_folder(pdf_filename, json_folder_path):
    """
    Kiểm tra xem file PDF có file JSON tương ứng trong folder table_data không.
    """
    # Chuẩn hóa tên PDF đang xét
    target_name = normalize_name(pdf_filename)
    
    # Duyệt qua các file trong thư mục JSON
    for json_file in os.listdir(json_folder_path):
        if json_file.lower().endswith('.json'):
            json_name = normalize_name(json_file)
            
            # So sánh sau khi đã chuẩn hóa
            if target_name == json_name:
                return json_file # Trả về True và tên file JSON tìm thấy
                
    return None