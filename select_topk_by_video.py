# -*- coding: UTF-8 -*-
import os
import sys
import shutil
import numpy as np
import cv2


'''
将real image 和 skeleton image合并到同一张图
'''

def get_cur_fold_list(path):
    sub_dir_list = []
    list = os.listdir(path)
    for line in list:
        filepath = os.path.join(path, line)
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

def save_topk_img_and_skeleton(input_path, output_path, k):
    output_path_A = os.path.join(output_path, "A")
    output_path_B = os.path.join(output_path, "B")
    if not os.path.exists(output_path_A):
        os.makedirs(output_path_A)
    if not os.path.exists(output_path_B):
        os.makedirs(output_path_B)

    real_img_list, skeleton_img_list = get_topk_pix_img(input_path, k)

    for img_path in real_img_list:
        img = cv2.imread(img_path)
        frame_path = img_path.replace("_skeleton", "").replace("ske_", "").replace("TRAIN", "")
        output_filename = frame_path.split("/")[-2] + "_" + frame_path.split("/")[-1]
        frame_ref_ske_img_path = output_path_A + "/" + output_filename
        cv2.imwrite(frame_ref_ske_img_path, img)

    # skeleton
    for ske_path in skeleton_img_list:
        ske_img = cv2.imread(ske_path)
        frame_path = ske_path.replace("_skeleton", "").replace("TRAIN", "")
        output_filename = frame_path.split("/")[-2] + "_" + frame_path.split("/")[-1]
        frame_ref_ske_img_path = output_path_B + "/" + output_filename
        cv2.imwrite(frame_ref_ske_img_path, ske_img)



if __name__=="__main__":
    # train
    # src = 'I:/KTH/TRAIN'
    # dst = 'I:/KTH/data5/train_A_B/train'
    src = sys.argv[1]
    dst = sys.argv[2]

    sub_dir_list = get_cur_fold_list(src)
    for sub_dir in sub_dir_list:
        dst_path = dst
        cat_dir = sub_dir.split("_")[1]
        dst_path = os.path.join(dst_path, cat_dir)
        save_topk_img_and_skeleton(sub_dir, dst_path, 80)




