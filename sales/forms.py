from django import forms
from django.forms import Textarea, SelectDateWidget, DateField

from .models import *
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from dal import autocomplete
from inventory.models import Products, Purchase
#import autocomplete_light

#autocomplete_light.register(Branch, name = 'ClientAutocomplete',choices = Products.objects.all())

class SalesForm(forms.ModelForm):      
    class Meta:
        model = Sales
        fields = ('Customer', 'OR', 'Date_Sold')        
        Date_Sold = forms.DateField( widget=forms.TextInput(attrs={'type': 'date'} ))
        widgets = {
            'Date_Sold': DatePickerInput(format='%m/%d/%Y'),            
        }

class SalesListForm(forms.ModelForm):
    Item = forms.ModelChoiceField( #check FIELD (Items)      
        queryset=Purchase.objects.all(), #check MODEL
        required=False,
        widget=autocomplete.ModelSelect2(url='items-autocomplete',attrs={'autocomplete':'off',}),
    )
    class Meta:
        model = tempSalesList
        fields = ('Item', 'Quantity')
        

        
        
        
    

