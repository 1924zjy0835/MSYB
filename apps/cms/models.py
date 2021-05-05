from django.db import models
from shortuuidfield import ShortUUIDField


# 服装分类的模型
class clothCategory(models.Model):
    name = models.CharField(max_length=20, error_messages={"max_length": "服装分类最大长度不超过100个字符~！"})


class Shop(models.Model):
    # 默认店主就是当前已经登录的用户
    shopkeeper = models.CharField(max_length=20, error_messages={"max_length": "店主的昵称不能超过20个字符！"})
    name = models.CharField(max_length=20, error_messages={"max_length": "店铺名最大长度不超过20的字符！"})

    class Meta:
        db_table = 'shop'


# 发布服装的模型
class Clothes(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    price = models.FloatField()
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('clothCategory', on_delete=models.SET_NULL, null=True)
    shop = models.CharField(max_length=20, error_messages={'max_length': "店铺名的最大长度不能超过2-个字符！"}, null=False)

    class Meta:
        db_table = "clothes"
        ordering = ["-pub_time", "price"]


class ClothesOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    cloth = models.ForeignKey("Clothes", on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey("msybauth.User", on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 1:代表的是支付宝支付；2：代表的是微信支付；
    istype = models.SmallIntegerField(default=0)
    # 1： 代表的是未支付；2：代表的是已经支付成功；
    status = models.SmallIntegerField(default=1)