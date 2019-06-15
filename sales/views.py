from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Sales

# Create your views here.

class SalesViewSolo(CreateView):
    model = Sales
    