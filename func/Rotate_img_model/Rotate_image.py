import tensorflow as tf
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import time
from PIL import Image

# Load mô hình đã huấn luyện
def load_trained_model(model):
    return load_model(model)

# Hàm dự đoán hướng tài liệu và xoay ảnh nếu cần
def predict_and_correct_orientation(model, pil_img):
    t0 = time.time()
    print("Running CNN model...")
    # Load và tiền xử lý ảnh
    img = pil_img.resize((224, 224))
    # img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Thêm batch dimension
    img_array /= 255.0  # Chuẩn hóa dữ liệu

    # Dự đoán
    prediction = model.predict(img_array)
    orientation = "0°" if prediction[0][0] < 0.5 else "180°"

    print(f"Dự đoán hướng: {orientation}")

    # Nếu ảnh được dự đoán là 180°, xoay lại và lưu
    if orientation == "180°":
        image_cv = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        # img_cv = cv2.imread(img_path)
        if image_cv is not None:
            img_rotated = cv2.rotate(image_cv, cv2.ROTATE_180)  # Xoay 180 độ
            print(f"Ảnh đã xoay")
            t1 = time.time() - t0
            print("Done in: {:.2f}".format(t1))
            # pil_image = Image.fromarray(
            #     img_rotated)
            orientated_pil_image = Image.fromarray(
                cv2.cvtColor(img_rotated, cv2.COLOR_BGR2RGB))
            return orientated_pil_image
            # return img_rotated
        else:
            print("Done in: {:.2f}".format(t1))
            print(f"Không thể đọc ảnh")
    else:
        return pil_img
# # Hàm chính để thực thi
# def main():
#     model = load_trained_model("orientation_model.h5")
#     test_image_path = "images/test_model_2.jpg"# Thay bằng đường dẫn ảnh của bạn
#     result_dir = "result"
#     os.makedirs(result_dir, exist_ok=True)  # Tạo thư mục nếu chưa có

#     img_rotated = predict_and_correct_orientation(model, test_image_path)
#     output_path = os.path.join(result_dir, os.path.basename(test_image_path))  # Đường dẫn lưu ảnh
#     cv2.imwrite(output_path, img_rotated)

# if __name__ == "__main__":
#     main()