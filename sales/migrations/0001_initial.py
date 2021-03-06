# Generated by Django 2.0 on 2019-07-03 15:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OR', models.IntegerField(default=0)),
                ('Customer', models.CharField(max_length=50)),
                ('Total_Sales', models.IntegerField(default=0, null=True)),
                ('Date_Sold', models.DateTimeField(default=datetime.datetime.now)),
                ('Date_Recorded', models.DateTimeField(default=datetime.datetime.now)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SalesList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField(default=0)),
                ('Total_Item_Price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('Item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Products')),
                ('SalesID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sales')),
            ],
        ),
        migrations.CreateModel(
            name='tempSalesList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField(default=0)),
                ('Item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventory.Products')),
            ],
        ),
    ]
