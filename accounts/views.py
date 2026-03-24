from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login , logout
from accounts.models import MyUser as User 
from django.urls import reverse , reverse_lazy
from .forms import LoginForm , SignupForm 

import uuid
from datetime import datetime

from random import randint  

def user_login(request):

    if request.user.is_authenticated:

        return redirect("home")
    
    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
             username = form.cleaned_data.get('username')
             password = form.cleaned_data.get("password")
             user = authenticate(request, username=username, password=password)
     
             if user is not None:

                    login(request, user)
                    return redirect("home") 
            
             else:
               
                form.add_error(None, "username or password is incorrect")
              
    return render(request, 'accounts/templates/index.html', context= {'form' : form}) 


from django.utils.http import urlencode

def signup(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = SignupForm()

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd["username"] , password=cd["password"] , email= cd["email"])
            login(request , user)

    return render(request, "SignUp.html", {"form": form})



def user_log_out(request):
    logout(request)  
    return redirect('home') 









'''class LoginFOrmView(FormView):
    template_name = 'accounts/templates/index.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "username or password is incorrect")
            return self.form_invalid(form)'''

     

# token = str(uuid.uuid4())
# User.objects.get_or_create