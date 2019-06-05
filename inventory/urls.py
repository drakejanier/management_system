from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'), #leave blank to make as homepage
]