from django.shortcuts import render, redirect
from .models import User, Product

def home(request):
    return render(request, 'home.html')

# Sign Up
def signup(request):
    if request.method == 'POST':
        User.objects.create(
            Name=request.POST['name'],
            Email=request.POST['email'],
            Role=request.POST['role'],
            PhoneNumber=request.POST['phone'],
            Password=request.POST['password']
        )
        return redirect('login')
    return render(request, 'test_temp/signup.html')

# Login
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(Email=email, Password=password).first()
        if user:
            request.session['user_id'] = user.UserID  # Store user ID in session
            return redirect('add_product')
    return render(request, 'test_temp/login.html')

# Add Product
def add_product(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = User.objects.get(UserID=user_id)
        Product.objects.create(
            ProductName=request.POST['name'],
            Category=request.POST['category'],
            Description=request.POST['desc'],
            Condition=request.POST['condition'],
            OwnerUserID=user,
            Value=request.POST['value']
        )
        return redirect('add_product')  # Or go to product list later
    return render(request, 'test_temp/add_product.html')
