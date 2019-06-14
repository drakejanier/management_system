from django import forms
from .models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['Name', 'Unit', 'Quantity', 'List_Price', 'Category']
        
class PurchaseForm(forms.ModelForm):    
    class Meta:
        model = Purchase
        fields = ('Item', 'Supplier', 'Quantity','Cost', 'Total_Cost')
        
    # def __str__(self)

