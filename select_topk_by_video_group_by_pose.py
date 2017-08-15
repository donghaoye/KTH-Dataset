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

def top_k(A, k):
    if len(A) < k: return A
    pivot = A[-1]
    right = [pivot] + [x for x in A[:-1] if x >= pivot]
    rlen = len(right)
    if rlen == k:
        return right
    if rlen > k:
        return top_k(right, k)
    else:
        left = [x for x in A[:-1] if x < pivot]
        return top_k(left, k - rlen) + right

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

    topk_pix = top_k(dict.keys(), k)
    real_img_list = []
    skeleton_img_list = []
    for tk in topk_pix:
        skeleton_img_list.append(dict[tk])
        real_img_list.append(dict[tk].replace("_skeleton", "").replace("ske_", ""))
    return real_img_list, skeleton_img_list

def write_file_by_list(real_img_list, output_path):
    for img_path in real_img_list:
        img = cv2.imread(img_path)
        output_filename = img_path.split("/")[-2] + "_" + img_path.split("/")[-1]
        output_file_path = os.path.join(output_path, output_filename)
        cv2.imwrite(output_file_path, img)


def save_topk_img_and_skeleton(input_path, output_path, k):
    output_path_A = os.path.join(output_path, "A")
    output_path_B = os.path.join(output_path, "B")
    if not os.path.exists(output_path_A):
        os.makedirs(output_path_A)
    if not os.path.exists(output_path_B):
        os.makedirs(output_path_B)

    real_img_list_waving = []
    real_img_list_walking = []
    real_img_list_running = []
    skeleton_img_list_waving = []
    skeleton_img_list_walking = []
    skeleton_img_list_running = []

    real_img_list, skeleton_img_list = get_topk_pix_img(input_path, k)

    for img in real_img_list:
        if img.find("waving") != -1:
            real_img_list_waving.append(img)
        if img.find("walking") != -1:
            real_img_list_walking.append(img)
        if img.find("running") != -1:
            real_img_list_running.append(img)

    for img in skeleton_img_list:
        if img.find("waving") != -1:
            skeleton_img_list_waving.append(img)
        if img.find("walking") != -1:
            skeleton_img_list_walking.append(img)
        if img.find("running") != -1:
            skeleton_img_list_running.append(img)

    write_file_by_list(real_img_list_waving, output_path_A)
    write_file_by_list(real_img_list_walking, output_path_A)
    write_file_by_list(real_img_list_running, output_path_A)
    write_file_by_list(skeleton_img_list_waving, output_path_B)
    write_file_by_list(skeleton_img_list_walking, output_path_B)
    write_file_by_list(skeleton_img_list_running, output_path_B)



if __name__=="__main__":

    # 按照pose类型建立的文件夹 waving/walking/running
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
        cat_dir = sub_dir.split("_")[1]
        dst_path = os.path.join(dst_path, cat_dir)
        save_topk_img_and_skeleton(sub_dir, dst_path, 80)




