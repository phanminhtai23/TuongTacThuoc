import cv2
import numpy as np
import pytesseract
from PIL import Image

# Đường dẫn đến tesseract.exe nếu cần thiết
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# input: pil_img -> text
def img_to_text(pil_img, save=False):
    # pil_img.show()

    # PIL -> CV
    image_cv = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # Gray scale
    gray_image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Khi truyền path ảnh
    # gray = cv2.imread(path_to_img, cv2.IMREAD_GRAYSCALE)

    # Loại bỏ nhiễu
    # denoised = cv2.medianBlur(gray_image_cv, 3)
    # tăng nét
    # sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    # sharpened = cv2.filter2D(denoised, -1, sharpen_kernel)
    # chỉ tăng nét ok

    # CV -> PIL
    # image_pil = Image.fromarray(cv2.cvtColor(gray_image_cv, cv2.COLOR_BGR2RGB))
    # image_pil.show()

    # Sử dụng OCR để nhận diện chữ
    text1 = pytesseract.image_to_string(gray_image_cv, lang='vie')

    if save:
        with open("content.txt", "w", encoding="utf-8") as f:
            f.write(text1)
        print("Saved content to content.txt")

    return text1


# image_path = './images/cv.jpg'

# # Kiểm tra xem ảnh có bị ngược không
# text = img_to_text(image_path)
# print(text)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
