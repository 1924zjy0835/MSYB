from django.db import models
from apps.msybauth.models import User
from shortuuidfield import ShortUUIDField


class PersonalPhotoModel(models.Model):
    # 将用户上传的个人照按照手机号排列
    uid = ShortUUIDField(primary_key=True)
    pub_time = models.DateTimeField(auto_now_add=True)
    img_url = models.URLField()

    class Meta:
        db_table = "photos"
        ordering = ["-pub_time"]


#  储衣间模型
class closet(models.Model, ):
    title = models.CharField(max_length=100)
    thumbnail = models.URLField()

    class Meta:
        db_table = "closet"
