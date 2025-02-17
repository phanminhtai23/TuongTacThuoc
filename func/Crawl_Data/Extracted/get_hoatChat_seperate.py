import json
import csv

csv_path = "../Data/hoatChat1.csv"

# Đọc tệp JSON
with open('../Data/drugs.json', 'r', encoding='utf-8') as file:
    drugs = json.load(file)

hoatChats = []

# Duyệt qua từng đối tượng trong danh sách
for drug in drugs:
    # tách bằng ;
    if len(drug['hoatChat'].split(',')) < len(drug['hoatChat'].split(';')):
        for chat in drug['hoatChat'].split(';'):
            chat = chat.strip()
            if chat != '':
                if chat not in hoatChats:
                    hoatChats.append(chat)
    else:  # tách bằng ,
        for chat in drug['hoatChat'].split(','):
            chat = chat.strip()
            if chat != '':
                if chat not in hoatChats:
                    hoatChats.append(chat)
                
print("Tổng số hoạt chất đã xử lý: ", len(hoatChats))
# print("Tổng số hoạt chất đã xử lý: ", hoatChats)
                
# Ghi mỗi hoatChat vào một hàng mới trong cột đầu tiên của tệp CSV
with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for hoatChat in hoatChats:
        writer.writerow([hoatChat])
