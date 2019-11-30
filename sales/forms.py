from .models import *
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from dal import autocomplete
from datetime import datetime, date
from django import forms
from django.forms import Textarea, SelectDateWidget, DateField
from inventory.models import Products, Purchase
#import autocomplete_light
# autocomplete_light.register(Branch, name = 'ClientAutocomplete',choices = Products.objects.all())

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
        queryset=Products.objects.all(), #check MODEL
        required=False,
        widget=autocomplete.ModelSelect2(url='items-autocomplete',attrs={'autocomplete':'off',}),
    )
    class Meta:
        model = tempSalesList
        fields = ('Item', 'Quantity')
        
def first_date():
    today = datetime.today()
    return datetime.date(year=2019, month=7, day=1)

class date_search(forms.Form):    
    # first_day = f"{datetime.today().month}/1/{datetime.today().year}"
    # date_start = forms.DateField(initial=first_day, widget=DatePickerInput(format='%m/%d/%Y',attrs={"class": "form-control"}))
    # date_end = forms.DateField(initial=datetime.today(), widget=DatePickerInput(format='%m/%d/%Y',attrs={"class": "form-control"}))
    date_start = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y',attrs={"class": "form-control"}))
    date_end = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y',attrs={"class": "form-control"}))