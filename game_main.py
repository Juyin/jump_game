#/usr/bin/env  python3.5
# -*- coding: UTF-8 -*-

import os
import sys
import subprocess
from PIL import Image
import math
import time

def is_jumper_pixel(pixel):
    if pixel[0] > 50 and pixel[0] < 60 and pixel[1] > 55 and pixel[1] < 65 and pixel[2] > 95 and pixel[2] < 105:
        return True
    else:
        return False


def get_device_info():
    device_size = os.popen('adb shell wm size').read()
    if not device_size:
        return 0,0
    print(device_size)#Physical size: 1080x1920

    screen_size = device_size.split(':')[1]
    x_size = screen_size.split('x')[0]
    y_size = screen_size.split('x')[1]
    #print(x_size,y_size)
    return x_size,y_size

def get_phone_shootphoto():
    if os.path.isfile('autojump.png'):
        try:
            os.remove('autojump.png')
        except Exception:
            pass

    process = subprocess.Popen('adb shell screencap -p',
        shell=True, stdout=subprocess.PIPE)
    binary_screenshot = process.stdout.read()
    binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')

    f = open('autojump.png', 'wb')
    f.write(binary_screenshot)
    f.close()
    try:
        Image.open('autojump.png').load()
        print('采用方式 {} 获取截图'.format(2))
    except Exception:
        pass
        # check_screenshot()

import matplotlib.pyplot as plt
def get_img_center_point(img):
    print(__file__)
    plt.imshow(img, cmap=plt.get_cmap("gray"))
    exit_this = False
    while not exit_this:
        pos = plt.ginput(3)
        center_x, center_y = pos[1][0], pos[1][1]
        yorn = input("are you sure use this: ")
        if yorn == 'y':
            exit_this = True
        else:
            exit_this = False
    return center_x, center_y




use_hand=False


def shootphoto_handle():
    img = Image.open('autojump.png')

    if not use_hand:
        #得到目的地方块的位置
        upper_point_x, upper_point_y, left_point_x, left_point_y, right_point_x, right_point_y=get_block(img)
        print("all:",upper_point_x,upper_point_y,left_point_x,left_point_y,right_point_x,right_point_y)
        center_x,center_y=get_block_center_point(upper_point_x, upper_point_y, left_point_x, left_point_y, right_point_x, right_point_y)
    else:
        center_x,center_y = get_img_center_point(img)

    print("center:",center_x,center_y)
    jumper_x,jumper_y = get_jumper(img)
    img.close()
    print("jumper:",jumper_x,jumper_y)


    offset_x = abs(jumper_x - center_x)
    offset_y = abs(jumper_y - center_x)
    #得到待跳方块位置
    return offset_x,offset_y

g_step = 1
def get_block(img):
    block_x = 0
    block_y = 0
    scan_start_y = 0
    upper_point_x = 0
    upper_point_y = 0
    left_point_x = 0
    left_point_y = 0
    right_point_x = 0
    right_point_y = 0
    down_point_x = 0
    down_point_y = 0


    x_size,y_size = img.size

    left_point_x = x_size
    right_point_x = 0

    img_pixel = img.load()
    print("find upper point,start y",int(400), int(y_size*2 / 3))
    # 以 50px 步长，尝试探测 scan_start_y,扫描纵坐标，50为步长
    for i in range(int(400), int(y_size*2 / 3), g_step):
        last_pixel = img_pixel[0, i]
        # print("last_pixel",last_pixel)
        for j in range(1, x_size):
            pixel = img_pixel[j, i]
            #if i>750 and i<810:
                #print("x,y,pixel:",j,i, pixel)

            # 不是纯色的线，则记录 scan_start_y 的值，准备跳出循环
            if abs(pixel[0] - last_pixel[0])>100 or abs(pixel[1] - last_pixel[1])>100 \
                or abs(pixel[2] - last_pixel[2])>100:
                scan_start_y = i - g_step
                upper_point_x = j
                upper_point_y = i
                break
        if scan_start_y:
            break
    print('scan_start_y: {}'.format(scan_start_y))
    print('upper_point: {},{}'.format(upper_point_x,upper_point_y))


    print("#################################")
    print(int(upper_point_y),int(y_size*2 / 3))

    for x in range(int(upper_point_x), int(x_size/8), -1):
        go_out=False

        upper_point = img_pixel[upper_point_x, upper_point_y]
        #print("last_pixel pixel", last_pixel)

        # print("start x",  int(x_size/8),int(upper_point_x))
        for y in range( int(300),int(y_size*2 / 3),1):
            last_pixel = img_pixel[10, y]
            pixel = img_pixel[x, y]
            # 不是纯色的线，则记录 scan_start_y 的值，准备跳出循环
            if (abs(pixel[0] - last_pixel[0]) > 100 or abs(pixel[1] - last_pixel[1]) > 100 \
                     or abs(pixel[2] - last_pixel[2]) > 100 ):
                print("x,y,left_point_y,pixel,last_pixel", x,y,left_point_y,pixel, last_pixel)
                if y > left_point_y + 5 and left_point_y!=0:
                    go_out = True
                    break
                elif y > left_point_y:
                    left_point_x = x
                    left_point_y = y
                    print('#left:',x,y)
                    break
                else:
                    print("error")
                    break
        if go_out:
            break

    # for y in range(int(upper_point_y), int(y_size*2 / 3), 1):
    #     go_out=False
    #     last_pixel = img_pixel[10, y]
    #     upper_point = img_pixel[upper_point_x, upper_point_y]
    #     #print("last_pixel pixel", last_pixel)
    #
    #     print("start x",  int(x_size/8),int(upper_point_x))
    #     for x in range( int(x_size/8),int(upper_point_x),1):
    #         pixel = img_pixel[x, y]
    #         # 不是纯色的线，则记录 scan_start_y 的值，准备跳出循环
    #         if (abs(pixel[0] - last_pixel[0]) > 100 or abs(pixel[1] - last_pixel[1]) > 100 \
    #             or abs(pixel[2] - last_pixel[2]) > 100 ):
    #             if is_jumper_pixel(pixel):
    #                 continue
    #             else:
    #                 print("x,y,left_point_x,pixel,last_pixel", x,y,left_point_x,pixel, last_pixel)
    #                 if x < left_point_x:
    #                     left_point_x = x
    #                     left_point_y = y
    #                     print('#left:',x,y)
    #                 elif x>left_point_x+2:#x逐渐减小，说明已经过左顶点
    #                     print("###x,y,left_point_x", x, y, left_point_x)
    #                     go_out = True
    #                     break
    #                 else:
    #
    #                     break
    #     if go_out:
    #         break
    print('left_point: {},{}'.format(left_point_x,left_point_y))
    print("#################################")



    for y in range(int(upper_point_y), int(y_size * 2 / 3), 5):
        go_out = False
        print(y,int(y_size * 2 / 3))
        last_pixel = img_pixel[x_size-1, y]
        upper_point = img_pixel[upper_point_x, upper_point_y]
        # print("upper_point pixel", upper_point)

        for x in range(int(x_size-1), int(upper_point_x), -1):
            pixel = img_pixel[x, y]
            # 不是纯色的线，则记录 scan_start_y 的值，准备跳出循环
            if (abs(pixel[0] - last_pixel[0]) > 100 or abs(pixel[1] - last_pixel[1]) > 100 \
                     or abs(pixel[2] - last_pixel[2]) > 100 ):
                # print("x,y,right_point_x", x, y, right_point_x)
                if x > right_point_x:
                    right_point_x = x
                    right_point_y = y
                    # print('right:', x, y)
                elif x <= right_point_x:  # x逐渐减小，说明已经过左顶点

                    go_out = True
                    break
                break
        if go_out:
            break
    print('right_point: {},{}'.format(right_point_x, right_point_y))




    print('upper_point: {},{}'.format(upper_point_x, upper_point_y))
    print('left_point: {},{}'.format(left_point_x,left_point_y))
    print('right_point: {},{}'.format(right_point_x, right_point_y))
    return upper_point_x,upper_point_y,left_point_x,left_point_y,right_point_x,right_point_y

