from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST, require_GET
from .models import clothCategory, Shop, Clothes, AddModel
from apps.msybauth.models import User
from utils import Restful
from .forms import EditClothCategory, AddShop, PublishClothesForm, EditShop
import os
from django.conf import settings
import qiniu
import getpass
from django.views.generic import View
from django.db.models import Count


# 只有公司的员工才能够来到该页面,普通用户在访问该页面的时候会重定向至首页
@staff_member_required(login_url="/")
def cms_index(request):
    return render(request, "cms/index.html")


#  添加店铺
def shop(request):
    shops = Shop.objects.all()
    context = {
        'shops': shops,
    }
    return render(request, 'cms/add_shop.html', context=context)


def add_shop(request):
    form = AddShop(request.POST)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        name_exist = Shop.objects.filter(name=name).exists()
        if not name_exist:
            Shop.objects.create(name=name, shopkeeper=request.user.username)
            return Restful.result(message="店铺添加成功~")
        else:
            return Restful.paramserror(message="店铺名称已经存在~")
    else:
        return Restful.paramserror(message=form.get_errors())


#  编辑店铺名
def edit_shop(request):
    form = EditShop(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get("pk")
        name = form.cleaned_data.get("name")
        try:
            # 通过pk拿到前端传递来的服装分类，进行更新服装分类名
            Shop.objects.filter(pk=pk).update(name=name)
            return Restful.ok()
            # 如果不存在的话就会抛出一个异常
        except:
            return Restful.paramserror(message="您当前编辑的店铺名不存在！")
    else:
        return Restful.paramserror(message=form.get_errors())


# 删除店铺(删除店铺只需要一个pk就可以了，因此就不需要定义表单进行验证了)
def delete_shop(request):
    pk = request.POST.get("pk")
    exists = Shop.objects.filter(pk=pk).exists()
    if exists:
        Shop.objects.filter(pk=pk).delete()
        return Restful.ok()
    else:
        return Restful.paramserror(message="该店铺已经不存在了！")


# 上架商品
class Publish_cloth(View):
    def get(self,request):
        categories = clothCategory.objects.all()
        shops = Shop.objects.all()
        context = {
            'categories': categories,
            'shops': shops
        }
        return render(request, "cms/publish_cloth.html", context=context)

    def post(self, request):
        form = PublishClothesForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form .cleaned_data.get('desc')
            price = form.cleaned_data.get('price')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            shop_id = form.cleaned_data.get('shop')
            shop_name = Shop.objects.get(pk=shop_id).name
            category_id = form.cleaned_data.get('category')
            category = clothCategory.objects.get(pk=category_id)
            Clothes.objects.create(title=title, desc=desc, price=price, thumbnail=thumbnail, content=content, shop=shop_name, category=category)
            return Restful.ok()
        else:
            return Restful.paramserror(message=form.get_errors())

from itertools import groupby

# 服装分类
@require_GET
def category_cloth(request):
    # 因为服装的分类不多，所以此时就可以全部取出进行返回
    categories = clothCategory.objects.all()
    # 使用annotate()函数对clothCategory按id进行分组，然后统计不同分组的服装数量
    clothNumbers = clothCategory.objects.annotate(numbers=Count("clothes__price"))
    # for clothNumber in clothNumbers:
    #     print("=============================")
    #     print("服装分类名称：",clothNumber.name)
    #     print(clothNumber.numbers)
    #     print("=============================")
    context = {
        "categories": categories,
            # 'clothNumbers': clothNumber.numbers
    }
    return render(request, 'cms/category_cloth.html', context=context)
    # return Restful.ok()


# 添加服装分类
@require_POST
def add_category_cloth(request):
    # 因为clothCategory模型只有一个字段，所以就不需要用表单去判定了
    name = request.POST.get("name")
    exists = clothCategory.objects.filter(name=name).exists()
    if not exists:
        clothCategory.objects.create(name=name)
        return Restful.ok()
    else:
        return Restful.paramserror(message="该分类已经存在！")


# 编辑服装分类
def edit_category_cloth(request):
    form = EditClothCategory(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get("pk")
        name = form.cleaned_data.get("name")
        try:
            # 通过pk拿到前端传递来的服装分类，进行更新服装分类名
            clothCategory.objects.filter(pk=pk).update(name=name)
            return Restful.ok()
            # 如果不存在的话就会抛出一个异常
        except:
            return Restful.paramserror(message="您当前编辑的该分类不存在！")
    else:
        return Restful.paramserror(message=form.get_errors())


# 删除服装分类(删除服装分类只需要一个pk就可以了，因此就不需要定义表单进行验证了)
def delete_category_cloth(request):
    pk = request.POST.get("pk")
    exists = clothCategory.objects.filter(pk=pk).exists()
    if exists:
        clothCategory.objects.filter(pk=pk).delete()
        return Restful.ok()
    else:
        return Restful.paramserror(message="该分类不存在！")


# 上传文件到本地服务器
@require_POST
def upload_file(request):
    file = request.FILES.get("file")
    name = file.name
    # 将文件name保存在我们在settings.py文件中设置的目录中
    with open(os.path.join(settings.MEDIA_ROOT, name), "wb") as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    # 拼接真实的url
    url = request.build_absolute_uri(settings.MEDIA_URL + name)
    return Restful.result(data={'url': url})


# 上传文件图片到qiniu
def qntoken(request):
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY

    bucket = settings.QINIU_BUCKET_NAME
    # 为七牛云操作提供授权加密服务，提供管理，下载，上传凭证
    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket)
    return Restful.result(data={"token": token})


#  添加模特
def add_model(request):
    thumbnail = request.POST.get('thumbnail')
    if thumbnail:
        AddModel.objects.create(thumbnail=thumbnail)
        return Restful.ok()
    else:
        return render(request, 'cms/add_model.html')
