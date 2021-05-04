from django import forms
from front.forms import FormMixin


# 买家说
class BuyerSayForm(forms.Form):
    title = forms.CharField(min_length=6, max_length=100, label="标题", error_messages={"min_length": "最少不能少于6个字符！","max_length": "最长不能超过100个字符！"})
    content = forms.CharField(widget=forms.Textarea, label="内容", error_messages={"required": "必须输入内容！"})
    email = forms.EmailField(label="邮箱", error_messages={"required": "必须输入邮箱！"})
    reply = forms.BooleanField(required=False, label='是否需要回复')


# 上传个人照表单
class PersonalPhotoForm(forms.Form):
    pub_time = forms.DateTimeField()
    img_url = forms.URLField(required=True)


# 点击加入试衣间的验证表单
class ClosetForm(forms.Form, FormMixin):
    title = forms.CharField(max_length=100)
    thumbnail = forms.URLField(required=True)

