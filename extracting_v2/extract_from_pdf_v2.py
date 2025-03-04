
# KEY API Gemini
import icecream as ic
import time as Time
from flask import Flask, request, jsonify
from PIL import Image
import os
import sys
from io import BytesIO
import google.generativeai as genai
import re
import json
import base64
import os
import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from unidecode import unidecode
import httpx


history_general = [
    {
        "role": "user",
        "parts": """
        Dữ liệu sau là file thông tin của một loại thuốc, có thể chứa thông tin về tương tác thuốc giữa hoạt chất với hoạt chất, Tương tác thuốc là hiện tượng xảy ra khi dùng phối hợp hai hay nhiều thuốc mà có sự thay đổi tác dụng của một hoặc nhiều thuốc dùng phối hợp. Đó có thể là sự tăng hoặc giảm tác dụng điều trị hoặc xuất hiện những tác dụng không mong muốn của thuốc. Hãy trích xuất dữ liệu theo các trường sau và trả về dưới dạng JSON:
        {
            TenThuoc (Tên thuốc, chính xác chỉ 1 tên thuốc, tên chính xác)
            HoatChat_1 (Hoạt chất 1, chính xác chỉ 1 chất, tên chính xác)
            HoatChat_2 (Hoạt chất 2, chính xác chỉ 1 chất, tên chính xác)
            LoaiTuongTac (Loại tương tác, Nếu không có thì để "Không xác định")
            MucDoNghiemTrong (Mức độ nghiêm trọng chỉ lưu các giá trị: Nghiêm trọng, Trung bình, Nhẹ, Không xác định)
            CanhBaoTuongTacThuoc (Cảnh báo tương tác thuốc chi tiết đầy đủ, nếu không có bạn có thể sử dụng kiến thức chính xác của ban được xác thực của bạn để điền vào, nội dung đảm bảo đầy đủ các thông tin cần thiết về tương tác thuốc đó)
        }
        Hãy trả lời lại dữ liệu trên trong cặp \{\} thôi nhé, không tìm thấy trường nào thì để nội dung trường đó là rỗng, nếu HoatChat_2 Không có hoặc không xác định thì bỏ qua, lưu khi có đủ 2 hoạt chất, các thông tin phải có đầy đủ tên thuốc, có cặp hoạt chất tương tác thì mới trả về dữ liệu json. Nếu thiếu dữ liệu về tên thuốc hoặc không có cặp hoạt chất tương tác thuốc nào thì không trả về gì cả, Sau đây là file pdf:
        """
    },
    {
        "role": "model",
        "parts": "ok, tôi sẽ vâng lời !"
    }
]
# Đường dẫn file log của Điển
log_file = open(
    "H:/My Drive/HK2-Nam4/Nien-Luan-Nganh/TuongTacThuoc/extracting_v2/log2.txt", "w", encoding="utf-8")

# đường dẫn file log đuôi .txt
file_path_logs = "H:/My Drive/HK2-Nam4/Nien-Luan-Nganh/TuongTacThuoc/extracting_v2/extracted_pdfs_logs_v2.txt"

# Đường dẫn đến file json
json_file_path = "H:/My Drive/HK2-Nam4/Nien-Luan-Nganh/TuongTacThuoc/extracting_v2/Thuoc1_DDI_v2.json"

# Khởi tạo API
global GEMINI_API_KEY_STUDENT, GEMINI_API_KEY_MINHTAI, GENERAL_API_KEY, GEMINI_MODEL


GEMINI_API_KEY_STUDENT = "AIzaSyASiMHE6d5tgL-cJ5vrdS0OHtopFPTauG0"
GEMINI_API_KEY_MINHTAI = "AIzaSyAbpBjvNKIetpsLLplmHeVPtFxoVaBY7EA"

GENERAL_API_KEY = GEMINI_API_KEY_MINHTAI

genai.configure(api_key=GENERAL_API_KEY)
GEMINI_MODEL = genai.GenerativeModel("gemini-2.0-flash")

# Đường dẫn file PDF cục bộ
# Thay bằng đường dẫn thật của bạn
# doc_path = "H:/My Drive/HK2-Nam4/Nien-Luan-Nganh/TuongTacThuoc/test/pdf/1556085312635_143(66).pdf"

# Cấu hình Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)


# Hàm ghi log
def log(message):
    log_file.write(message + "\n")
    log_file.flush()

# Hàm tải file PDF
# def download_pdf(pdf_url, filename):
#     try:
#         response = requests.get(pdf_url, stream=True)
#         response.raise_for_status()
#         with open(filename, "wb") as file:
#             for chunk in response.iter_content(chunk_size=8192):
#                 file.write(chunk)
#         log(f"Tải về thành công: {filename}")
#         print(f"Tải về thành công: {filename}")
#     except Exception as e:
#         log(f"Lỗi khi tải file {filename}: {e}")
#         print(f"Lỗi khi tải file {filename}: {e}")

# Hàm lấy tất cả các thuốc từ danh sách


