from PIL import Image
import numpy as np
from math import sin, cos
def Resize(src, tar, sx=1, sy=1):#放 sx高度 sy宽度 近邻插值法
    if sx == 1 and sy == 1:
        print("NO CHANGE NEEDED.")
    else:
        im = Image.open(src)
        imarray = np.array(im)
        height, width = imarray.shape
        output_h = round(height * sx)
        output_w = round(width * sy)
        new_arr = np.zeros((output_h, output_w), dtype="uint8")
        for i in range(output_h):
            for j in range(output_w):
                new_arr[i, j] = imarray[round((i + 1) / sx - 1), round((j + 1) / sy - 1)]
        new_im = Image.fromarray(new_arr)
        new_im.save(tar)
        print("ResizeSuceess.")

def Rotate(src, tar, center=(0, 0), theta=0, expand=False):#旋转
    '''
    theta>0 and theta < 180 is best.
    '''
    theta = round(theta * 3.14 / 180, 2)
    im = Image.open(src)
    imarray = np.array(im)
    height, width = imarray.shape
    x, y = center
    new_arr = np.zeros((height, width), dtype='uint8')

    if not expand:
        matrix = np.array(
            [[cos(theta), sin(theta), 0],
             [-sin(theta), cos(theta), 0],
             [-x * cos(theta) + y * sin(theta) + x, -x * sin(theta) - y * cos(theta) + y, 1]])
        for i in range(height):
            for j in range(width):
                pos_x, pos_y, _ = np.matmul(np.array([i, j, 1]), matrix)

                if pos_x >= height - 0.5 or pos_x < -0.5 or pos_y >= width - 0.5 or pos_y < -0.5:
                    new_arr[i, j] = 0
                else:
                    pos_x = int(round(pos_x))
                    pos_y = int(round(pos_y))
                    new_arr[i, j] = imarray[pos_x, pos_y]
    else:
        print("Sorry.This function does't support expand rotate.Please wait for us to improve ourselves.")
    new_im = Image.fromarray(new_arr)
    new_im.save(tar)
    print("RatoteSuceess.")


def Mirror(src, target, methods="vertical"):
    '''
    methods: vertical or horizontal.#上下和左右
    '''
    im = Image.open(src)
    imarray = np.array(im)
    height, width = imarray.shape
    new_arr = np.zeros((height, width), dtype="uint8")
    if methods == "vertical":
        for i in range(height):
            for j in range(width):
                new_arr[i, j] = imarray[height - 1 - i, j]
    else:
        for i in range(height):
            for j in range(width):
                new_arr[i, j] = imarray[i, width - 1 - j]
    new_im = Image.fromarray(new_arr)
    new_im.save(target)
    print("MirrorSuceess.")



gray_girl = "G1.jpg"
tar = "gray_girl_resize.jpg"
Resize(gray_girl, tar, 1.7, 1.6)

tar = "gray_girl_ratote.jpg"
Rotate(gray_girl, tar, center = (100,100),theta = 45)

tar = "gray_girl_mirr1.jpg"
Mirror(gray_girl, tar, "horizontal")

tar = "gray_girl_mirr2.jpg"
Mirror(gray_girl, tar)
