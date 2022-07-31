from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Dishes(models.Model):
    name=models.CharField(max_length=150)
    options = (
        ("veg", "veg"),
        ("nonveg", "nonveg")

    )
    category=models.CharField(max_length=150,choices=options,default="veg")
    price=models.PositiveIntegerField()
    image=models.ImageField(upload_to="images",null=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.IntegerField()
    review=models.CharField(max_length=150,null=True)
    review_date=models.DateTimeField(auto_now_add=True)

