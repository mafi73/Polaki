from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserSignUpForm
from django.contrib.auth import logout

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('wallet_dashboard')
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('wallet_dashboard') 
    else:
        form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form})
