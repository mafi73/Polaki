from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Wallet
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect





class WalletDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'wallet/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet, created = Wallet.objects.get_or_create(user=self.request.user, defaults={'balance': 0})
        context['wallet'] = wallet
        return context