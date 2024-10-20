from django.shortcuts import render , redirect
from .form import TransactionForm
from wallet.models import Wallet
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Transaction
@login_required

# Create your views here.

def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            wallet = Wallet.objects.get(user=request.user)

            if form.cleaned_data['transaction_type'] == 'withdraw':
                transaction.amount = -abs(transaction.amount)
                wallet.balance += transaction.amount
            else:
                transaction.amount = abs(transaction.amount)
                wallet.balance += transaction.amount

            transaction.wallet = wallet
            transaction.save()
            wallet.save()

            return redirect('wallet_dashboard')
    else:
        form = TransactionForm()

    return render(request, 'transactions/add_transaction.html', {'form': form})

def transactions_list(request):
    transactions = Transaction.objects.filter(wallet__user=request.user)
    for transaction in transactions:
        transaction.display_amount = abs(transaction.amount)
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})