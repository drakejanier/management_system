from django.db import models
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
    #Quantity = models.IntegerField(default=0)
    List_Price = models.DecimalField(max_digits=8, decimal_places=2)
    CategoryOpt = (
        ('food','Food'),
        ('medicine','Medicine'),
        ('treats','Treats'),
        ('accessories','Accessories'),
        ('soap','Soap'),
        ('cologne','Cologne'),
        ('others','Others'),
    )
    Category = models.ForeignKey('Category', on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return '{0} {1}'.format(self.Name, self.Unit)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


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
    
class Purchase(models.Model):
    Item = models.ForeignKey(Products, on_delete=models.CASCADE)
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)
    Cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    Total_Cost = models.IntegerField(default=0)
    Date_Purchased = models.DateTimeField(default=datetime.now)
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return '{0} {1}'.format(self.Item, self.Date_Purchased)
    
    def get_absolute_url(self):
        
        return reverse('product-list')
    



