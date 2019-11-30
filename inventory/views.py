from dal import autocomplete
from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, Category, Purchase
from sales.models import Sales, SalesList
from django.db.models import Avg, Count, Min, Sum, Q
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView,TemplateView, View
from django.views.generic.edit import FormView
from django.template.loader import get_template
from django.urls import reverse
from .forms import PurchaseForm, ProductForm, ProductFilterForm,PurchaseItemForm, SearchItemForm
from datetime import datetime, date
from .utils import render_to_pdf

# import autocomplete_light_registry

def print_products(request): #Print Product List
    template = get_template('pdf/products_pdf.html')
    get_item_list = Products.objects.all()    
    context = {
        "items" : get_item_list,
    }
    
    html = template.render(context)
    pdf= render_to_pdf('pdf/products_pdf.html', context)
    if pdf:
        response =  HttpResponse(pdf,content_type='application/pdf')
        filename = "Item_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
class GeneratePDF(View): #PRINT SAMPLE FOR CLASS VIEWS
    def get(self, request, *args, **kwargs):
        template = get_template('pdf/invoice.html')
        context = {
            "invoice_id" : 123,
            "customer_name" : "Jerome Janier",
            "amount" : 12333.99,
            "today" : "Today",            
        }
        
        html = template.render(context)
        pdf= render_to_pdf('pdf/invoice.html', context)
        if pdf:
            response =  HttpResponse(pdf,content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

def generate_pdf(request, *args, **kwargs): #PRINT SAMPLE FOR FUNCTIONS
    template = get_template('pdf/invoice.html')
    context = {
        "invoice_id" : 123,
        "customer_name" : "Jerome Janier",
        "amount" : 12333.99,
        "today" : "Today",            
    }    
    html = template.render(context)
    pdf= render_to_pdf('pdf/invoice.html', context)
    if pdf:
        response =  HttpResponse(pdf,content_type='application/pdf')
        filename = "Invoice_%s.pdf" %("12341231")
        content = "inline; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")

def home(request):
    if request.user.is_authenticated:
        
        search_request = request.GET.get('Item') #get searches
        if search_request:
            print(f"GET requested : {search_request}")
            search_item = Products.objects.get(pk=search_request)
            print(f"item searched as : {search_item}")
        else:
            search_item = ''
            
        purchases_today = Purchase.objects.filter(Date_Purchased__date=date.today())  
        sales_today = SalesList.objects.filter(SalesID__Date_Sold__date=date.today())  
        search_form = SearchItemForm()
        
        # print(purchases_today.count())
        context = { 
            'purchases' : purchases_today,
            'total_purchases': purchases_today.aggregate(Sum('Total_Cost'))['Total_Cost__sum'] or 0.00,
            'sales' : sales_today,
            'total_sales' : sales_today.aggregate(Sum('Total_Item_Price'))['Total_Item_Price__sum'] or 0.00,
            'title': 'Home', 
            'searchbox' : search_form,
            'search_item' : search_item,
            }
        
        return render(request, 'inventory/dashboard.html', context)
    else:
        return redirect('login')

def search_valid(param):
    return param != '' and param is not None
