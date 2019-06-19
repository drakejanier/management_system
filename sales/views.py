
from django.shortcuts import render
from django.views.generic import ListView, CreateView, FormView
from .models import Sales
from inventory.models import Products
from .forms import SalesForm

# Create your views here.

class SalesViewSolo(CreateView): #TEMP check if SalesVIEW is working
    template_name = 'sales/register.html'    
    # model = Sales
    form_class = SalesForm    
    context_object_name = 'sales'
    
def SalesView(request): #TEMPORARY DELETE AFTER 0623
    return render(request,'sales/register.html',{'title':'Sales Register'})

    # sales_form = SalesForm()
        
    # context  = {
    #     'sales_form': sales_form,
    #     'title' : 'Register Sales'     
    # }
    # return render(request, 'sales/register.html', context)