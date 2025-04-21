from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    # User Registeration and Login
    path('register/', views.register, name='register'),
    path('empEmailVerification/', views.employeeEmailVerfication, name='empEmailVerification'),
    path('empRegister/', views.employeeRegisteration, name='empRegister'),
    path('login/', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('products/', views.products, name='product'),
    path('customer/<str:id>', views.customer, name='customer'),
    path('user/', views.userPage, name='user'),
    path('userProfile/', views.userProfilePage, name='userProfile'),

    # Create urls
    path('create_customer/', views.createCustomer, name='create-customer'),
    path('create_product/', views.createProduct, name='create-product'),
    path('create_tag/', views.createTag, name='create-tag'),
    path('create_order/', views.createOrder, name='create-order'),
    path('create_order/<str:id>', views.createOrderFromCustomerPage, name='create-order'),
    path('customer_create_order/', views.customerCreateOrder, name='customer-create-order'),

    # Update urls
    path('update_order/<str:id>', views.updateOrderDetails, name='update-order'),
    path('update_customer/<str:id>', views.updateCustomerDetails, name='update-customer'),
    path('update_product/<str:id>', views.updateProductDetails, name='update-product'),
    path('update_profile/', views.updateProfileDetails, name='update-user-profile'),

    # Delete urls
    path('delete_order/<str:id>', views.deleteOrder, name='delete-order'),
    path('delete_customer/<str:id>', views.deleteCustomer, name='delete-customer'),
    path('delete_product/<str:id>', views.deleteProduct, name='delete-product'),
    path('delete_tag/<str:id>', views.deleteTag, name='delete-tag'),

    # Password Recreate urls
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete.html'), name='password_reset_complete'),
]