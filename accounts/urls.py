from django.urls import path
from .views import *

urlpatterns = [
    path('login/',user_login , name="login") ,
    path("signup/", signup , name="signup"),
    path("logout",user_log_out , name= "logout"),
]