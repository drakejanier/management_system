from dal import autocomplete
from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, Category, Purchase
from sales.models import Sales, SalesList
from django.db.models import Avg, Count, Min, Sum
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView,TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse
from .forms import PurchaseForm, ProductForm, ProductFilterForm,PurchaseItemForm
from datetime import datetime, date

# Create your views here.

def home(request):
    if request.user.is_authenticated:        
        purchases_today = Purchase.objects.filter(Date_Purchased__date=date.today())  
        sales_today = SalesList.objects.filter(SalesID__Date_Sold__date=date.today())  
        
        print(purchases_today.count())
        context = { 
            'purchases' : purchases_today,
            'total_purchases': purchases_today.aggregate(Sum('Total_Cost'))['Total_Cost__sum'] or 0.00,
            'sales' : sales_today,
            'total_sales' : sales_today.aggregate(Sum('Total_Item_Price'))['Total_Item_Price__sum'] or 0.00,
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
    
def PurchaseView(request): #if Purchase is clicked
    context = {
        'form' : PurchaseForm(),
        'title' : 'ADD NEW PRODUCT',
    }    
    return render (request, 'inventory/purchase_add.html', context)

class PurchaseViewItem(CreateView): #Purchase with item
    #model = Purchase
    form_class = PurchaseForm
    template_name = 'inventory/purchase_add.html' 
    #context_data = 'purchase_form'
    #print("pk : " + pk)
    
    def get_initial(self):
        product_item = get_object_or_404(Products, pk=self.kwargs['pk'])
        
        return {
            'Items':product_item,
            'Cost' : product_item.List_Price,
        }
        
    def form_valid(self, form):
        form_pk = form.cleaned_data['Items']
        print(f'form pk : {form_pk}')
        product_item = form.cleaned_data['Items']
        
        Purchase = form.save(commit=False)
        
        Purchase.Item = product_item
        Purchase.User = self.request.user
        Purchase.save()
        
        print(f'prd : {product_item.pk} ')
        add_item = Products.objects.get(pk = product_item.pk) 
        add_item.Quantity = int(add_item.Quantity) + int(Purchase.Quantity)
        add_item.save() #1
        
        messages.success(self.request,f'Item added. {product_item}')
        return super(PurchaseViewItem, self).form_valid(form)
    
def PurchaseNewItem(request):
    
    if request.method == 'POST':
        print(f'posted')
        product_form = ProductForm(request.POST)
        purchase_form = PurchaseForm(request.POST)
        
        if product_form.is_valid() and purchase_form.is_valid():
            frm_qty = purchase_form.cleaned_data['Quantity']
            product_item = product_form.save(commit=False)     
            product_item.Quantity = frm_qty
            product_item = product_form.save()
            
            Purchase = purchase_form.save(commit=False)
            
            Purchase.Item = product_item
            Purchase.save()
            
            messages.success(request, f'Saved {product_item}.')
            return redirect('product-list')
        else:
            messages.error(request, f'Form validation error {purchase_form.errors}.')
    else:
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
    
class getItemList(autocomplete.Select2QuerySetView):    
    def get_queryset(self):      
        items = None
        if self.q:
            items = Products.objects.filter(Name__istartswith=self.q)
        return items