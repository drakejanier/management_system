from django import forms

from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from dal import autocomplete
from inventory.models import Products

class SalesForm(forms.ModelForm):
    Items = forms.ModelChoiceField( #check FIELD 
        
        queryset=Products.objects.all(), #check MODEL
        widget=autocomplete.ModelSelect2(url='items-autocomplete',attrs={'autocomplete':'off',})
    )
    
    class Meta:
        model = Sales
        fields = ('Customer', 'Quantity', 'List_Price', 'Total_Sales')
