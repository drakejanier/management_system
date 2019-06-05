from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Inventory(models.Model):
    Name = models.CharField(max_length=100)
    Unit = models.CharField(max_length=50)
    Quantity = models.IntegerField(default=0)
    Sell_Price = models.DecimalField(max_digits=6, decimal_places=2)

    content = models.TextField()
    Date_posted = models.DateTimeField(default=timezone.now)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
