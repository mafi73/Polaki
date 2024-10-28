from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    TRANSACTION_CHOICES = [
        ('deposit', 'واریز'),  
        ('withdraw', 'برداشت'),  
    ]

    transaction_type = forms.ChoiceField(choices=TRANSACTION_CHOICES, label="نوع تراکنش")
    
    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'description' , 'transaction_type'] 
        labels = {
            'amount' : 'مبلغ',
            'category' : 'دسته بندی',
            'description' : 'توضیحات',
            'transaction_type' : 'نوع تراکنش',
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount == 0:
            raise forms.ValidationError("مقدار تراکنش نمی‌تواند صفر باشد.")
        return amount