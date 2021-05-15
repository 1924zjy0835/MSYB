from django.shortcuts import render, redirect,reverse
from django.views.generic import View
from .forms import BuyerSayForm, PersonalPhotoForm, ClosetForm
from django.http import HttpResponse
import os
from django.conf import settings
from .models import PersonalPhotoModel, closet, PeopleModel
from apps.cms.models import Clothes, clothCategory, Shop, ClothesOrder
from utils import Restful
from apps.msybauth.decorators import msyb_login_required
from django.db.models import Q
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt
from apps.cms.models import AddModel

import os
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import urllib
from io import BytesIO
from skimage import io


# index
def index(request):
    clothcategorys = clothCategory.objects.all()
    shops = Shop.objects.all()
    # 默认情况下，会查询所有的服装信息进行展示
    # [0: count]: 对经过排序的服装进行切片处理，这样，在首页起初展示的就是制定的count数量的服装数
    clothes = Clothes.objects.all()
    context = {
        'clothcategorys': clothcategorys,
        'shops': shops,
        'clothes': clothes
    }
    return render(request, 'index/index.html', context=context)


# index new products
def index_new_products(request, category_id):
    clothcategorys = clothCategory.objects.all()
    clothes = Clothes.objects.filter(category_id=category_id)
    context = {
        "clothes": clothes,
        'clothcategorys': clothcategorys
    }
    return render(request, 'index/index.html', context=context)


# index==============>search
# 访问该视图函数时，可能会没有传递q，所以就需要进行一层判断，如果没有传递参数的话就默认返回最近发布的几件服装信息
# 在做查找的时候，要做或操作，可以利用Q表达式
def Search1(request):
    q = request.GET.get('q')
    clothcategorys = clothCategory.objects.all()
    if q:
        hot_clothes = Clothes.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
        context = {
            'hot_clothes': hot_clothes,
            'clothcategorys': clothcategorys
            }
        return render(request, 'search/search1.html', context=context)
    else:
        hot_clothes = Clothes.objects.order_by("-pub_time")[0:6]
        context = {
            'hot_clothes': hot_clothes,
            'clothcategorys':clothcategorys
        }
    return render(request, 'search/search1.html', context=context)


def search(request):
    q = request.GET.get('q')
    clothcategorys = clothCategory.objects.all()
    if q:
        hot_clothes = Clothes.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
        context = {
            'hot_clothes': hot_clothes,
            'clothcategorys': clothcategorys
            }
        return render(request, 'search/search1.html', context=context)
    else:
        hot_clothes = Clothes.objects.order_by("-pub_time")[0:6]
        context = {
            'hot_clothes': hot_clothes,
            'clothcategorys':clothcategorys
        }
    return render(request, 'search/search1.html', context=context)


# index===============>buyer say
class Buy_say_view(View):
    def get(self,request):
        form = BuyerSayForm()
        return render(request, 'index/buyer_say.html', context={"form": form})

    def post(self, request):
        # 从前端输入的数据都保存在request.POST上面，提交给表单进行验证
        form = BuyerSayForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            email = form.cleaned_data.get('email')
            reply = form.cleaned_data.get('reply')
            return HttpResponse("留言成功！")
        else:
            print(form.errors.get_json_data())
            return HttpResponse("留言失败！")


#  商品详情页
def detail(request):
    pk = request.POST.get("pk")
    cloth = Clothes.objects.filter(pk=pk)
    if not cloth:
        return Restful.paramserror(message="sorry~没有找到该商品的详情")
    else:
        return render(redirect(reverse('clothes:cloth_detail', kwargs={'cloth_id': pk})))


# index=================>cloth detail
def cloth_detail(request, cloth_id):
    clothcategorys = clothCategory.objects.all()
    clothes = Clothes.objects.filter(pk=cloth_id)
    if not clothes:
        return Restful.paramserror(message="sorry~没有找到该商品的详情")
    else:
        context = {
            'clothes': clothes,
            'clothcategorys': clothcategorys
        }
        return render(request, 'clothes/cloth_detail.html', context=context)


