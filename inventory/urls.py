from django.urls import path
from django.conf.urls import include, url
from .views import *
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('home/', views.home, name='dashboard'),
    url(r'^items-autocomplete/$', getItemList.as_view(), name='items-autocomplete',),

    path('productlist/', SearchProducts.as_view(), name='product-list'),    
    path('product-details/<int:pk>/', ProductDetail.as_view(), name='product-details'),    
    path('product-new/', views.PurchaseNewItem, name='product-new'),
    path('product-delete/<int:pk>/', views.ProductDelete, name='product-delete'),
    # url(r'^pdf/$', GeneratePDF.as_view()),
    # path('pdf/',GeneratePDF.as_view(), name='pdf'),
    path('pdf/',views.generate_pdf, name='pdf'),
    path('pdf-products/',views.print_products, name='pdf-products'),
    
    
    path('purchase-view/', views.PurchaseView, name='purchase-view'),
    path('purchase-view/<int:pk>/', PurchaseViewItem.as_view(), name='purchase-view-pk'),
    
    path('purchase-list/', PurchasesListView.as_view(), name='purchase-list'), #list of Purchases
    path('purchase-delete/<int:pk>/', views.PurchaseDelete, name='purchase-delete'),
    
]