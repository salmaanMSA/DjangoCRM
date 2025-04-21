from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order, Customer, Tag
from .filters import OrderFilter
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_user, admin_only
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
import smtplib

# Create your views here.

# Template Rendering Views

@unauthenticated_user # decorator used to restrict the acces for authenticated user
def register(request):
    form = CreateUserForm() # using django default user form
    if request.method == 'POST':
        form = CreateUserForm(request.POST) # getting datas from user form
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was Created for ' + username)
            return redirect('login')
    context = {
        'form' : form
    }
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def employeeEmailVerfication(request):
    if request.method == 'POST':
        userEmail = request.POST.get('email')

        if userEmail:
            subject = 'Welcome to Our Website'
            message = '''
                Thankyou for signing up with us, we have verified your company email.
                Now register your account in our CRM using the link below
                http://127.0.0.1:8000/empRegister/
             '''
            from_email = settings.EMAIL_HOST_USER  # Make sure it's the same email as the one in EMAIL_HOST_USER
            recipient_list = [userEmail]  # The recipient's email address

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'Verification email sent!')

            except smtplib.SMTPAuthenticationError as e:
                print("SMTP Authentication Error:", e)
                messages.error(request, f'Authentication error: {e}')

            except smtplib.SMTPException as e:
                print("SMTP Error:", e)
                messages.error(request, f'SMTP error occurred: {e}')

            except Exception as e:
                print("General Error:", e)
                messages.error(request, f'Unexpected error: {e}')
        else:
            messages.error(request, 'Please enter a valid email.')

    return render(request, 'accounts/staff_emailVerf.html')

@unauthenticated_user
def employeeRegisteration(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='admin')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'accounts/staff_registerForm.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            user_group = None
            if user.groups.exists():
                user_group = user.groups.all()[0].name
            if user_group == 'admin':
                return redirect('home')
            else:
                return redirect('user')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@allowed_user(allowed_roles=['customer'])
def userPage(request):
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(customer=customer)
    products = Product.objects.all()
    total_orders = orders.count()
    total_orders_delivered = orders.filter(status='Delivered').count()
    total_orders_pending = orders.filter(status='Pending').count()
    context = {
        'orders' : orders,
        'products' : products,
        'total_orders': total_orders,
        'orders_delivered' : total_orders_delivered,
        'orders_pending' : total_orders_pending
    }
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
def userProfilePage(request):
    userInfo = Customer.objects.get(user=request.user)
    context = {
        'userInfo' : userInfo
    }
    return render(request, 'accounts/userProfile.html', context)

@login_required(login_url='login')
@admin_only
def home(request):
    print(request.user.groups.all()[0].name)
    orders = Order.objects.all()
    lastFiveOrders = orders.order_by('-date_created')[:5]
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

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def customer(request, id):
    customer = Customer.objects.get(id=id)
    products = Product.objects.all()
    orders = customer.order_set.all()
    orderFilters = OrderFilter(request.GET, queryset=orders)
    orders = orderFilters.qs
    context = {
        'customer': customer,
        'orders': orders,
        'products': products,
        'total_orders': orders.count(),
        'orderFilters': orderFilters
    }
    return render(request, 'accounts/customer.html', context)


# Create Operation Views

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createCustomer(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        new_customer = Customer(name=name, phone=phone, email=email)
        new_customer.save()
    return redirect('home')

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createTag(request):
    if request.method == 'POST':
        tagName = request.POST['tagName']
        new_tag = Tag(name=tagName)
        new_tag.save()
    return redirect('product')

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def createOrderFromCustomerPage(request, id):
    customer = Customer.objects.get(id=id)
    if request.method == "POST":
        product_name = request.POST['product']
        status = request.POST['status']
        product = Product.objects.get(name=product_name)
        new_order = Order(customer=customer, product=product, status=status)
        new_order.save()
    return redirect('customer', id=id)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def customerCreateOrder(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        product = Product.objects.get(name=request.POST.get('product'))
        quantity = request.POST.get('quantity')
        new_order = Order(customer=customer, product=product, quantity=quantity, status='Pending')
        new_order.save()
    return redirect('user')

# Update Operation Views

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateOrderDetails(request, id):
    customerId = request.POST.get('currPage', None)
    if request.method == 'POST':
        order = Order.objects.get(id=id)
        upd_product = request.POST.get('product_upd_order', None) 
        upd_status = request.POST.get('status_upd_order', None)
        if upd_product is not None:
            order.product = Product.objects.get(name=upd_product)
        if upd_status is not None:
            order.status = upd_status
        order.save()
    if customerId is not None:
        return redirect('customer', id=customerId)
    else:
        return redirect('home')

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def updateProductDetails(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        upd_name = request.POST.get('prod_upd_name', None)
        upd_price = request.POST.get('prod_upd_price', None)
        upd_category = request.POST.get('prod_upd_category', None)
        upd_desc = request.POST.get('prod_upd_description', None)
        if upd_name is not None:
            product.name = upd_name
        if upd_price is not None:
            product.price = upd_price
        if upd_category is not None:
            product.category = upd_category
        if upd_desc is not None:
            product.description = upd_desc
        product.save()
    return redirect('product')

@login_required(login_url='login')
def updateProfileDetails(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic', None)
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        customer.name = name
        customer.email = email
        customer.phone = phone
        
        if profile_pic is not None:
            customer.profile_pic = profile_pic

        customer.save()
    return redirect('userProfile')


# Delete Operation Views

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
    customerId = request.POST.get('customerId', None)
    if customerId is not None:
        return redirect('customer', id=customerId)
        
    else:
        return redirect('home')

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteCustomer(request, id):
    customer = Customer.objects.get(id=id)
    if request.method == 'POST':
        customer.delete()
    return redirect('home')

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.delete()
    return redirect('product')

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteTag(request, id):
    tag = Tag.objects.get(id=id)
    if request.method == 'POST':
        tag.delete()
    return redirect('product')
