from django import forms
from front.forms import FormMixin
from .models import Clothes


class EditClothCategory(forms.Form, FormMixin):
    pk = forms.IntegerField(required=True)
    name = forms.CharField(max_length=100, error_messages={"max_length" : "最大长度不超过100个字符！"})


class AddShop(forms.Form, FormMixin):
    name = forms.CharField(max_length=20, error_messages={"max_length": "店铺名最大长度不超过20的字符！"})


class EditShop(forms.Form, FormMixin):
    pk = forms.IntegerField(required=True)
    name = forms.CharField(max_length=20)


class PublishClothesForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()
    shop = forms.IntegerField()

    class Meta:
        model = Clothes
        exclude = ['category', 'pub_time']
        #  在介绍ModelForm时有介绍怎么定义error_message,可以再去看看