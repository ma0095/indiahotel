from rest_framework import serializers
from hotel.models import Dishes,Review
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

class ReviewSerializer(serializers.ModelSerializer):
    dish=DishesModelSerializer(many=False,read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Review
        fields=["dish","rating","comment","created_date","user"]

    def create(self,validated_data):
        user=self.context.get("user")
        dish=self.context.get("dish")
        return Review.objects.create(user=user,dish=dish,**validated_data)
