from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order, Customer, Tag
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
    for product in products:
        print(product.tags)
    categories = Product.objects.values_list('category', flat=True).distinct() # Get unique categories
    tags = Tag.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'tags': tags
    }
    return render(request, 'accounts/products.html', context)

def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': orders.count()
    }
    return render(request, 'accounts/customer.html', context)

def createCustomer(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        new_customer = Customer(name=name, phone=phone, email=email)
        new_customer.save()
    return redirect('home')

def createProduct(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        price = request.POST['price']
        tags = request.POST['tag']
        new_product = Product.objects.create(name=name, category=category, price=price)
        if tags:
            tag_list = tags.split(',')
            new_product.tags.set(Tag.objects.filter(name__in=tag_list))
    return redirect('product')