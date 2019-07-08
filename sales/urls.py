from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('register/<int:pk>/', views.SalesView, name='sales-register'),
    
    path('list-item-delete/<int:pk>/', views.ListItemDelete, name='list-item-delete'),
    path('list-item-add/<int:pk>/', views.itemAdd, name='list-item-add'),
    path('list-item-deduct/<int:pk>/', views.itemDeduct, name='list-item-deduct'),

    path('sales-summary/', SalesSummary.as_view(), name='sales-summary'),
    # url(r'^items-autocomplete/$', getItemList.as_view(), name='items-autocomplete',), #move to inventory
]
