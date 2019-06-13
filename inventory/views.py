from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, Category, Purchase
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView,TemplateView
from django.views.generic.edit import FormView
from .forms import PurchaseForm, ProductForm

# Create your views here.
def home(request):
    context = {                
        'title': 'Home',
    }
    return render(request, 'inventory/base.html', context)

def ProductView(request):
    items = Products.objects.all()
    context = {
        'items' : items,
        'title': 'Product List'        
    }

    return render(request, 'inventory/inventory.html', context)

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

class PurchaseAdd(CreateView): #CHECK IF TEMP
    model = Purchase
    # form = PurchaseForm
    fields = ['Item', 'Supplier', 'Quantity', 'Cost', 'Date_Purchased']
    # template_Name = 'inventory/purchase.html'
    
    
    def form_valid(self, form): #overide the form valid method
        form.instance.user = self.request.user.id
        return super().form_valid(form)

def PurchaseNewItem(request):
        
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        purchase_form = PurchaseForm(request.POST)
        
        
        
        if product_form.is_valid() and purchase_form.is_valid():
            
            added_qty = product_form['Quantity'].value()
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
        product_form = ProductForm()
        purchase_form = PurchaseForm()
        
    context = {
        'product_form' : product_form,
        'purchase_form' : purchase_form,
    }
    
    return render (request, 'inventory/purchase_New.html', context)

def ProductDelete(request, pk):
    item = Products.objects.only('Name').get(pk=pk).Name
    Products.objects.filter(id=pk).delete()
    
    return redirect('product-list')
    messages.success(request, f'Deleted.')   
    