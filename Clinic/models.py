from django.db import models
from datetime import datetime


# Create your models here.
class Owner(models.Model):
    Name = models.CharField(max_length=50)
    Contact = models.IntegerField(default=0)
    Address = models.CharField(max_length=100)

    def __str__(self):
        return self.Name

    # def get_absolute_url(self):
    #     return reverse('product-list')


class Pet(models.Model):
    Owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    Sex = models.CharField(max_length=10)
    Birthday = models.DateTimeField(default=datetime.now)
    Species = models.CharField(max_length=25)
    Breed = models.CharField(max_length=50)
    Color = models.CharField(max_length=50)
    Source = models.CharField(max_length=50)

    def __str__(self):
        return '{0} {1}'.format(self.Name, self.Owner.Name)

    # def get_absolute_url(self):
    #     return reverse('product-list')
