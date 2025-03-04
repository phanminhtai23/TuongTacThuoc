# KEY API Gemini
import icecream as ic
import time as Time
from flask import Flask, request, jsonify
import pdf_to_text as pdf_to_text
import image_to_text as img_to_text
from PIL import Image
import os
import sys
from io import BytesIO
import google.generativeai as genai
import re
import json

history_general = [
    {
        "role": "user",
        "parts": """
        Dữ liệu sau là thông tin về tương tác thuốc giửa hoạt chất với hoạt chất, hãy trích xuất dữ liệu theo các trường sau và trả về dưới dạng JSON:
        {
            TenThuoc (Tên thuốc, chính xác chỉ 1 tên thuốc, tên chính xác)
            HoatChat_1 (Hoạt chất 1, chính xác chỉ 1 chất, tên chính xác)
            HoatChat_2 (Hoạt chất 2, chính xác chỉ 1 chất, tên chính xác)
            LoaiTuongTac (Loại tương tác, Nếu không có thì để "Không xác định")
            MucDoNghiemTrong (Mức độ nghiêm trọng chỉ lưu các giá trị: Nghiêm trọng, Trung bình, Nhẹ, Không xác định)
            CanhBaoTuongTacThuoc (Cảnh báo tương tác thuốc chi tiết đầy đủ, nếu không có bạn có thể sử dụng kiến thức chính xác của ban được xác thực của bạn để điền vào, nội dung đảm bảo đầy đủ các thông tin cần thiết về tương tác thuốc đó)
        }
        Hãy trả lời lại dữ liệu trên trong cặp \{\} thôi nhé, không tìm thấy trường nào thì để nội dung trường đó là rỗng, nếu HoatChat_2 Không có hoặc không xác định th bỏ qua không cần lưu vào cơ sở dữ liệu, lưu khi có đủ 2 hoạt chất, các thông tin phải có đầy đủ mới lưu vào cở dữ liệu. Sau đây là dữ liệu:
        """
    },
    {
        "role": "model",
        "parts": "ok, tôi sẽ vâng lời !"
    }
]
# đường dẫn folder chứa các file pdfs
pdfs_folder_path = "H:\\My Drive\\HK2-Nam4\\Nien-Luan-Nganh\\TuongTacThuoc\\func\\Crawl_Data\\Data\\Thuoc2"

# đường dẫn file log đuôi .txt
txt_file_path = "H:\\My Drive\\HK2-Nam4\\Nien-Luan-Nganh\\TuongTacThuoc\\extracted_pdfs_logs.txt"

# Đường dẫn đến file json
json_file_path = "H:\\My Drive\\HK2-Nam4\\Nien-Luan-Nganh\\TuongTacThuoc\\Thuoc2_DDI.json"

# Khởi tạo API
global GEMINI_API_KEY_STUDENT, GEMINI_API_KEY_MINHTAI, GENERAL_API_KEY, GEMINI_MODEL

GEMINI_API_KEY_STUDENT = "AIzaSyASiMHE6d5tgL-cJ5vrdS0OHtopFPTauG0"
GEMINI_API_KEY_MINHTAI = "AIzaSyAbpBjvNKIetpsLLplmHeVPtFxoVaBY7EA"

GENERAL_API_KEY = GEMINI_API_KEY_MINHTAI

genai.configure(api_key=GENERAL_API_KEY)
GEMINI_MODEL = genai.GenerativeModel("gemini-1.5-flash")


def swap_api_key():
    global GENERAL_API_KEY
    if GENERAL_API_KEY == GEMINI_API_KEY_STUDENT:
        GENERAL_API_KEY = GEMINI_API_KEY_MINHTAI
    else:
        GENERAL_API_KEY = GEMINI_API_KEY_STUDENT
    genai.configure(api_key=GENERAL_API_KEY)
    global GEMINI_MODEL
    GEMINI_MODEL = genai.GenerativeModel("gemini-1.5-flash")


def text_to_json_data(contents_text):
    chat = GEMINI_MODEL.start_chat(history=history_general)
    response = chat.send_message(contents_text)
    return response.text


def writting_log(text, e):
    with open(txt_file_path, 'a', encoding='utf-8') as file:
        file.write(
            f"path: {text}\nError: {str(e)}\n_________________________________________________________________________________________________\n")


def save_json_data(json_data, json_file_path):
    try:
        with open(json_file_path, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                data.append(json_data)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump([json_data], file, ensure_ascii=False, indent=4)


index = 2513

count = 0
for root, dirs, files in os.walk(pdfs_folder_path):
    for file in files:
        try:
            count += 1
            if count <= index:
                continue
            pdf_path = os.path.join(root, file)
            text = pdf_to_text.pdf_to_text(pdf_path, file)

            respone_data = text_to_json_data(text)
            # print("respone_data: ", respone_data)
            match = re.search(r'```json\n(.*?)\n```',
                              respone_data, re.DOTALL)
            if match:
                json_string = match.group(1)
                json_object = json.loads(json_string)
                save_json_data(json_object, json_file_path)
                # print("json_object: ", json_object)
                print(f"{file} - {count}: ✔")
            else:
                print(f"{file} - {count}: ❌ No JSON found in response")
                writting_log(pdf_path, "No JSON found in response")

        except Exception as e:
            if str(e) == "429 Resource has been exhausted (e.g. check quota).":
                print("limited api key, swap to another key...")

                swap_api_key()
                try:

                    respone_data = text_to_json_data(text)
                    match = re.search(r'```json\n(.*?)\n```',
                                      respone_data, re.DOTALL)
                    if match:
                        json_string = match.group(1)
                        json_object = json.loads(json_string)
                        save_json_data(json_object, json_file_path)
                        # print("json_object: ", json_object)
                        print(f"{file} - {count}: ✔")
                    else:
                        print(f"{file} - {count}: ❌ No JSON found in response")
                        writting_log(pdf_path, "No JSON found in response")
                except Exception as e:
                    print(
                        f"{file} - {count}: ❌")
                    writting_log(pdf_path, e)
                    continue
            else:
                print(
                    f"{file} - {count}: ❌")
                writting_log(pdf_path, e)
                continue
