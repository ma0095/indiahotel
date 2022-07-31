from rest_framework import serializers
from hotel.models import Dishes
from django.contrib.auth.models import User

class DishSerializer(serializers.Serializer):
    name=serializers.CharField()
    category=serializers.CharField()
    price=serializers.IntegerField()


class DishesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Dishes
        fields="__all__"

    def validate(self, data):
        cost=data.get("price")
        if cost<0:
            raise serializers.ValidationError("invalid price")
        return data

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            "first_name", "last_name", "username", "email","password"
        ]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)