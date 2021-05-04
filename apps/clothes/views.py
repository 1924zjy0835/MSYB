from django.shortcuts import render, redirect,reverse
from django.views.generic import View
from .forms import BuyerSayForm, PersonalPhotoForm, ClosetForm
from django.http import HttpResponse
import os
from django.conf import settings
from .models import PersonalPhotoModel, closet
from apps.cms.models import Clothes, clothCategory, Shop
from utils import Restful
from apps.msybauth.decorators import msyb_login_required


# index
def index(request):
    clothcategorys = clothCategory.objects.all()
    shops = Shop.objects.all()
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
def Search(request):
    return render(request, 'index/search.html')


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


# 商品详情
def detail(request):
    pk = request.POST.get("pk")
    cloth = Clothes.objects.filter(pk=pk)
    if not cloth:
        return Restful.paramserror(message='不好意思没有找到该商品的详情')
    else:
        return redirect(reverse('clothes:cloth_detail', kwargs={'cloth_id': pk}))


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


#  fitting room ============ closet room ===========>delete clothes
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
def cloth_order(request):
    # cloth = Clothes.objects.get(pk=cloth_id)
    # context = {
    #     "cloth": cloth
    # }
    return render(request, 'clothes/cloth_order.html')





