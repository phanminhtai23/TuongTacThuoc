import json
import requests
from icecream import ic
import csv

csv_path_hoatChat = "../Data/hoatChat.csv"

# Đọc dữ liệu hiện tại từ tệp JSON

# Lấy dữ liệu từ API và thêm vào danh sách`
for page in range(513):

    response = requests.get(
        f'https://drugbank.vn/services/drugbank/api/public/thuoc?page={page}&size=20&isHide=ne(Yes)&sort=soDangKy,asc&sort=id')
    if response.status_code == 200:
        data = response.json()

        # Duyệt qua từng loại thuốc trong mảng thuốc
        for drug in data:
            # ic(drug)
            arr_chatChat = drug['hoatChat'].split(";")
            for hoatChat in arr_chatChat:
                # ic(hoatChat, 1)
                hoatChat = hoatChat.strip()
                if hoatChat != "":
                    # ic(hoatChat)
                    with open(csv_path_hoatChat, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([hoatChat])
    ic("Đã cào xong trang: ", page)
    
ic("Đã cào xong !", )

