from django.db import models
from inventory.models import Products
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Sales(models.Model):
    Item = models.ForeignKey(Products, on_delete=models.CASCADE)
    Customer = models.CharField(max_length=50)
    Quantity = models.IntegerField(default=0) #should be delete after sales list
    List_Price = models.DecimalField(max_digits=6, decimal_places=2, default=0) #should be delete after sales list
    Total_Sales = models.IntegerField(default=0)
    Date_Sold = models.DateTimeField(default=datetime.now)
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return '{0} {1}'.format(self.Item, self.Date_Sold)
    
    def get_absolute_url(self):        
        return reverse('product-list')

class SalesList(models.Model):
    Item = models.ForeignKey(Products, on_delete=models.CASCADE)
    Sales_ID = models.ForeignKey(Sales, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)
    Price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    def __str__(self):
        return '{0} {1}'.format(self.Sales_ID, self.Item)
    