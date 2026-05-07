from accounts.models import MyUser as User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm


def user_login(request):

    if request.user.is_authenticated:

        return redirect("task_list")

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:

                login(request, user)
                return redirect("task_list")

            else:

                form.add_error(None, "username or password is incorrect")

    return render(request, "accounts/templates/index.html", context={"form": form})


def signup(request):

    if request.user.is_authenticated:
        return redirect("task_list")

    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                username=cd["username"], password=cd["password"], email=cd["email"]
            )
            login(request, user)
            return redirect("task_list")

    return render(request, "SignUp.html", {"form": form})


def user_log_out(request):
    logout(request)
    return redirect("task_list")
