from django.shortcuts import render , redirect
from .form import TransactionForm , TransactionFilterForm
from wallet.models import Wallet
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction , Category
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
# import jdatetime


# Create your views here.
@login_required
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

@login_required
def transactions_list(request):
    form = TransactionFilterForm(request.GET or None)

    transactions = Transaction.objects.filter(wallet__user=request.user).order_by('-date')
    if form.is_valid():
        transaction_type = form.cleaned_data.get('transaction_type')
        category = form.cleaned_data.get('category')
        if transaction_type == 'deposit':
            transactions = transactions.filter(amount__gt=0)
        elif transaction_type == 'withdraw':
            transactions = transactions.filter(amount__lt=0)
        if category:
           transactions = transactions.filter(category=category) 
    # for transaction in transactions:
        # transaction.display_amount = abs(transaction.amount)
        # transaction.jalali_date = jdatetime.date.fromgregorian(date=transaction.date)
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions, 'form': form})


@login_required
def update_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id = transaction_id , wallet__user=request.user)
    wallet = transaction.wallet
    initial_amount = transaction.amount
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, )
        if form.is_valid():
            form.save(commit=False)
        wallet.balance -= initial_amount
        if form.cleaned_data['transaction_type'] == 'withdraw':
            transaction.amount= -abs(transaction.amount)
        else:
            transaction.amount = abs(transaction.amount)
        wallet.balance += transaction.amount
        transaction.save()
        wallet.save()
        return redirect('transaction_list')
    else:
        transaction.amount = abs(transaction.amount)
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/update_transaction.html', {'form': form})


@login_required
def delet_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id = transaction_id , wallet__user=request.user)
    wallet = transaction.wallet
    if request.method == 'POST':
        wallet.balance -= transaction.amount
        transaction.delete()
        wallet.save()
        return redirect('transaction_list')
    return render(request, 'transactions/delete_transaction.html', {'transaction': transaction})