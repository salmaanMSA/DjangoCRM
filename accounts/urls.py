from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='product'),
    path('customer/<str:id>', views.customer, name='customer'),
    path('create_customer/', views.createCustomer, name='create-customer'),
    path('create_product/', views.createProduct, name='create-product')
]