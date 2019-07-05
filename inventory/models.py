from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django import forms
from phone_field import PhoneField
from datetime import datetime
# Create your models here.

class Products(models.Model):
    Name = models.CharField(max_length=50)
    Unit = models.CharField(max_length=50)
    Quantity = models.IntegerField(default=0)
    List_Price = models.DecimalField(max_digits=8, decimal_places=2)
    Category = models.ForeignKey('Category', on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return '{0} {1}'.format(self.Name, self.Unit)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def get_qty(self):
        qty = 0        
        qty = Purchase.objects.all().filter(Item=self.pk).aggregate(total_qty=Sum('Quantity'))  
        total_qty = qty.get('total_qty')
        
        return str(total_qty)

class Category(models.Model):
    Name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.Name
    
    class Meta:
        verbose_name_plural = "Categories"
    


class Supplier(models.Model):
    Name = models.CharField(max_length=50)
    Address = models.CharField(blank=True, max_length=100)
    Contact_No = models.CharField(blank=True, max_length=20)
    Email = models.EmailField(blank=True, max_length=254)
    
    def __str__(self):
        return self.Name
    
class Purchase(models.Model): #should be changed to ITEMS model
    Item = models.ForeignKey(Products, on_delete=models.CASCADE)
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)
    Cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Total_Cost = models.IntegerField(default=0)
    Date_Purchased = models.DateTimeField(default=datetime.now)
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return '{0} {1}'.format(self.Item, self.Cost)
    
    def get_absolute_url(self):        
        return reverse('product-list')
    



