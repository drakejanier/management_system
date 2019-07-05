from django import forms
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from dal import autocomplete

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['Name', 'Unit', 'List_Price', 'Category']
        
class PurchaseForm(forms.ModelForm):    
    Items = forms.ModelChoiceField( #check FIELD (Items)      
        queryset=Products.objects.all(), #check MODEL
        required=False,
        widget=autocomplete.ModelSelect2(url='items-autocomplete',attrs={'autocomplete':'off',}),
    )
    
    class Meta:
        model = Purchase
        fields = ('Supplier', 'Quantity','Cost', 'Total_Cost')
        
class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('Item', 'Supplier', 'Quantity','Cost', 'Total_Cost')
        
    
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

class SearchItemForm(forms.Form):    
    
    
    Item = forms.ModelChoiceField( #check FIELD (Items)      
        queryset=Products.objects.all(), #check MODEL
        required=False,
        widget=autocomplete.ModelSelect2(url='items-autocomplete',attrs={'autocomplete':'off','data-placeholder': 'Search Item',}),
    )

    def __init__(self, *args, **kwargs):
        
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        # self.helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))      
        super(SearchItemForm, self).__init__(*args, **kwargs)
