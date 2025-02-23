# KEY API Gemini
import time as Time
from flask import Flask, request, jsonify
import pdf_to_text as pdf_to_text
import image_to_text as img_to_text
from PIL import Image
import os
import sys
from func.Rotate_img_model import Rotate_image as ROTATE_IMAGE_CNN
from func.SEG_YOLOv11 import detect_document_yolo11 as YOLO11
from func.CRAFT import rotated_img_craft as CARFT
from io import BytesIO
import google.generativeai as genai
genai.configure(api_key="AIzaSyASiMHE6d5tgL-cJ5vrdS0OHtopFPTauG0")


# import subprocess
# import io
# import cv2
# import numpy as np

# libs sever
app = Flask(__name__)
# import requests
# import io


# Get the directory path of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
# print("Current directory:", current_directory)

sys.path.append(os.path.abspath(
    current_directory + '/func/CRAFT'))

sys.path.append(os.path.abspath(
    current_directory + '/func/SEG_YOLOv11'))
sys.path.append(os.path.abspath(
    current_directory + '/func/Rotate_img_model'))


def preview_img(name, pil_image):

    # image_cv = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    # cv2.resizeWindow(name, 500, 500)
    # cv2.imshow(name, image_cv)
    pil_image.show()


# image = Image.open(image_path)
# image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# image_cv = cv2.imread(image_path)
# image_pil = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))


# CONFIG PATH
test_img = "D:\Project\AI\OCR\images\cv_nghieng_phai_45.jpg"
Init_image = Image.open(test_img)
# preview_img("Initial Image", Init_image)

# YOLO
Yolo_model_path = current_directory + '/func/SEG_YOLOv11/weights/last.pt'
Yolo_result_folder = current_directory + '/func/SEG_YOLOv11/results_img/'

# CRAFT
Craft_model_path = current_directory + '/func/CRAFT/craft_mlt_25k.pth'
Craft_result_folder = current_directory + '/func/CRAFT/result_img/'

# CNN
CNN_model_path = current_directory + '/func/Rotate_img_model/orientation_model.h5'
CNN_result_folder = current_directory + '/func/Rotate_img_model/result/'

# Load models


def load_model():
    t0 = Time.time()
    YOLO11_MODEL = YOLO11.load_model_yolo11(Yolo_model_path)
    CARFT_MODEL = CARFT.load_model_CRAFT(Craft_model_path)
    CNN_MODEL = ROTATE_IMAGE_CNN.load_trained_model(CNN_model_path)
    GEMINI_MODEL = genai.GenerativeModel("gemini-1.5-flash")
    print("Load models successfully in {:.2f} seconds".format(
        Time.time() - t0))
    return YOLO11_MODEL, CARFT_MODEL, CNN_MODEL, GEMINI_MODEL


YOLO11_MODEL, CARFT_MODEL, CNN_MODEL, GEMINI_MODEL = load_model()


# # Yolo nhận diện tài liệu
# detected_document_img = YOLO11.detect_document_yolo11(
#     YOLO11_MODEL, Init_image, showTime=True, isSaveResult=False, resultFolder=Yolo_result_folder)
# preview_img("detected_document_img", detected_document_img)

# #Craft để xoay ảnh
# rotated_image = CARFT.rotate_image_equal_craft(
#     pil_image=detected_document_img, image_path=test_img, model=CARFT_MODEL, save_result_img=True, result_folder=Craft_result_folder)
# preview_img("Rotated Image", rotated_image)

# #CNN để lật ảnh nếu ngược
# orientatied_img = ROTATE_IMAGE.predict_and_correct_orientation(
#     CNN_MODEL, rotated_image)
# preview_img("Orientatied Image", orientatied_img)

# # Trích xuất text
# extracted_text = img_to_text.img_to_text(orientatied_img, save=True)

# API trả về data

# Lưu vào csdl

# cv2.waitKey(0)
# cv2.destroyAllWindows()