def pdf_url_to_json_data(pdf_url, filename):
    try:
        # Generate content using the cached prompt and document
        chat = GEMINI_MODEL.start_chat(
            history=history_general
        )
        doc_data = base64.standard_b64encode(
            httpx.get(pdf_url).content).decode("utf-8")

        response = chat.send_message(
            [{'mime_type': 'application/pdf', 'data': doc_data}, ""])

        return response.text
    except Exception as e:
        return False


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


def writting_log(text, e):
    with open(file_path_logs, 'a', encoding='utf-8') as file:
        file.write(
            f"path: {text}\nError: {str(e)}\n_________________________________________________________________________________________________\n")

# 0 -> 255


count_pdf_had_DDI = 0


def scrape_drug_pdfs():
    page_number = 0
    drug_names = {}
    while True:
        try:
            url = f"https://drugbank.vn/danh-sach-thuoc?page={page_number}&size=20&sort=tenThuoc,asc"
            driver.get(url)
            time.sleep(2)

            # Lấy tất cả các nút "Xem"
            buttons = driver.find_elements(
                By.CSS_SELECTOR, "button.btn-info.btn-sm")
            if not buttons:
                break

            for index in range(len(buttons)):
                try:
                    log(f"Đang xử lý thuốc thứ {index + 1} trên trang {page_number}...")
                    # print(
                    #     f"Đang xử lý thuốc thứ {index + 1} trên trang {page_number}...")

                    # Re-locate the button to avoid stale element reference
                    buttons = driver.find_elements(
                        By.CSS_SELECTOR, "button.btn-info.btn-sm")
                    button = buttons[index]

                    # Cuộn đến nút để đảm bảo Selenium có thể nhấp vào
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", button)
                    button.click()
                    time.sleep(2)

                    # Lấy nội dung trang chi tiết
                    soup = BeautifulSoup(driver.page_source, "html.parser")

                    # Lấy tên thuốc
                    drug_name_tag = soup.find("h1")
                    drug_name = drug_name_tag.get_text(
                        strip=True) if drug_name_tag else f"Thuoc_{index + 1}"
                    drug_name = re.sub(
                        r"[^\w\s]", "", drug_name).replace(" ", "_")
                    # Chuyển tên thuốc thành không dấu
                    drug_name = unidecode(drug_name)

                    # Kiểm tra và xử lý tên thuốc trùng lặp
                    if drug_name in drug_names:
                        drug_names[drug_name] += 1
                        drug_name = f"{drug_name}_{drug_names[drug_name]}"
                    else:
                        drug_names[drug_name] = 0

                    log(f"Đang xử lý thuốc: {drug_name}")
                    # print(f"Đang xử lý thuốc: {drug_name}")

                    # Tìm thẻ iframe chứa file PDF
                    iframe_tag = soup.find(
                        "iframe", class_="embed-responsive-item")
                    if (iframe_tag and "src" in iframe_tag.attrs):
                        pdf_url = iframe_tag["src"]
                        if not pdf_url.startswith("http"):
                            pdf_url = "https://drugbank.vn" + pdf_url

                        response = pdf_url_to_json_data(pdf_url, drug_name)
                        # print("respone_data: ", response)
                        match = re.search(r'```json\n(.*?)\n```',
                                          response, re.DOTALL)
                        if match:
                            json_string = match.group(1)
                            json_object = json.loads(json_string)

                            save_json_data(json_object, json_file_path)

                            # print("json_object: ", json_object)
                            global count_pdf_had_DDI
                            count_pdf_had_DDI = count_pdf_had_DDI + 1
                            print(f"{drug_name} - {count_pdf_had_DDI}: ✔")
                        else:
                            print(
                                f"{drug_name}: ❌ Không tìm thấy cặp tương tác thuốc...")
                            writting_log(
                                drug_name, "Không tìm thấy cặp tương tác thuốc...")
                    else:
                        log(f"Không tìm thấy PDF cho thuốc {drug_name}")
                        # print(f"Không tìm thấy PDF cho thuốc {drug_name}")

                    driver.back()
                    time.sleep(1)

                except StaleElementReferenceException:
                    log(
                        f"Lỗi khi xử lý thuốc thứ {index + 1} trên trang {page_number}: Stale element reference")
                    # print(
                    #     f"Lỗi khi xử lý thuốc thứ {index + 1} trên trang {page_number}: Stale element reference")
                    driver.back()
                    time.sleep(1)
                except Exception as e:
                    log(f"Lỗi khi xử lý thuốc: {e}")
                    # print(f"Lỗi khi xử lý thuốc: {e}")
                    driver.back()
                    time.sleep(1)

            page_number += 1

        except Exception as e:
            log(f"Lỗi khi xử lý trang {page_number}: {e}")
            # print(f"Lỗi khi xử lý trang {page_number}: {e}")
            break


try:
    scrape_drug_pdfs()
finally:
    driver.quit()
    log_file.close()
