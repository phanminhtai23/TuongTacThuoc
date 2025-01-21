import requests
from bs4 import BeautifulSoup
import csv
import os
from icecream import ic

# Đường dẫn đầy đủ đến file CSV
csv_path = "./func/Crawl_Data/Data/Data_TuongTacThuoc.csv"

# Tạo file CSV và ghi đè lên tiêu đề các cột
with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
    file.truncate()
    writer = csv.writer(file)
    writer.writerow(['STT', 'Hoạt chất 1', 'Hoạt chất 2',
                    'Cơ chế', 'Hậu quả', 'Xử trí'])

# Kiểm tra xem hàng đã được chèn vào file CSV chưa
with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)