# fitting room ========= closet room =========>show
def closet_room(request):
    form = ClosetForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        thumbnail = form.cleaned_data.get("thumbnail")
        closet.objects.create(title=title, thumbnail=thumbnail)
        return Restful.ok()
    else:
        photos = PersonalPhotoModel.objects.all()
        clothcategorys = clothCategory.objects.all()
        clothes = closet.objects.all()
        models = AddModel.objects.all()
        first_model = PeopleModel.objects.first()
        context = {
            "photos": photos,
            "clothes": clothes,
            "clothcategorys": clothcategorys,
            "models": models,
            'first_model': first_model
        }
        return render(request, 'clothes/fitting_room.html', context=context)


#  fitting room ============ closet room ===========>delete cms
def drop_closet_cloth(request):
    img_url = request.POST.get("img_url")
    closetcloth = closet.objects.filter(thumbnail=img_url)
    if closetcloth.exists():
        closetcloth.delete()
        return Restful.ok()
    else:
        return Restful.paramserror(message="亲~您要删除的服装不存在哦！请刷新页面重试")


# fitting room========= model room =========>show
def fitting_room(request):
    photos = PersonalPhotoModel.objects.all()
    clothes = closet.objects.all()
    clothcategorys = clothCategory.objects.all()
    models = AddModel.objects.all()
    model = AddModel.objects.first()
    first_model = PeopleModel.objects.first()
    context = {
        "photos": photos,
        "clothes": clothes,
        "clothcategorys": clothcategorys,
        "models": models,
        "model": model,
        "first_model": first_model
    }
    return render(request, 'clothes/fitting_room.html', context=context)


# fitting room ========= model room ========> upload personal photos
def upload_personal_photo(request):
    # 生成上传的个人照的url并且保存找数据库中
    file = request.FILES.get("file")
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT, name), "wb") as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL+name)
    # form = PersonalPhotoForm(request.POST)
    # if form.is_valid():
    pub_time = request.POST.get("pub_time")
    personalphoto = PersonalPhotoModel.objects.create(pub_time=pub_time, img_url=url)
    personalphoto.save()
    return Restful.result(data={'img_url': url})


# fitting room ========= model room ==========> drop personal photos
def drop_personal_photo(request):
    img_url = request.POST.get("img_url")
    personalphoto = PersonalPhotoModel.objects.filter(img_url=img_url)
    exist = personalphoto.exists()
    if exist:
        personalphoto.delete()
        return Restful.ok()
    else:
        return Restful.paramserror(message="亲~您要删除的照片不存在哦！请刷新页面重试")


# 购买服装
@msyb_login_required
def cloth_order(request, cloth_id):
    clothcategorys = clothCategory.objects.all()
    cloth = Clothes.objects.get(pk=20)
    order = ClothesOrder.objects.create(cloth=cloth, buyer=request.user, status=1, amount=cloth.price)
    # 注意这里不是使用filter，而是使用get()一步到位。
    context = {
        "goods": {
            'thumbnail': cloth.thumbnail,
            'shop': cloth.shop,
            'title': cloth.title,
            'desc': cloth.desc,
            'price': cloth.price,
        },
        "clothcategorys": clothcategorys,
        # "cloth": cloth,
        "order": order,
        "notify_url": request.build_absolute_uri(reverse("clothes:notify_url")),
        "return_url": request.build_absolute_uri(reverse("clothes:return_url"))
    }
    return render(request, 'clothes/cloth_order.html', context=context)


@msyb_login_required
@csrf_exempt
def cloth_order_key(request):
    goodsname = request.POST.get("goodsname")
    istype = request.POST.get("istype")
    notify = request.POST.get("notify_url")
    orderid = request.POST.get("orderid")
    price = request.POST.get("price")
    return_url = request.POST.get("return_url")

    token = '81564749e8d14a486497f4f1dcb275f0'
    uid = '7225b2942ecc238ffdaf705a'
    orderuid = str(request.user.pk)

    key = md5((goodsname + istype + notify + orderid + orderuid + price + return_url + token + uid).encode(
        "utf-8")).hexdigest()
    return Restful.result(data={"key": key})


