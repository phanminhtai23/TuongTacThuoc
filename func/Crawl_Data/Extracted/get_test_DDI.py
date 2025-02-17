import requests
from bs4 import BeautifulSoup
import csv
import os
from icecream import ic

# Đường dẫn đầy đủ đến file CSV
csv_path = "./func/Crawl_Data/Data/Data_TuongTacThuoc.csv"
        
# URL của trang web bạn muốn cào dữ liệu
url = 'https://medica.wiki/tra-cuu-tuong-tac-thuoc/'

# Gửi yêu cầu HTTP GET đến URL
response = requests.get(url)

# Kiểm tra xem yêu cầu có thành công không
if response.status_code == 200:
    # Phân tích cú pháp HTML của trang web
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tìm thẻ <tbody> đầu tiên trong trang web
    tbody = soup.find('tbody')

    if tbody:
        # Tìm tất cả các thẻ <tr> trong thẻ <tbody>
        rows = tbody.find_all('tr')

        # Duyệt qua từng hàng và lấy dữ liệu
        for i, row in enumerate(rows, start=1):
            ic(i)
            # Tìm tất cả các thẻ <td> trong hàng
            cols = row.find_all('td')
            # Lấy nội dung văn bản của từng cột
            row_insert_csv = []
            for j, col in enumerate(cols):
                col_data = col.get_text().strip()
                col_data = col_data.replace('\n', ' ')
                row_insert_csv.append(col_data)
            # ic(row_insert_csv)
            # Ghi dữ liệu vào file CSV
            with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(row_insert_csv)
    else:
        print("No <tbody> found in the webpage")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    