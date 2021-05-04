from django import forms
from front.forms import FormMixin
from django.core.cache import cache
from .models import User


class LoginForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, error_messages={"max_length":"最大长度不能超过11个字符！"})
    password = forms.CharField(max_length=20, min_length=6, error_messages={"max_length": "最大长度不能超过20个字符！", "min_length" : "最短长度不能少于6个字符！"})
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11, error_messages={"max_length": "请确保您输入的手机号为11位", "min_length": "请确保您输入的手机号为11位！"})
    username = forms.CharField(max_length=20, min_length=4, error_messages={'max_length': "用户名不能超过20位字符！", 'min_length': "用户名不能少于4位字符！"})
    password1 = forms.CharField(max_length=20, min_length=6, error_messages={"max_length": "密码不能超过20位字符！", "min_length": "密码不能少于6位字符"})
    password2 = forms.CharField(max_length=20, min_length=6, error_messages={"max_length": "确认密码不能超过20位字符！", "min_length": "确认密码不能少于6位字符"})
    img_captcha = forms.CharField(max_length=6, min_length=6, error_messages={"max_length": "图片验证码为6位哦！", "min_length": "图片验证码为6位哦！"})

    # 重写父类的clean()方法，得到经过上面验证的数据
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        telephone = cleaned_data.get("telephone")
        # username = cleaned_data.get("username")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("两次输入的密码不一致！")

        # 判断图形验证码是否一致
        img_captcha = cleaned_data.get("img_captcha")
        cached_img_captcha = cache.get(img_captcha)
        # 判断是否可以通过用户输入的验证码在memecached缓存中拿到验证码，
        # 或者拿到的验证码是否和用户输入的一样，如果不同的话，就会抛出一个异常
        if not cached_img_captcha or cached_img_captcha != img_captcha:
            raise forms.ValidationError("图形验证码不正确！")

        # 判断用户注册的手机号是否已经注册过了
        telephone_exist = User.objects.filter(telephone=telephone).exists()
        if telephone_exist:
            raise forms.ValidationError("该手机号已经被注册过了！")

        #判断用户输入的用户名是否已经被注册过了
        # username_exist =



