
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
    sales_form = SalesForm()
        
    context  = {
        'sales_form': sales_form,
        'title' : 'Register Sales'     
    }
    return render(request, 'sales/register.html', context)
    
# class getItemList(autocomplete.Select2QuerySetView): #move to inventory for global
#     print("CALLED")
    
#     def get_queryset(self):
#         print("querried")
        
        

#         if self.q:
#             print("2")
#             items = Products.objects.filter(Name__istartswith=self.q)
#         return items

