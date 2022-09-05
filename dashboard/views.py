from urllib import request
from dashboard.cart import Cart
from asgiref.sync import async_to_sync
import json
from channels.layers import get_channel_layer
from django.shortcuts import render, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from dashboard.utilities import checkout, notify_customer, notify_vendor

from .models import *
from .forms import AddToCartForm, ProductForm, CheckoutForm, MessageForm, SupplierForm
from django.contrib import messages
from django.views.generic import DetailView, View,  TemplateView
from django.urls import reverse_lazy
from notifications_app.forms import BroadcastForm
from users.forms import CreateUserForm
from django.conf import settings
from django.core.mail import send_mail
from django.utils.text import slugify

# Create your views here.

def login_success(request):
    if request.user.is_superuser:
        return redirect('index')
    elif request.user.is_staff:
        return redirect('index')
    elif request.user.is_authenticated:
        return redirect('index')
    elif request.user.vendor:
        return render('index')
    else:
        return redirect('index')
    
    
def viewProduct(request, product_slug):
    # Create instance of Cart class
    cart = Cart(request)

    product = get_object_or_404(Product, slug=product_slug)

    # Check whether the AddToCart button is clicked or not
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product_id=product.id, quantity=quantity, update_quantity=True)

            messages.success(request, "The product was added to the cart.")
            return redirect('view-product',  product_slug=product_slug)            
    
    else:
        form = AddToCartForm()

    context = {
        'product': product,
        
        'form': form,
    }
    return render(request, 'skeleton/view_product.html', context)

def viewVendorProducts(request, key):
    vendor = get_object_or_404(Vendor, pk=key)
    
    context= {
        'vendor': vendor,
    }
    return render(request, 'skeleton/supplier_products.html', context)
    
# home page for both staff and customers defined by user permissions
def index(request): 
    
    vendors = Vendor.objects.all()
    product = Product.objects.all()
    if request.method == 'POST':
        form = BroadcastForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(request, f'broadcast added')
            return redirect('index')
        send = MessageForm(request.POST)
        if send.is_valid():
            send.save()
            return redirect('index')
    else:
        form = BroadcastForm()
        send = MessageForm()

    suppliers = Vendor.objects.all()
    sent_msgs = Message.objects.all()
    orders = Order.objects.all()

    total_customers = suppliers.count()
    total_messages = sent_msgs.count()
    total_products = product.count()
    total_orders = orders.count()
    
    v_products = vendors.product.all()
    v_orders = vendors.orders.all()

    context = {
        'vendors': vendors,
        'product': product,
        'total_customers': total_customers,
        'room_name': "broadcast",
        'total_messages': total_messages,
        'form': form,
        'send': send,
        'total_products':total_products,
        'total_orders': total_orders,
        'v_products':v_products,
        'v_orders':v_orders,
    }
    return render(request, 'skeleton/index.html', context)

@login_required(login_url='login')
def products(request,):
    # fetching all the data in the products table
    #stocks = Product.objects.raw('SELECT * FROM dashboard_product')
    context = {
        'stocks': Product.objects.filter(vendor=request.user.vendor),

    }
    return render(request, 'skeleton/products.html', context)

@login_required(login_url='login')
def viewMessages(request):
    context = {
        'view_msg': Message.objects.all(),
    }
    return render(request, 'skeleton/messages.html', context)


# reply messages sent user customers
@login_required(login_url='login')
def replyMessages(request, key):
    if request.method == 'POST':
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        msg_from = settings.EMAIL_HOST_USER

        send_mail(email, subject, message, msg_from)
        return render(request, 'skeleton/reply_msg.html')

    context = {
        'reply': Message.objects.get(id=key), }
    return render(request, 'skeleton/reply_msg.html', context)

