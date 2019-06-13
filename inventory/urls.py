from django.urls import path
from .views import *
from . import views



urlpatterns = [
    path('', views.home, name='home-page'),
    path('productlist/', views.ProductView, name='product-list'), #leave blank to make as homepage
    # path('purchase-add/', PurchaseAdd.as_view(), name='purchase-add'),
        
    path('product-add/<int:pk>/', views.PurchaseView, name='product-add'),
    path('product-delete/<int:pk>/', views.ProductDelete, name='product-delete'),
    
    path('purchase-add/', views.PurchaseNewItem, name='purchase-add'),
    path('purchase-list', PurchasesListView.as_view(), name='purchase-list'), #list of Purchases
]