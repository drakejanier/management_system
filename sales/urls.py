from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('register/', views.SalesView, name='sales-register'),
    # url(r'^items-autocomplete/$', getItemList.as_view(), name='items-autocomplete',), #move to inventory
]
