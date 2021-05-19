# -*- coding: utf-8 -*-
"""
@author = 老表
@date = 2019-09-24
@个人公众号 : 简说Python
"""
# 注意：print_function的导入必须在Image之前，否则会报错
from __future__ import print_function

import os

from PIL import Image

"""
需求：给图片右下角添加中国国旗
欢迎国庆，喜庆70周年
"""
# class Picture:
#  def handle_picture(self):
#   # 打开图片模版
#   img1 = Image.open(r"D:\python\pycharm\pythonSpace\flask-chatroom\static\img\head\h_temp1.jpg")
#   img1 = img1.convert('RGBA')
#   # 打开原来的微信头像
#   img2 = Image.open(r"D:\python\pycharm\pythonSpace\flask-chatroom\static\img\head\h_temp2.jpg")
#   img2 = img2.convert('RGBA')
#   if img2.size != (700, 700): # 判断图片大小，统一改为 700*700
#    # 修改图片尺寸
#    size = (700, 700)
#    img2.thumbnail(size)
#    img2.show()
#   # 图片粘贴选区
#   loc = (0, 0, 700, 700)
#   # 将img1 粘贴到 img2
#   img2.paste(img1, loc, img1)
#   img2.show() # 显示图片
#   img2.save("new.png") # 保存生成的头像图片
# t0 = Picture()
# t0.handle_picture()

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

root = os.path.abspath(__file__).split('utils')[0]
static_path = os.path.join(root, 'static')


class CreatImage:
    def __init__(self):
        self.dir = os.path.join(static_path, 'img', 'user_head')

    def image(self, msg, img_name):
        # 设置字体，如果没有，也可以不设置
        # font = ImageFont.truetype("simsun.ttc",100,index=1)    #现在是宋体
        font = ImageFont.truetype(os.path.join(static_path,'font','mn.ttf'), 170)  # 迷你
        # 打开底版图片
        imageFile = os.path.join(static_path, 'img', 'head', 'h_temp1.jpg')
        im1 = Image.open(imageFile)

        # 在图片上添加文字 1
        draw = ImageDraw.Draw(im1)
        draw.text((15, 20), msg, (89, 119, 115), font=font)
        draw = ImageDraw.Draw(im1)

        # 保存
        im1.save(os.path.join(self.dir, img_name))


if __name__ == '__main__':
    print(root)
    print(static_path)
    img = CreatImage()
    img.image('吴', 'test.png')
