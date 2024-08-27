from django.urls import path
from account.views import *

urlpatterns = [
    path('register/',ResgisterView.as_view()),
    path('login/',LoginView.as_view()),
]