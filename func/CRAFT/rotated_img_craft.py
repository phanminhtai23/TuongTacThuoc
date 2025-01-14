"""
Copyright (c) 2019-present NAVER Corp.
MIT License
"""

# -*- coding: utf-8 -*-
from collections import OrderedDict
import sys
import os
import time
import argparse

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable

from PIL import Image

# Add the CRAFT directory to the Python path
current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(current_directory))

import cv2
from skimage import io
import numpy as np
import craft_utils
import imgproc
import file_utils
import json
import zipfile

from craft import CRAFT



sys.stdout.reconfigure(encoding='utf-8')


def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict


def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")

# parser = argparse.ArgumentParser(description='CRAFT Text Detection')
# parser.add_argument('--trained_model', default='weights/craft_mlt_25k.pth', type=str, help='pretrained model')
# parser.add_argument('--text_threshold', default=0.7, type=float, help='text confidence threshold')
# parser.add_argument('--low_text', default=0.4, type=float, help='text low-bound score')
# parser.add_argument('--link_threshold', default=0.4, type=float, help='link confidence threshold')
# parser.add_argument('--cuda', default=True, type=str2bool, help='Use cuda for inference')
# parser.add_argument('--canvas_size', default=1280, type=int, help='image size for inference')
# parser.add_argument('--mag_ratio', default=1.5, type=float, help='image magnification ratio')
# parser.add_argument('--poly', default=False, action='store_true', help='enable polygon type')
# parser.add_argument('--show_time', default=False, action='store_true', help='show processing time')
# parser.add_argument('--test_folder', default='/data/', type=str, help='folder path to input images')
# parser.add_argument('--refine', default=False, action='store_true', help='enable link refiner')
# parser.add_argument('--refiner_model', default='weights/craft_refiner_CTW1500.pth', type=str, help='pretrained refiner model')

# args = parser.parse_args()


current_directory = os.path.dirname(os.path.abspath(__file__))
# Định nghĩa các biến trực tiếp trong mã nguồn
trained_model = current_directory + '/craft_mlt_25k.pth'
test_folder = 'images'
img_save_folder = 'images'
refiner_model = 'weights/craft_refiner_CTW1500.pth'
is_save_mask = True
is_save_boxes = True
show_time_process = True

text_threshold = 0.7
low_text = 0.4
link_threshold = 0.4
use_cuda = False
canvas_size = 1280
mag_ratio = 1.5
poly = False
show_time = False
refine = False


""" For test images in a folder """

result_folder = './func/CRAFT/result_img/'
if not os.path.isdir(result_folder):
    os.mkdir(result_folder)


def test_net(net, image, text_threshold, link_threshold, low_text, cuda, poly, refine_net=None):
    t0 = time.time()

    # resize
    img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(
        image, canvas_size, interpolation=cv2.INTER_LINEAR, mag_ratio=mag_ratio)
    ratio_h = ratio_w = 1 / target_ratio

    # preprocessing
    x = imgproc.normalizeMeanVariance(img_resized)
    x = torch.from_numpy(x).permute(2, 0, 1)    # [h, w, c] to [c, h, w]
    x = Variable(x.unsqueeze(0))                # [c, h, w] to [b, c, h, w]
    if cuda:
        x = x.cuda()

    # forward pass
    with torch.no_grad():
        y, feature = net(x)

    # make score and link map
    score_text = y[0, :, :, 0].cpu().data.numpy()
    score_link = y[0, :, :, 1].cpu().data.numpy()

    # refine link
    if refine_net is not None:
        with torch.no_grad():
            y_refiner = refine_net(y, feature)
        score_link = y_refiner[0, :, :, 0].cpu().data.numpy()

    t0 = time.time() - t0
    t1 = time.time()

    # Post-processing
    boxes, polys = craft_utils.getDetBoxes(
        score_text, score_link, text_threshold, link_threshold, low_text, poly)

    # coordinate adjustment
    boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
    polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)
    for k in range(len(polys)):
        if polys[k] is None:
            polys[k] = boxes[k]

    t1 = time.time() - t1

    # render results (optional)
    render_img = score_text.copy()
    render_img = np.hstack((render_img, score_link))
    ret_score_text = imgproc.cvt2HeatmapImg(render_img)

    if show_time:
        print("\ninfer/postproc time : {:.3f}/{:.3f}".format(t0, t1))

    return boxes, polys, ret_score_text


def find_longest_ratio_box(bboxes):
    max_ratio = 0
    longest_ratio_box = None

    for box in bboxes:
        # Tính chiều dài và chiều rộng của hộp
        width = np.linalg.norm(box[0] - box[3])
        height = np.linalg.norm(box[0] - box[1])

        # Tính tỷ lệ dài
        ratio = max(width, height) / min(width, height)

        # Kiểm tra nếu tỷ lệ này là lớn nhất
        if ratio > max_ratio:
            max_ratio = ratio
            longest_ratio_box = box

    return longest_ratio_box, max_ratio


