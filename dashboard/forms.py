from django import forms
from .models import Order, Product, Message, Vendor, Customer
from django.contrib.auth.forms import UserCreationForm


#create form to add products


class SupplierForm(UserCreationForm):
    class Meta:
        model = Vendor
        fields =[
            'username',
            'mcaz_license',
            'email',
            'phone_number',
            'password1',
            'password2',
            #'is_staff',
        ]
        
        
class CreateUserForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = Customer
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'is_superuser',
            'is_staff',
        ]
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =[
            'title',
            'category',
            'pack_size',
            'quantity',
            'price',
            'expiry_date',
            'batch_number',
            'description',  
            ]
        
class CheckoutForm(forms.Form):
    
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
         
class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(max_value=100)     

