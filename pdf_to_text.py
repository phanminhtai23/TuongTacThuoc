import pytesseract
import os
import cv2
import numpy as np
import pdfplumber
from PIL import Image, ImageEnhance, ImageFilter
import re

# Đường dẫn đến tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# pdf to text


def pdf_to_text(file, file_name):
    images = []
    extracted_text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            pil_image = page.to_image(resolution=300).original
            images.append(pil_image)

            # Xử lý từng ảnh
        for index, img in enumerate(images):
            # img.show()
            # Chuyển ảnh sang dạng xám
            gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
            # Xử lý ảnh

            # Xử lý ảnh nhị phân
            # _, binary = cv2.threshold(
            #     gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            # loại bỏ nhiễu
            denoised = cv2.medianBlur(gray, 3)
            # Tăng nét
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            resized = cv2.resize(sharpened, None, fx=2, fy=2,
                                 interpolation=cv2.INTER_LINEAR)
            # Hiển thị ảnh đã resize với kích thước window hiển thị ảnh thành 500 x 500
            cv2.imwrite(f"test/pdf/{file_name}{index}.png", resized)
            # # CV -> PIL
            # image_pil = Image.fromarray(
            #     cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
            # image_pil.show()
            # OCR
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(
                resized, lang="vie", config=custom_config)
            extracted_text += f"\n--- {file_name} ---\n{text}"
        print(f"Extracted text from {file_name} Done.")
    return extracted_text