def get_horizontal_vector(image):
    h, w = image.shape[:2]
    # Tọa độ của hai điểm nằm trên trục ngang giữa bức ảnh
    point1 = np.array([0, h // 2])
    point2 = np.array([w, h // 2])
    # Tạo vector từ hai điểm này
    horizontal_vector = point2 - point1
    return horizontal_vector


# Hàm tính góc xoay cần thiết
def calculate_rotation_angle(box, img):
    # Tính vector của cạnh dài nhất
    edge1 = box[1] - box[0]
    edge2 = box[2] - box[1]
    if np.linalg.norm(edge1) > np.linalg.norm(edge2):
        longest_edge = edge1
    else:
        longest_edge = edge2

    # Tính góc giữa cạnh dài nhất và trục x
    angle = np.arctan2(longest_edge[1], longest_edge[0])
    # print("Góc giữa cạnh dài nhất và trục x:", np.degrees(angle))
    return np.degrees(angle)

# Hàm xoay ảnh


def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated


def load_model_CRAFT(Craft_model_path):
    # load net
    net = CRAFT()
    t_load_cuda = time.time()
    # print('Loading weights from checkpoint (' + trained_model + ')')
    if use_cuda:
        net.load_state_dict(copyStateDict(torch.load(Craft_model_path)))
        # print("Load CAFT model sucessfully in {:3.f}".format(time.time() - t_load_cuda))
    else:
        net.load_state_dict(copyStateDict(
            torch.load(Craft_model_path, map_location='cpu')))
        # print("Load CAFT model sucessfully in {:3.f}".format(
        #     time.time() - t_load_cuda))

    if use_cuda:
        net = net.cuda()
        net = torch.nn.DataParallel(net)
        cudnn.benchmark = False
    return net


def preview_img(name, image):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 500, 500)
    cv2.imshow(name, image)


def draw_box_on_img(box, img):
    if box is not None:
        pts = box.reshape((-1, 1, 2)).astype(np.int32)
        cv2.polylines(img, [pts], isClosed=True,
                      color=(0, 255, 0), thickness=2)
    return img


def rotate_image_equal_craft(pil_image, image_path, model, save_result_img=False, result_folder = result_folder):
    t0 = time.time()
    print("Running CRAFT model...")
    model.eval()
    # LinkRefiner
    refine_net = None
    poly = False
    if refine:
        from refinenet import RefineNet
        refine_net = RefineNet()
        # print('Loading weights of refiner from checkpoint (' + refiner_model + ')')
        if use_cuda:
            refine_net.load_state_dict(
                copyStateDict(torch.load(refiner_model)))
            refine_net = refine_net.cuda()
            refine_net = torch.nn.DataParallel(refine_net)
        else:
            refine_net.load_state_dict(copyStateDict(
                torch.load(refiner_model, map_location='cpu')))

        refine_net.eval()
        poly = True

    # print("Test image {:d}/{:d}: {:s}".format(k+1, len(image_list), image_path), end='\r')
    image = imgproc.loadImage(pil_image)

    
    bboxes, polys, score_text = test_net(
        model, image, text_threshold, link_threshold, low_text, use_cuda, poly, refine_net)
    # _________________________
    # print("box:", bboxes)
    # Lấy box có radio dài nhất
    longest_ratio_box, max_ratio = find_longest_ratio_box(bboxes)
    # print("Hộp có tỷ lệ dài nhất:", longest_ratio_box)
    # print("Tỷ lệ dài nhất:", max_ratio)

    # ảnh xoay
    # iamge_ne = cv2.imread(image_path)
    init_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    # init_image = pil_image
    # Tính góc xoay cần thiết
    angle = calculate_rotation_angle(longest_ratio_box, init_image)

    # # Vẽ box dài nhất và hiển thị ảnh
    # init_image = draw_box_on_img(longest_ratio_box, init_image)
    # preview_img("draw box Image", init_image)

    # Xoay ảnh
    rotated_image = rotate_image(init_image, angle)
    # _________________________

    # save score text
    if is_save_mask:
        filename, file_ext = os.path.splitext(os.path.basename(image_path))
        mask_file = result_folder + "/res_" + filename + '_mask.jpg'
        cv2.imwrite(mask_file, score_text)
        print("Mask on img saved to", result_folder)

        # save boxes lên ảnh
    if is_save_boxes:
        file_utils.saveResult(
            image_path, image[:, :, ::-1], polys, dirname=result_folder)
        print("Boxes on img saved to", result_folder)

    if show_time_process:
        t1 = time.time() - t0
        print("Craft done in: {:0.3f}".format(t1))
       
    rotated_pil_image = Image.fromarray(cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB))
    if save_result_img:
        cv2.imwrite(result_folder + "result_img_with_craft.jpg", rotated_image)
        print("Rotated image saved to", result_folder)
    
    return rotated_pil_image

# if __name__ == '__main__':

#     caft_model = load_model_CRAFT()  # initialize

#     img_path = 'D:/Project/AI/OCR/images/hoadon_xoay.jpg'
#     initial_img = cv2.imread(img_path)
#     preview_img("Initial Image", initial_img)

#     rotated_img = rotate_image_equal_craft(img_path, caft_model)
#     preview_img("Rotated Image", rotated_img)

#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
