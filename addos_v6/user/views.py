from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, EmailLoginForm
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'user/profile.html', {'user': user})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.nickname = form.cleaned_data['nickname']
            user.ip_address = form.cleaned_data['ip_address']
            user.save()
            login(request, user)
            return redirect('home:index')  # 로그인 후 메인 페이지로 리다이렉트
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home:index')  # 로그인 후 메인 페이지로 리다이렉트
    else:
        form = EmailLoginForm()
    return render(request, 'user/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('user:login')  # 로그아웃 후 로그인 페이지로 리다이렉트