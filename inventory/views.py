from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, Category, Purchase
from django.db.models import Avg, Count, Min, Sum
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView,TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse
from .forms import PurchaseForm, ProductForm, ProductFilterForm
from datetime import datetime, date

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        purchases_today = Purchase.objects.filter(Date_Purchased__date=date.today())

        
        context = { 
            'purchases' : purchases_today,
            'total_purchases': purchases_today.aggregate(Sum('Total_Cost'))['Total_Cost__sum'] or 0.00,
            'title': 'Home', 
            }
        
        return render(request, 'inventory/dashboard.html', context)
    else:
        return redirect('login')
    


def ProductView(request): #TEMP GETTING OBSOLETE
    items = Products.objects.all()
    search_form = ProductFilterForm()
    
    context = {
        'items' : items,
        'title': 'Product List',
        'search_form':search_form,
    }

    return render(request, 'inventory/inventory.html', context)

class SearchProducts(ListView):
    template_name = 'inventory/inventory.html'    
    model = Products
    context_object_name = 'items'
    
    def get_context_data(self, **kwargs):
        search_form = ProductFilterForm()        
        
        context = super(SearchProducts, self).get_context_data(**kwargs)        
        context.update({    
            'title': 'Product List',
            'search_form':search_form,
        })
        return context
    
    def get_queryset(self):
        category_pk = self.request.GET.get('Category')
        search_name = self.request.GET.get('Name')
        search_unit = self.request.GET.get('Unit')
        
        if search_name and search_unit and category_pk:
            return Products.objects.filter(Name__icontains=search_name, Unit__icontains=search_unit, Category=category_pk)
        elif search_name and search_unit:
            return Products.objects.filter(Name__icontains=search_name, Unit__icontains=search_unit)
        elif search_name and category_pk:
            return Products.objects.filter(Name__icontains=search_name, Category=category_pk)
        elif search_unit and category_pk:
            return Products.objects.filter(Unit__icontains=search_unit, Category=category_pk)
        elif category_pk:
            return Products.objects.filter(Category=category_pk)
        elif search_name:
            return Products.objects.filter(Name__icontains=search_name)
        elif search_unit:
            return Products.objects.filter(Unit__icontains=search_unit)
        else:
            messages.info(self.request, f'')           
            return Products.objects.all()

class PurchasesListView(ListView):
    model = Purchase
    queryset = Purchase.objects.order_by('-Date_Purchased')
    template_name = 'inventory/purchase-list.html'
    context_object_name = 'purchases'    
    
    
def PurchaseView(request, pk): #TEMPORARY DELETE AFTER 0623
    p_item = get_object_or_404(Purchase, pk=pk)    
    form = PurchaseForm(instance=p_item)
    
    if request.method == 'POST':
        p_item = get_object_or_404(Purchase, pk=pk)
        form = PurchaseForm(request.POST)
        
        if form.is_valid():
            item = form.cleaned_data.get('Item')
            supplier = form.cleaned_data.get('Supplier')
            quantity = form.cleaned_data.get('Quantity')
            cost = form.cleaned_data.get('Cost')
            date_Purchased = form.cleaned_data.get('Date_Purchased')
            
            p_item.Item = item
            p_item.Supplier = supplier
            p_item.Quantity = quantity
            p_item.Cost = item
            p_item.Date_Purchased = item
            
            return redirect('product-list')
    
    return render(request, 'inventory/purchase.html', {'form':form})

def PurchaseAdd(request, pk):
    if pk==0:
        item_data = {}
        
    else:
        product_item = get_object_or_404(Products, pk=pk) #get form Item model with primary key    
        item_data = {'Item' : product_item}
    
    
    if request.method == "POST":
        form = PurchaseForm(request.POST)     
        purchase_qty = form['Quantity'].value()
        
        print("purcahse qty : " + purchase_qty)
        
        if form.is_valid():
            product_item = Products.objects.get(pk = pk)
            old_qty = product_item.Quantity
            
            new_qty = int(old_qty) + int(purchase_qty)
            print("new qty : " + str(new_qty))
            
            product_item.Quantity = new_qty
            
            
            
            product_item.save()
            print("product updated")
            
            form.save()
            
            return redirect('product-list')

    else: #IF GET
        purchase_form = PurchaseForm(initial=item_data)
        context  = {
            'purchase_form': purchase_form,
            'title' : 'Purchase'     
        }
        return render(request, 'inventory/purchase_add.html', context)

def PurchaseNewItem(request):
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        purchase_form = PurchaseForm(request.POST)
        user_reg = 'jerome'

        if product_form.is_valid() and purchase_form.is_valid():

            added_qty = product_form['Quantity'].value()
            #product_form.User = 'jerome'
            added_product = product_form.save()

            item_pk = added_product.pk
            product_item = Products.objects.get(pk = item_pk)
            
            add_purchase = purchase_form.save(commit=False)
            add_purchase.Item = product_item

            add_purchase.Quantity = added_qty
            add_purchase.save()
            
            messages.success(request, f'Added new product.')            
            return redirect('product-list')
        
        else:
            print("5")
            messages.success(request, f'Added new product.')            
            
    else:
        print("6")
        product_form = ProductForm()
        purchase_form = PurchaseForm()
        
    context = {
        'product_form' : product_form,
        'purchase_form' : purchase_form,
        'title' : 'ADD NEW PRODUCT'
    }
    
    return render (request, 'inventory/purchase_New.html', context)

def ProductDelete(request, pk):
    item = Products.objects.only('Name').get(pk=pk).Name
    Products.objects.filter(id=pk).delete()
    
    return redirect('product-list')
    messages.success(request, f'Deleted.')   

def PurchaseDelete(request, pk):
    item = Purchase.objects.only('Item').get(pk=pk).Item
    Purchase.objects.filter(id=pk).delete()
    
    return redirect('purchase-list')
    messages.success(request, f'Deleted.')   