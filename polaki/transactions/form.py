from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    TRANSACTION_CHOICES = [
        ('deposit', 'واریز'),  
        ('withdraw', 'برداشت'),  
    ]

    transaction_type = forms.ChoiceField(choices=TRANSACTION_CHOICES, label="Transaction Type")
    
    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'description' , 'transaction_type'] #'transaction_type'