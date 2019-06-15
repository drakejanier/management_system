from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('sales/', SalesViewSolo.as_view(), name='sales-view'),
]
