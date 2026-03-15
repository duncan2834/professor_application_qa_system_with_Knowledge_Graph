import os
from KG_builder.convert_pdf_to_text.core import extract_context_from_pdf
from KG_builder.extract.utils import get_main_subject 


def rename_pdfs_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            old_path = os.path.join(folder_path, filename)
            try:
                # 1. Lấy tên từ nội dung
                text = extract_context_from_pdf(pdf_path=old_path)
                new_name = get_main_subject(text, r"Họ và tên người đăng ký:\s*([^\n\r,.;]+)")
                
                if not new_name:
                    print(f"⚠️ Không tìm thấy tên trong: {filename}")
                    continue
                
                # 2. Xử lý trùng tên và đổi tên
                base_new_path = os.path.join(folder_path, f"{new_name}.pdf")
                final_new_path = base_new_path
                counter = 1
                
                # Vòng lặp thêm hậu tố nếu file đã tồn tại
                while os.path.exists(final_new_path):
                    final_new_path = os.path.join(folder_path, f"{new_name}_{counter}.pdf")
                    counter += 1
            except RuntimeError as e:
                # Bắt lỗi "No extractable text..." và bỏ qua file này
                if "Consider OCR" in str(e):
                    print(f"⏩ Bỏ qua (PDF Ảnh/Scan): {filename}")
                else:
                    print(f"❌ Lỗi Runtime khác: {e}")
            # 3. Thực hiện đổi tên
            try:
                os.rename(old_path, final_new_path)
                print(f"✅ Đã đổi: {filename} -> {os.path.basename(final_new_path)}")
            except Exception as e:
                print(f"❌ Lỗi đổi tên {filename}: {e}")
                
                
def rename_to_uppercase(folder_path):
    # Lấy danh sách tất cả file trong thư mục
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    for filename in files:
        # 1. Tách phần tên và phần mở rộng (ví dụ: .pdf, .docx)
        name_part, extension = os.path.splitext(filename)
        
        # 2. Chuyển phần tên sang VIẾT HOA và dọn dẹp khoảng trắng
        # Ví dụ: "Nguyen Van A" -> "NGUYEN VAN A"
        new_name_upper = name_part.strip().upper()
        
        # 3. Tạo đường dẫn cũ và mới
        old_path = os.path.join(folder_path, filename)
        new_filename = f"{new_name_upper}{extension}"
        new_path = os.path.join(folder_path, new_filename)
        
        # 4. Kiểm tra nếu tên mới khác tên cũ thì mới đổi
        if filename != new_filename:
            # Xử lý trường hợp trùng tên (nếu có)
            counter = 1
            while os.path.exists(new_path):
                new_path = os.path.join(folder_path, f"{new_name_upper}_{counter}{extension}")
                counter += 1
            
            try:
                os.rename(old_path, new_path)
                print(f"✅ Đã đổi: {filename} -> {os.path.basename(new_path)}")
            except Exception as e:
                print(f"❌ Lỗi khi đổi file {filename}: {e}")
                
if __name__ == "__main__":
    rename_to_uppercase("../table_data/")
        
