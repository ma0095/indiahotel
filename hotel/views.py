from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from hotel.serializers import DishSerializer,DishesModelSerializer,RegistrationSerializer
from hotel.models import Dishes
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions,authentication
from django.contrib.auth.models import User

# Create your views here.

class DishesView(APIView):
    def get(self,request,*args,**kwargs):
        all_dishes=Dishes.objects.all()
        serializer=DishSerializer(all_dishes,many=True)
        return Response(data=serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=DishSerializer(data=request.data)
        if serializer.is_valid():
            name=serializer.validated_data.get("name")
            category=serializer.validated_data.get("category")
            price=serializer.validated_data.get("price")
            Dishes.objects.create(name=name,category=category,price=price)
            return Response(data=serializer.data)

        else:
            return Response(data=serializer.errors)

class DishDetailsView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        dish=Dishes.objects.get(id=id)
        serializer=DishSerializer(dish)
        return Response(data=serializer.data)

    def put(self,request,*args,**kwargs):
        id = kwargs.get("id")
        instance = Dishes.objects.get(id=id)
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            category = serializer.validated_data.get("category")
            price = serializer.validated_data.get("price")
            instance.name=name
            instance.category=category
            instance.price=price
            instance.save()
            return Response(data=serializer.data)


    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        dish=Dishes.objects.get(id=id)
        dish.delete()
        return Response({"msg":"dish deleted"})



class MenuItemView(APIView):

    serializer_class=DishesModelSerializer


    def get(self,request,*args,**kwargs):
        all_dishes=Dishes.objects.all()
        serializer=self.serializer_class(all_dishes,many=True)
        return Response(data=serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class MenuDetailsView(APIView):
    serializer_class=DishesModelSerializer

    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        try:
            dish = Dishes.objects.get(id=id)
            serializer = self.serializer_class(dish)
            return Response(data=serializer.data)
        except:
            return Response({"msg":"invalid"},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        try:
            dish=Dishes.objects.get(id=id)
            dish.delete()
            return Response(data=request.data)
        except:
            return Response({"msg":"invalid"},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,*args,**kwargs):
        id = kwargs.get("id")
        instance = Dishes.objects.get(id=id)
        serializer = self.serializer_class(data=request.data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class SignupView(APIView):
    serializer_class=RegistrationSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
           # User.objects.create_user(**serializer.validated_data)

        else:
            return Response(data=serializer.errors)

class DishesViewsetView(viewsets.ViewSet):
    serializer_class=DishesModelSerializer
    def list(self,request,*args,**kwargs):
        dish=Dishes.objects.all()
        if "category" in request.query_params:
            category=request.query_params.get("category")
            dish=Dishes.objects.filter(category=category)
        if "price_lte" in request.query_params:
            price=request.query_params.get("price_lte")
            dish=Dishes.objects.filter(price__lte=price)
        serializer=DishesModelSerializer(dish,many=True)
        return Response(data=serializer.data)




    def create(self,request,*args,**kwargs):
        serializer=DishesModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        dish=Dishes.objects.get(id=id)
        serializer=DishesModelSerializer(dish)
        return Response(data=serializer.data)

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        instance=Dishes.objects.get(id=id)
        serializer=DishesModelSerializer(data=request.data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def destroy(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        dish = Dishes.objects.get(id=id)
        dish.delete()
        return Response({"msg":"dish deleted"})



class DishModelViewsetView(viewsets.ModelViewSet):
    serializer_class = DishesModelSerializer
    queryset =Dishes.objects.all()
    model=Dishes
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [authentication.BasicAuthentication]
    # permission_classes = [permissions.IsAuthenticated]