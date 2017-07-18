# -*- coding: UTF-8 -*-
import os
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

# 将KTH分成A、B两个文件夹
def split2AB(src, dst):
    if os.path.exists(dst + "/trainA/") == False:
        os.makedirs(dst + "/trainA/")
    if os.path.exists(dst + "/trainB/") == False:
        os.makedirs(dst + "/trainB/")

    for fpathe, dirs, fs in os.walk(src):
        for f in fs:
            img_file = os.path.join(fpathe, f)
            if img_file.find("skeleton") == -1:
                file_copy(img_file, dst + "/trainA/" + img_file.split('/')[-2] + "_" + f)           # 拷贝到trainA目录
            else:
                file_copy(img_file, dst + "/trainB/" + img_file.split('/')[-2] + "_"  + f)          # 拷贝到trainB目录


def combine_A_and_B(fold_A, fold_B, fold_AB):
    if not os.path.isdir(fold_AB):
        os.makedirs(fold_AB)

    img_list = os.listdir(fold_A)
    for n in range(len(img_list)):
        name_A = img_list[n]
        path_A = os.path.join(fold_A, name_A)
        name_B = "ske_" + name_A
        path_B = os.path.join(fold_B, name_B)
        if os.path.isfile(path_A) and os.path.isfile(path_B):
            name_AB = name_A
            path_AB = os.path.join(fold_AB, name_AB)
            im_A = cv2.imread(path_A)
            im_B = cv2.imread(path_B)
            im_AB = np.concatenate([im_A, im_B], 1)
            cv2.imwrite(path_AB, im_AB)

if __name__=="__main__":
    src = '/data/donghaoye/KTH/data2/TRAIN'
    dst = '/data/donghaoye/KTH/data2/train_A_B'
    fold_A = dst + '/trainA'
    fold_B = dst + '/trainB'
    fold_AB = dst + '/trainAB'

    split2AB(src, dst)
    combine_A_and_B(fold_A, fold_B, fold_AB)


