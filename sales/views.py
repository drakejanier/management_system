
from django.shortcuts import render
from django.views.generic import ListView, CreateView, FormView, View
from django.urls import reverse_lazy
from .models import Sales
from inventory.models import Products
from .forms import SalesForm,SalesListForm
from shapeshifter.views import MultiFormView

# Create your views here.

class SalesViewSolo(CreateView): #TEMP check if SalesVIEW is working
    template_name = 'sales/register.html'    
    # model = Sales
    form_class = SalesForm    
    context_object_name = 'sales'
    
class SalesView(MultiFormView):
    
    def get(self, *args, **kwargs):
        sales_form = SalesForm()
        saleslist_form = SalesListForm()        
        context = {
            'sales_form' : sales_form,
            'saleslist_form' : saleslist_form,
        }
        
        return render(self.request, 'sales/register.html', context)