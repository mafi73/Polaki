from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.IntegerField
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.category}"
    

# Create your models here.