def get_block_center_point(upper_point_x,upper_point_y,left_point_x,left_point_y,right_point_x,right_point_y):
    center_x = left_point_x  +   (right_point_x - left_point_x)/2
    center_y = left_point_y +   (right_point_y - left_point_y)/2
    return center_x,center_y


def get_jumper(img):
    jumper_x = 0
    jumper_y = 0
    x_size,y_size = img.size
    img_pixel = img.load()
    for y in range(400, int(y_size * 2 / 3), 5):
        for x in range(int(x_size / 8), int(x_size)):
            pixel = img_pixel[x, y]
            #print("x,y,pixel",x,y,pixel)
            if pixel[0]>50 and pixel[0]<60 and pixel[1]>55 and pixel[1]<65 and pixel[2]>95 and pixel[2]<105:
                #print(x,y)
                if y > jumper_y:
                    jumper_x = x
                    jumper_y = y

    jumper_y -= 15
    jumper_x += 10
    return jumper_x,jumper_y

def jump2(offset_x, offset_y):
    """
    跳跃一定的距离
    """
    press_time =(int(offset_x)^2+int(offset_y)^2)

    print("press_time",press_time)

    press_time = press_time*1.392
    #press_time = max(press_time, 200)  # 设置 200ms 是最小的按压时间
    print("press_time2", press_time)
    press_time = int(press_time)
    cmd = 'adb shell input touchscreen swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=560,
        y1=1536,
        x2=560,
        y2=1536,
        duration=press_time
    )

    print(cmd)
    os.system(cmd)
    return press_time

press_coefficient=1.475
def jump(offset_x, offset_y):
    """
    跳跃一定的距离
    """
    distance = math.sqrt((offset_x ) ** 2 + (offset_y) ** 2)

    press_time = distance * press_coefficient
    if press_time <200:
        print("press_time",press_time)
        return
    #press_time = max(press_time, 400)   # 设置 200ms 是最小的按压时间

    press_time = int(press_time)
    cmd = 'adb shell input touchscreen swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=560,
        y1=1536,
        x2=560,
        y2=1536,
        duration=press_time
    )
    print(cmd)
    os.system(cmd)
    return press_time

def main():
    device_screen=[0,0]

    #检查adb调试模式是否可用
    x_size, y_size = get_device_info()
    if not x_size and y_size:
        print("请检查是否打开手机调试模式")
        return

    print ('screen size:{}x{}'.format(x_size,y_size))

    while True:
        #获取手机截图
        if not DEBUG:
            get_phone_shootphoto()


        #手机截图处理
        offset_x, offset_y = shootphoto_handle()
        print(offset_x,offset_y)

        print("手机截图处理")

        if not DEBUG:
            ret = jump(offset_x, offset_y)
            print("跳")

        time.sleep(2)



DEBUG=True
DEBUG=False


if __name__=='__main__':
    main()