# return_url作用：支付宝处理完成后，浏览器当前页面自动跳转回商户网站中指定页面的http路径，同时返回订单信息。
# notify_url作用：支付宝服务器主动通知商户网站里指定页面路径，返回订单信息。

@csrf_exempt
def notify_url(request):
    orderid = request.POST.get('orderid')
    istype = request.POST.get('istype')
    ClothesOrder.objects.filter(pk=orderid).update(status=2, istype=istype)
    return Restful.ok()


# return_url
@csrf_exempt
def profile(request):
    clothcategorys = clothCategory.objects.all()
    clothes = Clothes.objects.order_by("-pub_time")[0:3]
    orders = ClothesOrder.objects.filter(buyer=request.user).all()
    for order in orders:
        cloths = Clothes.objects.filter(pk=order.cloth_id).all()
        context = {
            'clothcategorys': clothcategorys,
            'orders': orders,
            'cloths': cloths,
            'clothes': clothes
        }
        return render(request, 'clothes/profile.html', context=context)
    return render(request, 'clothes/profile.html')


@msyb_login_required
def profile_view(request):
    buyer = request.POST.get('buyer')
    user = request.user.pk
    status = request.POST.get('status')
    print(buyer)
    print(user)
    print(status)
    if status == 2 and buyer == user:
        return render(request, 'clothes/profile.html')
    else:
        return Restful.paramserror(message="不好意思~亲，您无法查看当前页面哦")


# 保存人体模型
@msyb_login_required
def people_model(request):
    user = request.user
    thumbnail = request.POST.get("thumbnail")
    PeopleModel.objects.create(user=user, thumbnail=thumbnail)
    return Restful.ok()


# 删除人体模型
def delete_model(request):
    thumbnail = request.POST.get("thumbnail")
    model = PeopleModel.objects.filter(thumbnail=thumbnail)
    if model:
        model.delete()
        return Restful.ok()
    else:
        return Restful.paramserror(message="亲~您删除的这个模型不存在哦~")


from datetime import datetime


# 对服装进行前景的提取
def grabCut(request):
    url = request.POST.get('thumbnail')
    img = io.imread(url)
    mask = np.zeros(img.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgbModel = np.zeros((1, 65), np.float64)

    # rect 定义包含前景的矩形，格式为：（x,y,w,h）
    # x，y:代表的是在x,y轴上从哪里开始确定是前景的区域
    # 而w，h则是确定这个包含前景趋于的矩形的大小
    rect = (20, 20, 700, 800)

    # 函数返回值是更新的mask, bgdmodel, fgbmodel
    # cv2.grabCut(img, mask, rect, bdgModel, fgbModel, interCount, mode)
    # img: 代表的是输入的图像；
    # mask： 代表的是掩模图像，用来确定哪些区域为背景，前景，或者是可能是前景或背景等。
    # rect: 确定包含前景的矩形的位置与大小；
    # bgdModel, fgbModel: 算法内部使用的数组，你只需要创建两个大小为（1， 65），数据类型为np.float64的数组
    # interCount: 算法的迭代次数；
    # mode: 可以设置为矩形模式：cv2.GC_INIT_WITH_RECT或者是cv2.GC_INIT_WITH_MASK也可以联合使用，这是用来确定我们进行修改的方式，矩形模式或者是掩模模式
    cv.grabCut(img, mask, rect, bgdModel, fgbModel, 5, cv.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img*mask2[:, :, np.newaxis]

    plt.imshow(img)
    # plt.colorbar()
    # 以下三行代码要放在plt.show()之前，plt.imshow()函数之后
    # 去掉x坐标的刻度
    plt.xticks([])
    # 去掉Y坐标轴的刻度
    plt.yticks([])
    # 去掉坐标轴
    plt.axis('off')
    path = "D:/Git02/Git01/DSFN/MSYB/cloth_models"
    # strftime函数生成格式化的日期：这样就可以创建一个名为20210523.jpg的文件
    filename = datetime.now().date().strftime('%Y%m%d') + ".jpg"
    #  将画图保存为图片
    cv.imwrite(os.path.join(path,filename), img)
    plt.show()



