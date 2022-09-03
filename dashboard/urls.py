from django.urls import path
from . import views
from .views import (
    ProductDetailView,
    CustomersView,
    
)


urlpatterns = [
    path('', views.index, name='index'),##check
    path('login_success', views.login_success, name='login_success'),##check
    path('account/', views.supplier_Inventory, name= 'account'),##check
    path('products/', views.products , name= 'products'),##check
    path('sup-products/<int:key>/',views.viewVendorProducts, name='sup-products'),
    path('s_order_detail/<int:key>/',views.supplierOrderDetails, name='s_order_detail'),
    path('add_products/', views.addProducts , name= 'add_products'),##check
    path('messages/', views.viewMessages , name= 'messages'),##check
    path('reply_msg/<int:key>/', views.replyMessages , name= 'reply_msg'),##check
    path('add_users/', views.addUsers , name= 'add_users'),##check
    path('add_supplier/', views.addSupplier , name= 'add_supplier'),##check
    path('delete/<int:key>', views.delete, name= 'delete'),##check
    path('delete-order/<int:pk>/', views.deleteOrder, name='delete-order'),
    path('update/<int:key>', views.update, name='update'),##check
    path('update-user/<int:key>', views.updateUser, name='update-user'),##check
    #path('items_list/', ItemListView.as_view(), name='items_list'),##check
    path('my_cart/', views.cart_details, name='my_cart'),##check
    path('view-product/<slug:product_slug>/', views.viewProduct, name='view-product'),##check
    path("checkout/", views.cart_details, name="checkout"),
    path('success/', views.success, name="success"),
    path("admin_dash/", views.adminDash, name="admin_dash"),
    path("customers/", CustomersView.as_view(), name="customers"),
    path("order_detail/<int:pk>/", views.orderDetail,
         name="order_detail"),
    path('order_summary/<slug:slug>/', ProductDetailView.as_view(), name='order_summary'),##check
    
   
]