from django.urls import path
from . import views

#  应用命名空间
app_name = 'clothes'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/products/<int:category_id>/', views.index_new_products, name='new_products'),
    path('search/', views.Search, name='search'),
    path('buyer/say/', views.Buy_say_view.as_view(), name='buyer_say'),
    path('detail/', views.detail, name='detail'),
    path('cloth/detail/<int:cloth_id>/', views.cloth_detail, name='cloth_detail'),
    path('closet/room/', views.closet_room, name='closet_room'),
    path('drop/closet/cloth/', views.drop_closet_cloth, name='drop_closet_cloth'),
    path('model/room/', views.fitting_room, name='fitting_room'),
    path('upload/person/photo/', views.upload_personal_photo, name='upload_person_photo'),
    path('drop/personal/photo/', views.drop_personal_photo, name='drop_personal_photo'),
    path('cloth/order/', views.cloth_order, name='cloth_order'),
]

