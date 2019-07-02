
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, FormView, View
from django.urls import reverse_lazy
from .models import Sales, tempSalesList, SalesList
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
    product_count = tempSalesList.objects.count()
    qty = tempSalesList.objects.all().aggregate(total_qty=Sum('Quantity'))  
    total_qty = qty.get('total_qty')
    
    total_price = 0
    for item in added_item:
        total_price = total_price + int(item.get_total_item())

    print (total_price)
    
    context = {
        'sales_form' : sales_form,
        'saleslist_form' : saleslist_form,
        'added_item' : added_item,
        'product_count' : product_count,
        'total_quantity' : total_qty,
        'total_price' : total_price,
    }
    
    if request.method == 'POST': #IF POSTED
        if request.POST.get("button_add"): #if button ADD is called
            temp_saleslist = SalesListForm(request.POST)          
            
            if temp_saleslist.is_valid():    #IF VALID  
                frm_qty = temp_saleslist.cleaned_data['Quantity']
                frm_item = temp_saleslist.cleaned_data['Item']
                item_qty = frm_item.Quantity                
                
                if frm_qty > 0 and frm_qty <= item_qty : #if 0 
                    
                    temp_saleslist.save() # << item add SUCCESS HERE
                    messages.success(request, "added")   
                    return redirect('sales-register')

                else:
                    messages.info(request, f"Invalid Quantity. Maximum Quantity is {item_qty}")                 
            
            else: #IF NOT VALID
                messages.info(request, temp_saleslist.errors)                
                
        elif request.POST.get("button_register"): #if Sales is SAVED
            sales_info = SalesForm(request.POST) #pass form
            
            if sales_info.is_valid() and total_qty > 0:
                sales_reg = sales_info.save(commit=False)
                sales_reg.Total_Sales = total_price
                sales_reg.User = request.user
                sales_reg.save() #<<<<<<<<<<<<<<<< SALES saved here 
                sales_id = sales_reg.pk
                item_instance = Sales.objects.get(pk=sales_id)
                                
                temp_list = tempSalesList.objects.all()                
                
                for obj in temp_list:
                    sales_list = SalesList()
                    sales_list.SalesID = item_instance
                    sold_item = getattr(obj, 'Item')
                    sold_qty = getattr(obj, 'Quantity')
                    
                    sales_list.Item = sold_item
                    sales_list.Quantity = sold_qty
                    sales_list.Total_Item_Price = obj.get_total_item()
                    sales_list.save()  # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SALES LIST SAVED
                    
                    #deduct in Purchase Quantity
                    print(f'item pk = {sold_item.pk}')
                    item_purchase = Products.objects.get(pk = sold_item.pk) #search item in Purchase
                    item_purchase.Quantity = int(item_purchase.Quantity) - sold_qty
                    item_purchase.save()
                    
                tempSalesList.objects.all().delete() # templist DELETED
                messages.success(request, f'Items Saved')
                return redirect('sales-register')

            else:
                messages.info(request, f"Invalid form {sales_info.errors}. {total_qty}")
                
            
        elif request.POST.get("delete-item"): #IF ITEM DELETE
            messages.info(request, str(request.POST.get("delete-item")))
            
        else: #IF NOT IN CHOICEs
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
    item = tempSalesList.objects.get(pk=pk)
    item_qty = item.Quantity
    max_limit = item.Item.Quantity
    
    new_qty = item_qty + 1
    
    print(f'new qty {new_qty} is greater-de max_limit {max_limit}')
    if new_qty <= max_limit:
        item.Quantity = new_qty
        item.save()
    else:
        messages.info(request, 'max qty reached')
    
    return redirect('sales-register')

def itemDeduct(request, pk):
    item = tempSalesList.objects.get(pk=pk)
    item_qty = item.Quantity
    new_qty = item_qty - 1
    
    print(new_qty)
    if new_qty >= 0:
        item.Quantity = new_qty
        item.save()
    else:
        messages.info(request, 'min qty reached')
    
    return redirect('sales-register')
