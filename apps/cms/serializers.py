from rest_framework import serializers
from .models import Clothes, clothCategory


class ClothCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = clothCategory
        fields = ('id', 'name')


class ClothesSerializer(serializers.ModelSerializer):
    category = ClothCategorySerializer()

    class Meta:
        model = Clothes
        fields = ('id', 'title', 'desc', 'thumbnail', 'category', 'shop', 'price', 'pub_time')
