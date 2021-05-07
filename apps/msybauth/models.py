from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models


class UserManager(BaseUserManager):
    # 加了下划线的方法是被保护的，不能够在外部被调用，这个方法使用被创建用户的
    def _create_user(self, telephone, username, password, **kwargs):
        if not telephone:
            raise ValueError("请输入手机号！")
        if not username:
            raise ValueError('请输入用户名！')
        if not password:
            raise  ValueError("请输入密码！")

        # 使用user模型创建一个用户，手机号和用户名都可以直接传入，但是密码需经过加密处理
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        # 返回这个user就行
        return user

    # 这个方法是用来创建普通用户的
    def create_user(self, telephone, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone, username, password, **kwargs)

    # 创建超级用户
    def create_superuser(self, telephone, username, password,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone, username, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    # 我么不使用默认的自增长的主键
    # 使用uuid太长；可以使用shortuuid：比较短的uuid，即可以保持字段不会太长，又可以保持字段的唯一性；
    # 使用到第三方的一个包：通过：pip install shortuuidfield进行安装；
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11, unique=True)
    # password = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # auto_now_add为True就代表自从用户被创建保存在数据库中起就是其加入的时间
    date_joined = models.DateTimeField(auto_now_add=True)

    # 验证字段
    USERNAME_FIELD = 'telephone'
    # 在输入create_supperuser时就会让填写字段：username、telephone、password
    REQUIRED_FIELDS = ['username']
    # 用来给指定用户发送邮件
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username