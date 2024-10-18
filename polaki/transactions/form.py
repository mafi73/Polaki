from django import forms
from .models import Transaction
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'transaction_type', 'description']