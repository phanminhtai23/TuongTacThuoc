# Run with python command
import google.generativeai as genai
genai.configure(api_key="AIzaSyBEpar61waSy4B2vus5mJYrUmLUhwTlpsE")


from ultils.CRAFT import rotated_img_craft as CARFT
from ultils.SEG_YOLOv11 import detect_document_yolo11 as YOLO11
from ultils.Rotate_img_model import Rotate_image as ROTATE_IMAGE_CNN
from ultils.Rotate_img_model import Rotate_image as ROTATE_IMAGE

import subprocess
import sys
import os
import io
import cv2
from PIL import Image
import numpy as np
import image_to_text as img_to_text
from flask import Flask, request, jsonify
app = Flask(__name__)
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
    image_cv = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 500, 500)
    cv2.imshow(name, image_cv)

# image = Image.open(image_path)
# image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# image_cv = cv2.imread(image_path)
# image_pil = Image.fromarray(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB))

#CONFIG PATH
# test_img = "D:\Project\AI\OCR\images\\thuoc_nguoc_180.jpg"
# Init_image = Image.open(test_img)
# preview_img("Initial Image", Init_image)

# YOLO
Yolo_model_path = current_directory + '/func/SEG_YOLOv11/weights/last.pt'
Yolo_result_folder = current_directory + '/func/SEG_YOLOv11/results_img/'

# CRAFT
Craft_model_path = current_directory + '/func/CRAFT/weights/craft_mlt_25k.pth'
Craft_result_folder = current_directory + '/func/CRAFT/result_img/'

# CNN
CNN_model_path = current_directory + '/func/Rotate_img_model/orientation_model.h5'



#Load models
def load_model():
    YOLO11_MODEL = YOLO11.load_model_yolo11(Yolo_model_path)
    CARFT_MODEL = CARFT.load_model_CRAFT()
    CNN_MODEL = ROTATE_IMAGE.load_trained_model(CNN_model_path)
    GEMINI_MODEL = genai.GenerativeModel("gemini-1.5-flash")
    print("Load models successfully")
    return YOLO11_MODEL, CARFT_MODEL, CNN_MODEL, GEMINI_MODEL


YOLO11_MODEL, CARFT_MODEL, CNN_MODEL, GEMINI_MODEL = load_model()

# KEY API Gemini


# response = model.generate_content("Explain how AI works")
# print(response.text)

@app.route('/api', methods=['POST'])
def api():
    if request.method == 'POST':
        data = request.get_json()
        response = GEMINI_MODEL.generate_content(data['content'])
        return jsonify({"response": response.text})

# # Yolo nhận diện tài liệu
# detected_document_img = YOLO11.detect_document_yolo11(
#     YOLO11_MODEL, Init_image, showTime=True, isSaveResult=True, resultFolder=Yolo_result_folder)
# preview_img("detected_document_img", detected_document_img)

# #Craft để xoay ảnh
# rotated_image = CARFT.rotate_image_equal_craft(
#     detected_document_img, test_img, CARFT_MODEL)
# preview_img("Rotated Image", rotated_image)

# #CNN để lật ảnh nếu ngược
# orientatied_img = ROTATE_IMAGE.predict_and_correct_orientation(
#     CNN_MODEL, rotated_image)
# preview_img("Orientatied Image", orientatied_img)

# # Trích xuất text
# extracted_text = img_to_text.img_to_text(orientatied_img)
# print("message", extracted_text)

# API trả về data

# Lưu vào csdl

# cv2.waitKey(0)
# cv2.destroyAllWindows()


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="localhost")
    print("Server is running on {0}".format(5000))