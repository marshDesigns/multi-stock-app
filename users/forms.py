from django import forms
from dashboard.models import Customer
from django.contrib.auth.forms import UserCreationForm

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