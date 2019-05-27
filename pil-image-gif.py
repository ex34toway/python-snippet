# -*- coding:utf-8 -*-

import time
from PIL import Image
from PIL.GifImagePlugin import getheader, getdata
import os
import numpy as np


def intToBin(i):
    """ 把整型数转换为双字节 """
    # 先分成两部分,高8位和低8位
    i1 = i % 256
    i2 = int(i / 256)
    # 合成小端对齐的字符串
    return chr(i1) + chr(i2)


def getheaderAnim(im):
    """ 生成动画文件头 """
    bb = "GIF89a"
    bb += intToBin(im.size[0])
    bb += intToBin(im.size[1])
    bb += "\x87\x00\x00"  # 使用全局颜色表
    return bb


def getAppExt(loops=0):
    """ 应用扩展,默认为0,为0是表示动画是永不停止
    """
    bb = "\x21\xFF\x0B"  # application extension
    bb += "NETSCAPE2.0"
    bb += "\x03\x01"
    if loops == 0:
        loops = 2 ** 16 - 1
    bb += intToBin(loops)
    bb += '\x00'  # end
    return bb


def getGraphicsControlExt(duration=0.1):
    """ 设置动画时间间隔 """
    bb = '\x21\xF9\x04'
    bb += '\x08'  # no transparancy
    bb += intToBin(int(duration * 100))  # in 100th of seconds
    bb += '\x00'  # no transparant color
    bb += '\x00'  # end
    return bb


def _writeGifToFile(fp, images, durations, loops):
    """ 把一系列图像转换为字节并存入文件流中
    """
    # 初始化
    frames = 0
    previous = None
    for im in images:
        if not previous:
            # 第一个图像
            # 获取相关数据
            palette = getheader(im)[1]  # 取第一个图像的调色板
            data = getdata(im)
            imdes, data = data[0], data[1:]
            header = getheaderAnim(im)
            appext = getAppExt(loops)
            graphext = getGraphicsControlExt(durations[0])

            # 写入全局头
            fp.write(header)
            fp.write(palette)
            fp.write(appext)

            # 写入图像
            fp.write(graphext)
            fp.write(imdes)
            for d in data:
                fp.write(d)

        else:
            # 获取相关数据
            data = getdata(im)
            imdes, data = data[0], data[1:]
            graphext = getGraphicsControlExt(durations[frames])

            # 写入图像
            fp.write(graphext)
            fp.write(imdes)
            for d in data:
                fp.write(d)
                # 准备下一个回合
        previous = im.copy()
        frames = frames + 1

    fp.write(";")  # 写入完成
    return frames


def writeGif(filename, images, duration=0.1, loops=0, dither=1):
    """ writeGif(filename, images, duration=0.1, loops=0, dither=1)
    从输入的图像序列中创建GIF动画
    images 是一个PIL Image [] 或者 Numpy Array
    """
    images2 = []
    # 先把图像转换为PIL格式
    for im in images:

        if isinstance(im, Image.Image):  # 如果是PIL Image
            images2.append(im.convert('P', dither=dither))

        elif np and isinstance(im, np.ndarray):  # 如果是Numpy格式
            if im.dtype == np.uint8:
                pass
            elif im.dtype in [np.float32, np.float64]:
                im = (im * 255).astype(np.uint8)
            else:
                im = im.astype(np.uint8)
                # 转换
            if len(im.shape) == 3 and im.shape[2] == 3:
                im = Image.fromarray(im, 'RGB').convert('P', dither=dither)
            elif len(im.shape) == 2:
                im = Image.fromarray(im, 'L').convert('P', dither=dither)
            else:
                raise ValueError("图像格式不正确")
            images2.append(im)

        else:
            raise ValueError("未知图像格式")

            # 检查动画播放时间
    durations = [duration for im in images2]
    # 打开文件
    fp = open(filename, 'wb')
    # 写入GIF
    try:
        n = _writeGifToFile(fp, images2, durations, loops)
        print(n, '帧图像已经写入')
    finally:
        fp.close()


if __name__ == "__main__":
    seq = []
    steps = float(input("输入录制间隔(单位:秒):"))
    x = input("按下任意键开始录制...")
    os.system("mkdir images")  # 创建一个文件夹,用于存放临时文件
    for i in range(10):
        time.sleep(steps)
        im = Image.grab((0, 0, 1920, 1080))  # 捕捉屏幕的左上角(0,0,320,245)部分
        # 这里由于ImageGrab.grab返回的图像格式未知,只能使用笨办法,每次存盘再打开,格式就正确了
        im.save("images\\test" + str(i) + ".jpg")  # 图像存入
        seq.append(Image.open("images\\test" + str(i) + ".jpg"))  # 重新打开
        print("采集了第" + str(i) + "帧图像")
    print("屏幕捕捉完成")
    writeGif('output.gif', seq, duration=0.5, dither=0)
    x = input("按下任意键退出")
