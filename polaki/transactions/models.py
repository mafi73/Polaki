from django.db import models
from django.contrib.auth.models import User
from wallet.models import Wallet
import jdatetime

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'واریز'),
        ('withdraw', 'برداشت'),
    ]
    wallet=models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount=models.BigIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    # transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw')], default='withdraw')
    
    def display_amount(self):
        return abs(self.amount)
    
    def jalali_date(self):
        return jdatetime.date.fromgregorian(date=self.date)
    
    def __str__(self):
        return f"{self.wallet.user.username} - {self.amount} - {self.category}" #- {self.transaction_type}"
    

# Create your models here.
