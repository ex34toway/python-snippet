# -*- coding:utf-8 -*-

import os
from PIL import Image


def image_spite(src, row_num, col_num, dst):
    if os.path.isdir(dst) and os.path.isfile(src):
        img = Image.open(src)
        w, h = img.size
        row_num = row_num if row_num > 0 else 1
        col_num = col_num if col_num > 0 else 1
        print('Original image info: %sx%s, %s, %s' % (w, h, img.format, img.mode))
        print('开始处理图片切割, 请稍候...')

        basename = 'result'
        ext = 'JPEG'

        num = 1
        row_height = h // row_num
        col_width = w // col_num
        for r in range(row_num):
            for c in range(col_num):
                box = (c * col_width, r * row_height, (c + 1) * col_width, (r + 1) * row_height)
                img.crop(box).save(os.path.join(dst, basename + '_' + str(num) + '.' + 'jpg'), ext)
                num += 1
        print('图片切割完毕，共生成 %s 张小图片。' % (num-1))
    else:
        print('图片切割参数不正确！')

if __name__ == "__main__":
    image_spite('test.jpg', 3, 3, './dst')
