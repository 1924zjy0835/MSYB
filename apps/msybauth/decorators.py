# @Description: decorators.py.py
# @Author: 孤烟逐云zjy
# @Date: 2021/5/2 18:23
# @SoftWare: PyCharm
# @CSDN: https://blog.csdn.net/zjy123078_zjy
# @博客园: https://www.cnblogs.com/guyan-2020/

from django.shortcuts import render, redirect
from utils import Restful


def msyb_login_required(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, *kwargs)
        else:
            if request.is_ajax():
                return Restful.unauth(message="亲爱的！请登录哦！")
            else:
                return redirect('/')
    return wrapper