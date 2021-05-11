from django.shortcuts import render, redirect,reverse
from django.views.generic import View
from .forms import BuyerSayForm, PersonalPhotoForm, ClosetForm
from django.http import HttpResponse
import os
from django.conf import settings
from .models import PersonalPhotoModel, closet
from apps.cms.models import Clothes, clothCategory, Shop, ClothesOrder
from utils import Restful
from apps.msybauth.decorators import msyb_login_required
from django.db.models import Q
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt


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
        clothes = closet.objects.all()
        context = {
            "photos": photos,
            "clothes": clothes
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
    context = {
        "photos": photos,
        "clothes": clothes,
        "clothcategorys": clothcategorys
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





