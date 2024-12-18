from django.shortcuts import render , redirect
from .form import TransactionForm , TransactionFilterForm
from wallet.models import Wallet
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction , Category
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from rest_framework import viewsets , status
from .serializers import TransactionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TransactionFilter

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
            transactions = transactions.filter(amount__gt=0) #variz
        elif transaction_type == 'withdraw':
            transactions = transactions.filter(amount__lt=0)#bardasht
        if category:
           transactions = transactions.filter(category=category) 

    #تنظیم صفحه بندی:
    p = Paginator(transactions,5)
    page = request.GET.get('page')
    Tlist = p.get_page(page)



    # for transaction in transactions:
        # transaction.display_amount = abs(transaction.amount)
        # transaction.jalali_date = jdatetime.date.fromgregorian(date=transaction.date)
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions, 'form': form, 'Tlist':Tlist})


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


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user)
    
    def perform_create(self, serializer):
        wallet = serializer.validated_data['wallet']
        amount = serializer.validated_data['amount']

        #manteghe update dashboard:
        wallet.balance += amount
        wallet.save()

        serializer.save(wallet=wallet)

    def destroy(self, request, *args, **kwargs): #manteghe delet tarakonesh va update wallet
        instance = self.get_object()
        wallet = instance.wallet
        transaction_id = instance.id
        transaction_amount = instance.amount
        wallet.balance -= transaction_amount
        wallet.save()
        self.perform_destroy(instance)
        return Response(
            {
                "message": f"Transaction No.{transaction_id} with amount: {transaction_amount} was deleted. Wallet balance updated to {wallet.balance}."
            },
            status=status.HTTP_200_OK
        )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        wallet = instance.wallet
        old_amount = instance.amount
        new_amount = request.data.get('amount', old_amount)
        wallet.balance -= old_amount  
        wallet.balance += int(new_amount)
        wallet.save()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "message": f"Transaction No.{instance.id} updated successfully. Wallet balance updated to {wallet.balance}.",
                "transaction": serializer.data
                 },
            status=status.HTTP_200_OK
        )
