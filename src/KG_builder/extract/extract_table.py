import os
import json
import time

from KG_builder.convert_pdf_to_text.extract_table import extract_table_from_pdf
from KG_builder.extract.utils import check_file_exists_in_json_folder
from KG_builder.llm.base.base_model import BaseLLM
from KG_builder.utils.llm_utils import load_model

# TODO: làm regex để trích ra họ tên.


if __name__ == "__main__":
    # loop qua các pdf, đổi tên
    folder_path = "../pdf_data/"
    json_folder_path = "../table_data/"
    llm = load_model("gemini-2.5-flash")
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            if not check_file_exists_in_json_folder(pdf_filename=filename, json_folder_path=json_folder_path):
                table_data = extract_table_from_pdf(pdf_path=pdf_path, genai=llm)
                print(f"Đã trích xuất xong bảng từ file {pdf_path}")
                parsed_data = json.loads(table_data)
                
                name = os.path.splitext(filename)[0]
                table_data_path = f"../table_data/{name}.json"
                
                os.makedirs(os.path.dirname(table_data_path), exist_ok=True)
                with open(table_data_path, 'w', encoding='utf-8') as f:
                    json.dump(parsed_data, f, ensure_ascii=False, indent=4)
                print(f"{filename}")
                
                time.sleep(10)