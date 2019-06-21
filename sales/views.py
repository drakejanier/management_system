
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, FormView, View
from django.urls import reverse_lazy
from .models import Sales, tempSalesList
from inventory.models import Products, Purchase
from .forms import SalesForm,SalesListForm
from shapeshifter.views import MultiFormView

# Create your views here.

class SalesViewSolo(CreateView): #TEMP check if SalesVIEW is working
    template_name = 'sales/register.html'    
    # model = Sales
    form_class = SalesForm    
    context_object_name = 'sales'
    
def SalesView(request):
    sales_form = SalesForm()
    saleslist_form = SalesListForm()
    added_item = tempSalesList.objects.all()
    context = {
        'sales_form' : sales_form,
        'saleslist_form' : saleslist_form,
        'added_item' : added_item,
    }
    
    if request.method == 'POST':
        if request.POST.get("button_add"):
            temp_saleslist = SalesListForm(request.POST)            
            
            
            if temp_saleslist.is_valid():   
                print(temp_saleslist.cleaned_data['Item'])
                
                temp_saleslist.save()
                messages.info(request, "added")    
                return redirect('sales-register')
            else:
                messages.info(request, temp_saleslist.errors)
        else:
            print("did not ")
    else:
        print("GET")
    
    return render(request, 'sales/register.html', context)
        
