from django.shortcuts import render
from .models import Wallet
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def wallet_dashboard(request):
    wallet = Wallet.objects.get(user=request.user)
    return render(request, 'wallets/dashboard.html', {'wallet': wallet})