from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order, Customer, Tag
# Create your views here.

# Template Rendering Views

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    products = Product.objects.all()
    total_orders = orders.count()
    total_customers = customers.count()
    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()
    
    context = {
        'orders': orders,
        'customers': customers,
        'products': products,
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


# Create Operation Views

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

def createTag(request):
    if request.method == 'POST':
        tagName = request.POST['tagName']
        new_tag = Tag(name=tagName)
        new_tag.save()
    return redirect('product')

def createOrder(request):
    if request.method == 'POST':
        customer_name = request.POST['customer']
        product_name = request.POST['product']
        status = request.POST['status']
        customer = Customer.objects.get(name=customer_name)
        product = Product.objects.get(name=product_name)
        new_order = Order(customer=customer, product=product, status=status)
        new_order.save()
    return redirect('home')


# Update Operation Views

def updateOrderDetails(request, id):
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        upd_product = request.POST.get('product_upd_order', None) 
        upd_status = request.POST.get('status_upd_order', None)
        if upd_product is not None:
            order.product = Product.objects.get(name=upd_product)
        if upd_status is not None:
            order.status = upd_status
        order.save()
    return redirect('home')

def updateCustomerDetails(request, id):
    if request.method == 'POST':
        customer = Customer.objects.get(id=id)
        upd_name = request.POST.get('customer_name', None)
        upd_phone = request.POST.get('customer_phone', None)
        if upd_name is not None:
            customer.name = upd_name
        if upd_phone is not None:
            customer.phone = upd_phone
        customer.save()
    return redirect('customer', id=id)



# Delete Operation Views

def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
    return redirect('home')

def deleteCustomer(request, id):
    customer = Customer.objects.get(id=id)
    if request.method == 'POST':
        customer.delete()
        print("deleted")
    print("problem")
    return redirect('home')