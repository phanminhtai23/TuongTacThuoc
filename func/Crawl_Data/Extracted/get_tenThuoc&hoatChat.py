import json
import requests
from icecream import ic
import csv

csv_path_hoatChat = "../Data//thuoc&hoatChat.json"
ten_thuocs = []
drugs_result = []

def convert_medicine_data(drug):
    # Tách hoạt chất và hàm lượng
    hoat_chat_names = drug.get("hoatChat", "").split(" ; ")
    hoat_chat_dosages = drug.get("nongDo", "").split("; ")

    # Đảm bảo số lượng hoạt chất và hàm lượng tương ứng
    hoat_chat_list = []
    for i in range(len(hoat_chat_names)):
        hoat_chat_list.append({
            "tenHoatChat": hoat_chat_names[i].strip(),
            "nongDo": hoat_chat_dosages[i].strip() if i < len(hoat_chat_dosages) else "Không rõ"
        })

    # Thay thế trường hoatChat bằng danh sách mới
    drug["hoatChat"] = hoat_chat_list

    # Xóa các trường cũ không còn cần thiết
    del drug["nongDo"]

    return drug

# Lấy dữ liệu từ API và thêm vào danh sách`
for page in range(513):

    response = requests.get(
        f'https://drugbank.vn/services/drugbank/api/public/thuoc?page={page}&size=20&isHide=ne(Yes)&sort=soDangKy,asc&sort=id')
    if response.status_code == 200:
        twenty_pages_drugs = response.json()

        # Duyệt qua từng loại thuốc trong mảng thuốc
        for drug in twenty_pages_drugs:
            # ic(drug)
            
            tenThuoc = drug['tenThuoc']
            if tenThuoc not in ten_thuocs:
                ten_thuocs.append(tenThuoc)
                drug = convert_medicine_data(drug)
                drugs_result.append(drug)
                # print(drug)

    ic("Đã cào xong trang: ", page)

# Ghi dữ liệu vào file CSV
with open(csv_path_hoatChat, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Ghi dữ liệu thuốc dưới dạng JSON
    json.dump(drugs_result, file, ensure_ascii=False, indent=4)

print("Tổng số thuốc đã xử lý: ", len(ten_thuocs))
print("Đã ghi dữ liệu vào file JSON !")

