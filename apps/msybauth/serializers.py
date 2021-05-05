
from rest_framework import serializers
from apps.msybauth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('uid', 'telephone', 'email', 'username', 'is_active', 'is_staff')