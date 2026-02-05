from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

# Create your views here. 
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username=username,password=password)
        if user:
            if not user.is_superuser:
                teacher = user.teacher
                teacher.check_subscription()
                if not teacher.is_active:
                    messages.error(request,"Your account is blocked. Please contact admin.")
                    return redirect("login")
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request,"Invalid username or password")
    return render(request, "accounts/login.html")

def logout_view(request):

    logout(request)
    return redirect("login")