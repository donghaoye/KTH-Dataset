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
        img = os.path.join(dir_proc, file)
        resultList.append(img)

    return resultList

if __name__ == "__main__":
    image_files = get_dir_img_list("I:\\test")

    with imageio.get_writer('I:\\1.gif', mode='I', duration=0.5) as writer:
        for filename in image_files:
            image = imageio.imread(filename)
            writer.append_data(image)

    images = []
    for filename in image_files:
        images.append(imageio.imread(filename))
    imageio.mimsave('I:\\2.gif', images, duration=0.5)
