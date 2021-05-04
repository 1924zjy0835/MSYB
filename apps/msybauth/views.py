from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm
from django.http import JsonResponse
from utils import Restful
from django.shortcuts import render, reverse, redirect,HttpResponse
from utils.captcha.msybcaptcha import Captcha
from io import BytesIO
from django.core.cache import cache
from .models import User


@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        # 验证用户信息
        user = authenticate(request, username=telephone, password=password)
        if user:
            if user.is_active:
                # 如果用户是有效的就可以登录成功
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                # 一定要返回一个http Response
                return Restful.ok()
            else:
                print("亲，您没有权限访问该页面哦！")
                return Restful.unauth(message="亲，您没有权限访问该页面哦！")
        else:
            print("您输入的手机号或密码有误！")
            return Restful.paramserror(message="您输入的手机号或密码有误！")
    else:
        # 因为继承了FormMixin，所以form就拥有get_errors()方法
        errors = form.get_errors()
        print(errors)
        return Restful.paramserror(message=errors)


#  退出登录的视图函数
def logout_view(request):
    logout(request)
    return redirect(reverse("clothes:index"))


@require_POST
def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get("telephone")
        username = form.cleaned_data.get("username")
        # 密码在form表单，前端出已经验证过了，在这里只要获取一个password即可
        password = form.cleaned_data.get("password1")
        user = User.objects.create_user(telephone=telephone, username=username, password=password)
        # 将用户保存在数据库中
        User.save(user)
       # 如果可以创建用户成功，就默认让用户自动登录
        login(request, user)
        # 并且需要返回给用户一个登录成功
        return Restful.ok()
    else:
        return Restful.paramserror(message=form.get_errors())


def img_captcha(request):
    # 获取文本和图片
    text, image = Captcha.gene_code()
    # image图片返回给浏览器，但是image并不能直接放在httpResponse中，
    # 需要放在内存流管道中
    # BytesTO()相当于一个管道，用来存储图片的流数据
    out = BytesIO() # 创建一个对象
    # 将图片保存,并且指定写入图片的类型
    image.save(out, 'png')
    # 将文件指针移动到最前面
    out.seek(0)
    # 指定HttpResponse中存放的对象为image，而不是字符串
    response = HttpResponse(content_type="image/png")
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    # 通过tell获取当前文件指针的位置，就是当前的文件的大小
    response['Content-length'] = out.tell()

    #  将图形验证码存放在memcached缓存中
    # cache.set(key, value, 过期时间)
    cache.set(text, text, 5*60)
    return response


# 测试memcached是否可以存储数据
def memcache_test(request):
    cache.set('username', 'ant', 60)
    result = cache.get("username")
    print(result)
    return HttpResponse("success")

