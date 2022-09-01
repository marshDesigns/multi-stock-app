from django.shortcuts import render, redirect
from .forms import CreateUserForm

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else :
        form = CreateUserForm()
        
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    return render(request, 'users/login.html')


def logout(request):
    return render(request, 'users/logout.html')