class SearchProducts(ListView):
    template_name = 'inventory/inventory.html'    
    model = Products
    context_object_name = 'items'
    paginate_by = 5
    
    def post(self, request, *args, **kwargs):        
        
        if self.request.POST.get('btn-print') == 'btn-print':
            print("print posted")
            template = get_template('pdf/products_pdf.html')
            # get_item_list = Products.objects.all()    
            context = {
                "items" : self.get_queryset(),
            }
            
            html = template.render(context)
            pdf= render_to_pdf('pdf/products_pdf.html', context)
            if pdf:
                response =  HttpResponse(pdf,content_type='application/pdf')
                filename = "Item_%s.pdf" %("12341231")
                content = "inline; filename='%s'" %(filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
        else:
            return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        search_form = ProductFilterForm()
        context = super(SearchProducts, self).get_context_data(**kwargs)
        total_assets = self.get_queryset().aggregate(Sum('List_Price'))['List_Price__sum'] or 0.00
        total_qty =  self.get_queryset().aggregate(Sum('Quantity'))['Quantity__sum'] or 0.00
        print(f'total assets = {total_assets}')
        
        context.update({    
            'title': 'Product List',
            'search_form':search_form,
            'total_assets':total_assets,
            'total_qty':total_qty,
        })
        return context
    
    def get_queryset(self):
        category_pk = self.request.GET.get('Category')
        search_name = self.request.GET.get('Name')
        search_unit = self.request.GET.get('Unit')
        total_assets = 0
        total_qty = 0
        
        qsearch = Products.objects.all()
        qfilter =''
        
        if search_valid(category_pk):
            qfilter = Q(Category=category_pk)            
        elif search_valid(search_name):
            
            if qfilter != '':
                qfilter |= Q(Name__icontains=search_name) 
            else:
                qfilter = Q(Name__icontains=search_name)
        elif search_valid(search_unit):            
            if qfilter != '':
                qfilter |= Q(Unit__icontains=search_unit) 
            else:
                qfilter = Q(Unit__icontains=search_unit)

        
        if qfilter != '':            
            qsearch = qsearch.filter(qfilter)
            # total_assets = qsearch.aggregate(Sum('List_Price'))['List_Price__sum'] or 0.00
            # total_qty =  qsearch.aggregate(Sum('Quantity'))['Quantity__sum'] or 0.00

            
        return qsearch

class ProductDetail(DetailView):
    model = Products
    template_name = 'inventory/product_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    
class ProductUpdate(UpdateView):  
    form_class = ProductForm
    template_name = 'inventory/product_details.html'
    queryset = Products.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().values('Name')
        return context
    
    def get(self, request, **kwargs):
        self.object = ProductUpdate.objects.get(id=self.request.id)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = Products.objects.get(id=self.kwargs['id'])
        return obj
    
    
class PurchasesListView(ListView):
    model = Purchase
    queryset = Purchase.objects.order_by('-Date_Purchased')
    template_name = 'inventory/purchase-list.html'
    context_object_name = 'purchases'
    paginate_by = 5
    
    def post(self, request, *args, **kwargs):        
        
        if self.request.POST.get('btn-print') == 'btn-print':
            print("print posted")
            # template = get_template('pdf/products_pdf.html')
            # get_item_list = Products.objects.all()    
            context = {
                "items" : self.get_queryset(),
            }
            
            # html = template.render(context)
            pdf= render_to_pdf('pdf/purchases_pdf.html', context)
            if pdf:
                response =  HttpResponse(pdf,content_type='application/pdf')
                filename = "Item_%s.pdf" %("12341231")
                content = "inline; filename='%s'" %(filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
        else:
            return self.get(request, *args, **kwargs)
    
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
        # print(f'form pk : {form_pk}')
        product_item = form.cleaned_data['Items']
        
        Purchase = form.save(commit=False)
        
        Purchase.Item = product_item
        Purchase.User = self.request.user
        Purchase.save()
        
        add_item = Products.objects.get(pk = product_item.pk) 
        add_item.Quantity = int(add_item.Quantity) + int(Purchase.Quantity)
        add_item.User = self.request.user
        add_item.save() #1
        
        messages.success(self.request,f'Item added. {product_item}')
        return super(PurchaseViewItem, self).form_valid(form)
    
def PurchaseNewItem(request):
    
    if request.method == 'POST':
        # print(f'posted')
        product_form = ProductForm(request.POST)
        purchase_form = PurchaseForm(request.POST)
        
        if product_form.is_valid() and purchase_form.is_valid():
            frm_qty = purchase_form.cleaned_data['Quantity']
            product_item = product_form.save(commit=False)     
            product_item.Quantity = frm_qty
            product_item.User = request.user
            product_item = product_form.save()
            
            Purchase = purchase_form.save(commit=False)
            
            Purchase.Item = product_item
            Purchase.User = request.user
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