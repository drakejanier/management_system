
from django.contrib import messages
from django.db.models import F
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
    
    if request.method == 'POST': #IF POSTED
        if request.POST.get("button_add"):
            temp_saleslist = SalesListForm(request.POST)          
            
            if temp_saleslist.is_valid():    #IF VALID  
                frm_qty = temp_saleslist.cleaned_data['Quantity']
                frm_item = temp_saleslist.cleaned_data['Item']
                item_qty = frm_item.Quantity                
                
                if frm_qty > 0 and frm_qty <= item_qty : #if 0 
                    
                    temp_saleslist.save() # << SUCCESS HERE
                    messages.success(request, "added")   
                    return redirect('sales-register')

                else:
                    messages.info(request, f"Invalid Quantity. Maximum Quantity is {item_qty}") 
                
            
            else: #IF NOT VALID
                messages.info(request, temp_saleslist.errors)
                
        elif request.POST.get("delete-item"): #IF ITEM DELETE
            messages.info(request, str(request.POST.get("delete-item")))
            
        else: #IF NOT INC CHOICE
            print("did not ")
    else:
        print("GET")
    
    return render(request, 'sales/register.html', context)

def ListItemDelete(request, pk):
    item = tempSalesList.objects.only('Item').get(pk=pk).Item
    messages.success(request, f'{item} deleted.')      
    tempSalesList.objects.filter(id=pk).delete()    
    return redirect('sales-register')

def itemAdd(request, pk):
    item_qty = tempSalesList.objects.filter(id=pk)
    item_qty.Quantity = item_qty.Quantity + 1
    item_qty.save()
    