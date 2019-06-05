from django.shortcuts import render
from .models import Inventory

# Create your views here.
def home(request):
    context = {
        'posts':Inventory.objects.all(),
        'title': 'Home'
    }
    return render(request, 'inventory/base.html', context)