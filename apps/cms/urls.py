from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path("", views.cms_index, name="index"),
    path("shop/", views.shop, name="shop"),
    path("add/shop/", views.add_shop, name="add_shop"),
    path("edit/shop/", views.edit_shop, name="edit_shop"),
    path("delete/shop/", views.delete_shop, name="delete_shop"),
    path("upload/file/", views.upload_file, name="upload"),
    path("publish/cloth/", views.Publish_cloth.as_view(), name="publish"),
    path("category/cloth/", views.category_cloth, name="category"),
    path("add/category/cloth/", views.add_category_cloth, name="add_category"),
    path("edit/category/cloth/", views.edit_category_cloth, name="edit_category"),
    path("delete/category/cloth/", views.delete_category_cloth, name="delete_category"),
    path("qntoken/", views.qntoken, name='qntoken'),
    path("add/model/", views.add_model, name="add_model"),
]
