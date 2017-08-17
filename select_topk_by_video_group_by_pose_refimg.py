# -*- coding: UTF-8 -*-
import os
import sys
import shutil
import numpy as np
import cv2

def get_cur_fold_list(path):
    sub_dir_list = []
    list = os.listdir(path)
    for line in list:
        #filepath = os.path.join(path, line)
        filepath = path + "/" + line
        if os.path.isdir(filepath):
            if filepath.find("_skeleton") != -1:
                sub_dir_list.append(filepath)
    return sub_dir_list

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
        #img = os.path.join(dir_proc, file)
        img = dir_proc + "/" + file

        file_list.append(img)
    return file_list

def sum_zero_one_img(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    return sum(sum(img))


def get_topk_pix_img(img_fold, k):
    img_list = get_dir_img_list(img_fold)
    dict = {}
    for path in img_list:
        sum_pix = sum_zero_one_img(path)
        dict[sum_pix] = path
    k = min(k, len(img_list))
    topk_pix = sorted(dict.keys(), reverse=True)[:k]                            # top k
    real_img_list = []
    skeleton_img_list = []
    for tk in topk_pix:
        skeleton_img_list.append(dict[tk])
        real_img_list.append(dict[tk].replace("_skeleton", "").replace("ske_", ""))
    return real_img_list, skeleton_img_list

def write_file_by_list(img_list, output_path):
    for img_path in img_list:
        img = cv2.imread(img_path)
        output_filename = img_path.split("/")[-2] + "_" + img_path.split("/")[-1]
        output_file_path = os.path.join(output_path, output_filename)
        cv2.imwrite(output_file_path, img)

def write_ref_file_by_list(img_path, imgpath_list, output_path):
    img = cv2.imread(img_path)
    for img_path in imgpath_list:
        output_filename = img_path.split("/")[-2] + "_ref_" + img_path.split("/")[-1]
        output_file_path = os.path.join(output_path, output_filename)
        cv2.imwrite(output_file_path, img)

def save_topk_img_and_skeleton(input_path, output_path, k):
    output_path_A = os.path.join(output_path, "real")
    output_path_B = os.path.join(output_path, "skeleton")
    output_path_C = os.path.join(output_path, "reference")
    if not os.path.exists(output_path_A):
        os.makedirs(output_path_A)
    if not os.path.exists(output_path_B):
        os.makedirs(output_path_B)
    if not os.path.exists(output_path_C):
        os.makedirs(output_path_C)

    real_img_list, skeleton_img_list = get_topk_pix_img(input_path, k)

    write_file_by_list(real_img_list, output_path_A)
    write_file_by_list(skeleton_img_list, output_path_B)
    write_ref_file_by_list(real_img_list[0], real_img_list, output_path_C)



if __name__=="__main__":

    # train
    # src = 'I:/KTH/TRAIN'
    # dst = 'I:/KTH/data5/train_A_B/train2'
    # src = /data/donghaoye/KTH/data/VALIDATION
    # dst = /data/donghaoye/KTH/data5/validation_A_B/validation
    # src = /data/donghaoye/KTH/data/TEST
    # dst = /data/donghaoye/KTH/data5/test_A_B/test
    src = sys.argv[1]
    dst = sys.argv[2]

    sub_dir_list = get_cur_fold_list(src)
    for sub_dir in sub_dir_list:
        dst_path = dst
        cat_dir = sub_dir.split("_")[1]                     # 这里已经按照pose类型建立的文件夹 waving/walking/running
        dst_path = os.path.join(dst_path, cat_dir)
        if cat_dir.find("handwaving") != -1:                # waving的图片全拿，running只取skeleton出现的
            save_topk_img_and_skeleton(sub_dir, dst_path, 65535)
        else:
            save_topk_img_and_skeleton(sub_dir, dst_path, 50)




