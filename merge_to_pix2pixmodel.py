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
def split2AB(src, fold_A, fold_B):
    if os.path.exists(fold_A) == False:
        os.makedirs(fold_A)
    if os.path.exists(fold_B) == False:
        os.makedirs(fold_B)

    for fpathe, dirs, fs in os.walk(src):
        for f in fs:
            img_file = os.path.join(fpathe, f)
            if img_file.find("skeleton") == -1:
                file_copy(img_file, fold_A + "/" + img_file.split('/')[-2] + "_" + f)           # 拷贝到trainA目录
            else:
                file_copy(img_file, fold_B + "/" + img_file.split('/')[-2] + "_"  + f)          # 拷贝到trainB目录


def combine_A_and_B(fold_A, fold_B, fold_AB):
    if not os.path.isdir(fold_AB):
        os.makedirs(fold_AB)

    img_list = os.listdir(fold_A)
    for n in range(len(img_list)):
        name_A = img_list[n]
        path_A = os.path.join(fold_A, name_A)
        tmp1 = name_A.split('_')[-2] + "_" + name_A.split('_')[-1]
        tmp2 = name_A.split(tmp1)[0]
        name_B = tmp2 + "skeleton_ske_" + tmp1
        path_B = os.path.join(fold_B, name_B)
        if os.path.isfile(path_A) and os.path.isfile(path_B):
            name_AB = name_A
            path_AB = os.path.join(fold_AB, name_AB)
            im_A = cv2.imread(path_A)
            im_B = cv2.imread(path_B)
            im_AB = np.concatenate([im_A, im_B], 1)
            cv2.imwrite(path_AB, im_AB)

if __name__=="__main__":
    # train
    # src = '/data/donghaoye/KTH/data/TRAIN'
    # dst = '/data/donghaoye/KTH/data3/train_A_B'
    # fold_A = dst + '/trainA'
    # fold_B = dst + '/trainB'
    # fold_AB = dst + '/train'   #trainAB

    # test
    src = '/data/donghaoye/KTH/data/TEST'
    dst = '/data/donghaoye/KTH/data3/test_A_B'
    fold_A = dst + '/testA'
    fold_B = dst + '/testB'
    fold_AB = dst + '/test'   #testAB

    # validation
    # src = '/data/donghaoye/KTH/data/VALIDATION'
    # dst = '/data/donghaoye/KTH/data3/validation_A_B'
    # fold_A = dst + '/validationA'
    # fold_B = dst + '/validationB'
    # fold_AB = dst + '/validation'   #validationAB


    split2AB(src, fold_A, fold_B)
    combine_A_and_B(fold_A, fold_B, fold_AB)


