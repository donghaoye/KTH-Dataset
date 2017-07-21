# -*- coding: UTF-8 -*-
import os
import sys
import shutil
import numpy as np
import cv2


'''
将real image 和 skeleton image合并到同一张图
'''


def file_copy(src, dst):
    try:
        shutil.copy(src, dst)
    except:
        error_flag = True

# 取得目录下面的文件列表
def get_dir_img_list(dir_proc, recusive=True):
    file_list = []
    for file in os.listdir(dir_proc):
        if os.path.isdir(os.path.join(dir_proc, file)):
            if (recusive):
                file_list.append(get_dir_img_list(os.path.join(dir_proc, file), recusive))
            continue
        img = dir_proc + "/" + file
        file_list.append(img)
    return file_list

def sum_zero_one_img(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    return sum(sum(img))

def get_maxpix_img(img_fold):
    img_list = get_dir_img_list(img_fold)
    dict = {}
    for path in img_list:
        sum_pix = sum_zero_one_img(path)
        dict[sum_pix] = path

    max_pix = max(dict.keys())
    return dict[max_pix].replace("_skeleton", "").replace("ske_", ""), img_list

def merge_refimg_skes_by_fold(input_path, output_path):
    ref_img_path, ske_list = get_maxpix_img(input_path)
    ref_img = cv2.imread(ref_img_path)
    for ske_path in ske_list:
        ske_img = cv2.imread(ske_path)
        ref_ske_img = cv2.add(ref_img, ske_img)
        frame_path = ske_path.replace("_skeleton", "").replace("ske_", "")
        frame_img = cv2.imread(frame_path)
        frame_ref_ske_img = np.concatenate([frame_img, ref_ske_img], 1)
        output_filename = frame_path.split("/")[-2] + "_" + frame_path.split("/")[-1]
        frame_ref_ske_img_path = output_path + "/" + output_filename
        cv2.imwrite(frame_ref_ske_img_path, frame_ref_ske_img)

def get_cur_fold_list(path):
    sub_dir_list = []
    list = os.listdir(path)
    for line in list:
        filepath = os.path.join(path, line)
        if os.path.isdir(filepath):
            if filepath.find("_skeleton") != -1:
                sub_dir_list.append(filepath)
    return sub_dir_list


if __name__=="__main__":

    # train
    # src = '/data/donghaoye/KTH/data/TRAIN'
    # dst = '/data/donghaoye/KTH/data4/train_A_B/train'
    src = sys.argv[0]
    dst = sys.argv[1]

    sub_dir_list = get_cur_fold_list(src)
    for sub_dir in sub_dir_list:
        merge_refimg_skes_by_fold(sub_dir, dst)





