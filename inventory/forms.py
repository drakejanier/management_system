from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['Name', 'Unit', 'Quantity', 'List_Price', 'Category']
        
class PurchaseForm(forms.ModelForm):    
    class Meta:
        model = Purchase
        fields = ('Item', 'Supplier', 'Quantity','Cost', 'Total_Cost')
        
    # def __str__(self)
    
class ProductFilterForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['Name', 'Unit', 'Category']
        
    def __init__(self, *args, **kwargs):      
        
        super(ProductFilterForm, self).__init__(*args, **kwargs)
        self.fields['Name'].required = False
        self.fields['Unit'].required = False
        self.fields['Category'].required = False
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Name',
                'Unit',
                'Category',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )

