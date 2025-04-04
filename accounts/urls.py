from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='product'),
    path('customer/<str:id>', views.customer, name='customer'),

    # Create urls
    path('create_customer/', views.createCustomer, name='create-customer'),
    path('create_product/', views.createProduct, name='create-product'),
    path('create_tag/', views.createTag, name='create-tag'),
    path('create_order/', views.createOrder, name='create-order'),

    # Update urls
    path('update_order/<str:id>/', views.updateOrderDetails, name='update-order'),
    path('update_customer/<str:id>/', views.updateCustomerDetails, name='update-customer'),

    # Delete urls
    path('delete_order/<str:id>/', views.deleteOrder, name='delete-order'),
    path('delete_customer/<str:id>/', views.deleteCustomer, name='delete-customer')
]