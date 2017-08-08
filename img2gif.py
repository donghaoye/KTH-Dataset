# -*- coding: UTF-8 -*-

import os
from PIL import Image
import imageio

#取得目录下面的文件列表
def get_dir_img_list(dir_proc, recusive = True):
    resultList = []
    for file in os.listdir(dir_proc):
        if os.path.isdir(os.path.join(dir_proc, file)):
            if (recusive):
                resultList.append(get_dir_img_list(os.path.join(dir_proc, file), recusive))
            continue
        img = dir_proc + "/" + file
        resultList.append(img)
    return resultList


def split_imglist_to_videoimglist(resultList):
    d = {}
    img_realA_list = []
    img_realB_list = []
    img_fakeB_list = []
    for jpg_path in resultList:
        filename = jpg_path.split("/")[-1]
        fname_list = filename.split("_")
        cur_end = fname_list[5]
        cur_index = fname_list[7]
        AorB = fname_list[-2] + "_" + fname_list[-1][0]
        key = fname_list[0] + "_" + fname_list[1] + "_" + fname_list[2] + "_" + fname_list[3] + "_" + fname_list[
            4] + "_" + fname_list[5] + "_" + AorB

        if AorB.find("real_A") != -1:
            if cur_index < cur_end:
                img_realA_list.append(jpg_path)
            elif cur_index == cur_end:
                img_realA_list.append(jpg_path)
                d[key] = img_realA_list
                img_realA_list = []
        elif AorB.find("real_B") != -1:
            if cur_index < cur_end:
                img_realB_list.append(jpg_path)
            elif cur_index == cur_end:
                img_realB_list.append(jpg_path)
                d[key] = img_realB_list
                img_realB_list = []
        elif AorB.find("fake_B") != -1:
            if cur_index < cur_end:
                img_fakeB_list.append(jpg_path)
            elif cur_index == cur_end:
                img_fakeB_list.append(jpg_path)
                d[key] = img_fakeB_list
                img_fakeB_list = []
    return d


def imglist2gif(gifpath, image_list, duration=0.5):
    # methon 1
    # images = []
    # for filename in image_list:
    #     images.append(imageio.imread(filename))
    #
    # imageio.mimsave(gifpath, images, duration)

    # methon 2
    with imageio.get_writer(gifpath, mode='I', duration=0.5) as writer:
        for filename in image_list:
            image = imageio.imread(filename)
            writer.append_data(image)

    print (gifpath)
    for img in image_list:
        print (img)


if __name__ == "__main__":
    image_files = get_dir_img_list("I:/20170801/results/skeleton_pix2pix/test_latest/images")
    dict = split_imglist_to_videoimglist(image_files)

    for k, image_list in dict.iteritems():
        gif_dir = "I:/20170801/results/skeleton_pix2pix/test_latest/gif/"
        if os.path.exists(gif_dir) == False:
            os.makedirs(gif_dir)

        imglist2gif(gif_dir + "/" + k + ".gif", image_list, duration=0.002)


