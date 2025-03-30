from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Order, Customer

# Create your views here.

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_customers = customers.count()
    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()
    
    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending
    }

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products' : products})

def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': orders.count()
    }
    return render(request, 'accounts/customer.html', context)
