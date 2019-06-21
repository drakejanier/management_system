
from django.shortcuts import render
from django.views.generic import ListView, CreateView, FormView, View
from django.urls import reverse_lazy
from .models import Sales
from inventory.models import Products, Purchase
from .forms import SalesForm,SalesListForm
from shapeshifter.views import MultiFormView

# Create your views here.

class SalesViewSolo(CreateView): #TEMP check if SalesVIEW is working
    template_name = 'sales/register.html'    
    # model = Sales
    form_class = SalesForm    
    context_object_name = 'sales'
    
class SalesView(MultiFormView):
    context_data = 'added_item'
    
    def get(self, *args, **kwargs):
        print('GET called.')
        # next_pk = Products.objects. #get next pk
        # user_profile_form = UserProfileForm(request.GET,initial={'Sales_ID' : NORMAL_USER})
        
        sales_form = SalesForm()
        saleslist_form = SalesListForm()
        context = {
            'sales_form' : sales_form,
            'saleslist_form' : saleslist_form,
        }
        
        return render(self.request, 'sales/register.html', context)
    
    def get_initial(self):
        purchase_item = get_object_or_404(Purchase, pk=self.kwargs['pk'])
        
        return {
            'Items':purchase_item,
            'Cost' : purchase_item.List_Price,
        }    
    
    def get_queryset(self):
        add_item = self.request.GET.get('Item')
        
        if add_item:
            return Purchase.objects.filter(Item__icontains=add_item)
        