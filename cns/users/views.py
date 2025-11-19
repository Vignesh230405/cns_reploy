from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import MyUsers
from django.contrib.auth.models import User
from .crypto.algorithms import encrypt, decrypt

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            raw_pass = form.cleaned_data["password"]
            algorithm = form.cleaned_data["algorithm"]

            encrypted, key = encrypt(raw_pass, algorithm)

            django_user = User.objects.create_user(username=username)

            MyUsers.objects.create(
                username=username,
                password=encrypted,
                algorithm=algorithm,
                key=key
            )
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            raw_pass = form.cleaned_data["password"]

            try:
                myuser = MyUsers.objects.get(username=username)
            except MyUsers.DoesNotExist:
                return render(request, "users/login.html", {"form": form, "error": "Invalid credentials"})

            if raw_pass.upper() == decrypt(myuser.password, myuser.algorithm, myuser.key):
                request.session["username"] = myuser.username
                return redirect("home")

            return render(request, "users/login.html", {"form": form, "error": "Invalid credentials"})
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        request.session.flush()
        return redirect("login")

    return render(request, "users/logout.html")
