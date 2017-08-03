# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import randint


# 随机字母:
def rnd_char():
    return chr(randint(65, 90))


# 随机颜色1:
def rnd_color():
    return (randint(64, 255), randint(64, 255), randint(64, 255))


# 随机颜色2:
def rnd_color2():
    return (randint(32, 127), randint(32, 127), randint(32, 127))


def rnd_captcha():
    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype("C:\\Windows\\Fonts\\Arial.ttf", 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rnd_color())
    # 输出文字:
    for t in range(4):
        draw.text((60 * t + 10, 10), rnd_char(), font=font, fill=rnd_color2())
    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    image.save('captcha.jpg', 'JPEG')


if __name__ == "__main__":
    rnd_captcha()
