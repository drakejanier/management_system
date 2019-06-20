from django import forms

from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from dal import autocomplete
from inventory.models import Products
# autocomplete_light.register(Branch, name = 'ClientAutocomplete',choices = Products.objects.all())

class SalesForm(forms.ModelForm):  
    
    class Meta:
        model = Sales
        fields = ('Customer', 'OR', 'Date_Sold', 'Total_Sales')        
        Date_Sold = forms.DateField( widget=forms.TextInput(attrs={'type': 'date'} ))   

class SalesListForm(forms.ModelForm):
    Items = forms.ModelChoiceField( #check FIELD         
        queryset=Products.objects.all(), #check MODEL
        widget=autocomplete.ModelSelect2(url='items-autocomplete',attrs={'autocomplete':'off',})
    )    
    class Meta:
        model = SalesList
        fields = ('Quantity', 'Total_Item_Price')
        
        
    