# add stock products
@login_required(login_url='login')
def addProducts(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            product = form.save(commit=True)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            form.save()
            title = form.cleaned_data.get('title')
            messages.success(request, f'{title} has been added')
            return redirect('products')
    else:
        form = ProductForm()
    context = {
        'form': form
    }
    return render(request, 'skeleton/add_products.html', context)

@login_required(login_url='login')
def supplier_Inventory(request):
    vendor = request.user.vendor
    
    products = vendor.products.all()
    orders = vendor.orders.all()
    messages = Message.objects.all()
    
    total_orders = orders.count()
    total_products = products.count()
    total_messages = messages.count()
    
    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False
    context = {
        'vendor': vendor,
        'products': products,
        'orders': orders,
        'total_orders':total_orders,
        'total_products':total_products,
        'total_messages':total_messages,
   
    }
    return render(request, 'skeleton/account.html', context)


## add supplier
@login_required(login_url='login')
def addSupplier(request):
    if request.method =='POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            user = form.save()
            #supplier = Supplier.object.create(name = user.username, first_name = user.first_name, last_name = user.last_name, email = user.email)
            
            return redirect('customers')
    else :
        form = SupplierForm()
    context = {
        'form': form,
    }
    return render(request, 'skeleton/add_supplier.html', context)


# add users
@login_required(login_url='login')
def addUsers(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('username')
            messages.success(request, f'{title} has been added')
            return redirect('add_users')
    else:
        form = CreateUserForm()
    context = {
        'form': form
    }
    return render(request, 'skeleton/add_customers.html', context)

class CustomersView(TemplateView):
    template_name = 'skeleton/customer_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customers = Vendor.objects.all()
        context['customers'] = customers
        return context


# view item details for customer


# view products in cart

# place the order and submit
@login_required(login_url='login')
def cart_details(request):
    cart = Cart(request)

    # If Checkout
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
        
           # try:
        
            amount=int(cart.get_total_cost() * 100), # Amount in Cents
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
              
            order = checkout(request, first_name, last_name, email, phone, address, cart.get_total_cost())
            
            cart.clear()

                # SEnd Email Notification
            #notify_customer(order)
            #notify_vendor(order)
            return redirect('success')
            
           # except Exception:
               # messages.error(request, "Something went wrong with payment.")
            
    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('my_cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('my_cart')
    
    context ={
        'form':form
    }   
    return render(request, 'skeleton/my_cart.html', context)

def success(request):
    return render(request, 'skeleton/success.html')


class AdminOrders(TemplateView):
    template_name= 'skeleton/admin_dash.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor = self.request.user.vendor
        context["orders"] = vendor.orders.all()
        return context
class CustomerOrders(TemplateView):
    template_name= 'skeleton/customer_order_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["orders"] = Order.objects.all()
        return context

# view order details
class SupplierOrderDetails(DetailView):
    template_name= 'skeleton/supplier_order_detail.html'
    model = Order
    context_object_name = 'details'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = ORDER_STATUS
        return context
    
class CustomerOrderDetails(DetailView):
    template_name= 'skeleton/customer_order_detail.html'
    model = Order
    context_object_name = 'details'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status"] = ORDER_STATUS
        return context
class ChangeStatusView(View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy('s_order_detail',kwargs={'pk': order_id}))

# update stock
@login_required(login_url='login')
def update(request, key):
    stock = Product.objects.get(id=key)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=stock)
    context = {
        'form': form,
    }
    return render(request, 'skeleton/update.html', context)

# update user info
@login_required(login_url='login')
def updateUser(request, key):
    stock = User.objects.get(id=key)
    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('customers')
    else:
        form = CreateUserForm(instance=stock)
    context = {
        'form': form,
    }
    return render(request, 'skeleton/update_user.html', context)

# delete stock form database
@login_required(login_url='login')
def delete(request, key):
    stock = Product.objects.get(id=key)
    if request.method == 'POST':
        stock.delete()
        return redirect('products')
    return render(request, 'skeleton/delete.html')

# delete order record
@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('admin_dash')
    return render(request, 'skeleton/delete.html')


def test(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            'type': 'send_notification',
            'message': json.dumps("Notification")
        }
    )
    return HttpResponse("Done")

# customer order summary
class ProductDetailView(DetailView):
    template_name = 'skeleton/order_summary.html'
    model = Order
    context_object_name = 'ord_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context
