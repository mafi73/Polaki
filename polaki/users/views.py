from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserSignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('wallet_dashboard') 
    else:
        form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form})