history_general = [
    {"role": "user", "parts": """
        Đoạn văn bản sau là mô tả của một loại thuốc, hãy trích xuất dữ liệu trong đoạn sau thành dữ liệu json và trích theo các trường như sau và trả về như sau:
    {
        TenThuoc(tên đầy đủ của thuốc)
        DangBaoChe (dạng bào chế của thuốc)
        CacThanhPhan [
        {
        ThanhPhan(thành phần thuốc 1): ...,
        HamLuong (Hàm lượng của thuốc 1): ...
        }, 
        {
        ThanhPhan(thành phần thuốc 2): ...,
        HamLuong (Hàm lượng của thuốc 2): ...
        }, 
        {
        ThanhPhan(thành phần thuốc 3): ...,
        HamLuong (Hàm lượng của thuốc 3): ...
        },
        {
        ...  
        },
        {
        ThanhPhan(thành phần thuốc n): ...,
        HamLuong (Hàm lượng của thuốc n): ...
        }
        ] (là thành phần của thuốc và hàm lượng, khối lượng hoặc nồng độ của từng thành phần thuốc trong công thức thuốc)
        CachDongGoi (Cách đóng gói)
        ChiDinh (chỉ định, dành cho ai)
        ChongChiDinh (chống chỉ định)
        CachDung (cách dùng)
        HanSuDung (hạn sử dụng)
        TieuChuanChatLuong (tiêu chuẩn chất lượng của thuốc)
        DieuKienBaoQuan (điều kiện bảo quản của thuốc)
        KhuyenCao (khuyến cáo hay lưu ý của thuốc)
        CoSoSanXuatThuoc (là cơ sở sản xuất thuốc chứa object sau) {
            TenCoSoSanXuatThuoc(Tên cơ sở sản xuất thuốc): ,
            DiaChiCoSoSanXuatThuoc (Đại chỉ cơ sở sản xuất thuốc): 
        }
        TuongTacThuoc (là phần tương tác thuốc) [
        {
            ThanhPhanTuongTac (thành phần trong thuốc hiện tại bị tương tác): ,
            TenThuocTuongTac (tên loại thuốc mà tương tác với thành phần thuốc trên): ,
            HauQua (hậu quả khi xảy ra khi 2 thành thuốc trên tương tác):
        },
        {
            TenThuocTuongTac (tên loại thuốc mà thuốc hiện tại tương tác): ,
            HauQua (hậu quả khi xảy ra khi thuốc hiện tại tương tác thuốc này):
        },
        ...
        ]
    }
        XuatSuThuoc (Xuất sứ của thuốc)
        Hãy trả lời lại dữ liệu trên trong cặp \{\} thôi nhé, không tìm thấy trường nào thì để nội dung trường đó là rỗng, sau đây là đoạn văn bản đó:
     """},
    {"role": "model", "parts": "ok, tôi sẽ vâng lời !"}
]


def text_to_json_data(contents_text):
    GEMINI_MODEL = genai.GenerativeModel("gemini-1.5-flash")
    chat = GEMINI_MODEL.start_chat(history=history_general)
    response = chat.send_message(contents_text)
    return response.text


@app.route('/api/image', methods=['POST'])
def get_data_from_images():
    print("Đang trích dữ liệu từ images...")

    contents_text = ""
    if request.method == 'POST':
        try:
            # get
            images = request.files.getlist('images')

            for img in images:
                # Đọc dữ liệu ảnh từ tệp tin
                img_bytes = img.read()
                # Chuyển đổi từ bytes sang PIL image
                img_bytes = Image.open(BytesIO(img_bytes))

                # img_bytes.show()

                # processing image
                detected_document_img = YOLO11.detect_document_yolo11(
                    YOLO11_MODEL, img_bytes, showTime=True, isSaveResult=True, resultFolder=Yolo_result_folder)

                # detected_document_img.show("detected_document_img")

                # Craft để xoay ảnh
                rotated_image = CARFT.rotate_image_equal_craft(
                    pil_image=detected_document_img, image_path=test_img, model=CARFT_MODEL, save_result_img=True, result_folder=Craft_result_folder)

                # rotated_image.show("Craft để xoay ảnh")

                # CNN để lật ảnh nếu ngược
                orientatied_img = ROTATE_IMAGE_CNN.predict_and_correct_orientation(
                    CNN_MODEL, rotated_image, is_save_result=True, result_folder=CNN_model_path)

                # orientatied_img.show("CNN để lật ảnh nếu ngược")

                # Trích xuất text
                extracted_text = img_to_text.img_to_text(
                    orientatied_img, save=True)
                contents_text = contents_text + extracted_text

            # print("contents_text: ", contents_text)

            json_data = text_to_json_data(contents_text)
            # print("contents_text: ", contents_text)
            # print("ok xuong server, repson của gemini:\n", response.text)
            return jsonify({"contents": json_data}), 200
        except Exception as e:
            print(f"Error to process image: {e}")
            return jsonify({"response": "Error"}), 400


@app.route('/api/pdf', methods=['POST'])
def get_data_from_pdf():
    print("Đang trích dữ liệu từ dpf...")

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.pdf'):
        text = pdf_to_text.pdf_to_text(file, file.filename)
        if text != "":
            json_data = text_to_json_data(text)

            print("trích thành công !")
            return jsonify({"contents": json_data}), 200

        else:
            print("Không tìm thấy dữ liệu !")
            return jsonify({"error": "No text extracted"}), 400
    else:
        return jsonify({"error": "Invalid file type"}), 400


if __name__ == '__main__':
    print("Server is running on http://{0}:{1}".format("localhost", 5000))
    app.run(debug=True, port=5000, host="localhost")
