# -*- coding: utf-8 -*-
# @Description: msybcaptcha.py
# @Author: 孤烟逐云zjy
# @Date: 2020 / 3 / 25 21: 41
# @ SoftWare: PyCharm
# @CSDN: https: //blog.csdn.net/ zjy123078_zjy
# @ 博客园: https: // www.cnblogs.com / guyan - 2020 /


 # 导入随机模块,用来产生随机数
import random
import string
import os
import time
# Image:相当于一个画布；ImageDraw：相当于一个画笔；ImageFont：相当于画笔画出的字体
from PIL import Image, ImageDraw, ImageFont
# PIL库是需要单独安装的，通过pip install pillow


# Captcha验证码
class Captcha(object):
    # 把一些常量抽取成类属性
    # 字体位置
    font_path = os.path.join(os.path.dirname(__file__),"verdana.ttf")
    # font_path='utils/captcha/ZEPHYR__1.TTF'
    # 生成几位数的验证码
    number = 6
    # 生成验证码图片的宽度和高度
    size = (120,40)
    # 背景颜色，默认为白色 RGB()
    bgColor = (0, 0, 0)
    # 随机字体颜色
    random.seed(int(time.time()))
    fontColor = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
    # 验证码字体的大小
    fontsize = 20
    # 随机干扰线颜色
    lineColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0,255))
    # 是否要加入干扰线
    draw_line = True
    # 是否绘制干扰点
    draw_point = True
    # 加入干扰线的条数
    line_number = 3

    # 返回一个小写的、大写的A-Z的列表，而string.ascii_letters就代表的是一个字符串
    SOURCE = list(string.ascii_letters)
    # index为0-9的10的字符
    for index in range(0, 10):
        # SOURCE就含有a-z,A-Z,0-9，为列表
        SOURCE.append(str(index))

    # 用来随机生成一个字符串（包括英文和数字）
    # 定义成类方法，私有，对象在类的外面不能直接调用
    @classmethod
    def gene_text(cls):
        # number是用来生成验证码的位数
        # random.sample函数（取样函数）会从SOURCE列表中取出number位字符进行拼接
        return ''.join(random.sample(cls.SOURCE, cls.number))

    # 用来验证干扰线
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.lineColor)

    # 定义检测干扰点
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(34, 213, 222))

    # 生成验证码
    @classmethod
    def gene_code(cls):
        width, height = cls.size
        # 创建画布
        image = Image.new('RGBA', (width, height), cls.bgColor)
        # 验证码的字体
        font = ImageFont.truetype(cls.font_path, cls.fontsize)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 生成字符串
        text = cls.gene_text()
        font_width, font_height = font.getsize(text)
        # 填充字符串
        draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font, fill=cls.fontColor)

        # 如果需要绘制干扰线
        if cls.draw_line:
            # 遍历line_number次，就是画line_number根线
            for x in range(0, cls.line_number):
                cls.__gene_line(draw, width, height)

        # 如果要绘制干扰点
        # if cls.draw_point:
        #     cls.__gene_points(draw, 10, width, height)

        # 返回所画的文本和图片
        return (text, image)
