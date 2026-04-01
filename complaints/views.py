from django.shortcuts import render
from .models import Complaints
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.shortcuts import redirect, render
# Create your views here

def add_complaint(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        location = request.POST.get('location')

        print(title, description, category, location)

        Complaints.objects.create(
            title=title,
            description=description,
            category=category,
            location=location
        )

        return render(request, 'complaints/add_complaint.html', {'success': True})

    return render(request, 'complaints/add_complaint.html')

def view_complaints(request):
    data = Complaints.objects.all()   

    return render(request, 'complaints/view_complaints.html', {
        'complaints': data
    })


def delete_complaint(request, id):
    if not request.user.is_superuser:
        return HttpResponse("Not allowed")
    else:
        data = Complaints.objects.get(id=id)
        data.delete()
        return redirect('/view_complaint/')

def edit_complaint(request, id):
    data = Complaints.objects.get(id=id)

    if request.method == "POST":
        data.title = request.POST.get('title')
        data.description = request.POST.get('description')
        data.category = request.POST.get('category')
        data.location = request.POST.get('location')
        data.save()

        return redirect('/view_complaint/')
    return render(request, 'complaints/edit_complaint.html', {'data': data})
   

def home(request):
    recent_complaints = Complaints.objects.all().order_by('-id')[:3]
    return render(request, 'complaints/home.html', {'recent_complaints': recent_complaints})

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db import IntegrityError

def register(request):
    errors = []

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        # Basic validation
        if not username:
            errors.append("Username is required")
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if password != confirmpassword:
            errors.append("Passwords do not match")

        # Check for duplicates
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists")
        if User.objects.filter(email=email).exists():
            errors.append("Email already registered")

        if not errors:
            try:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                return redirect('login_view')
            except IntegrityError:
                errors.append("Something went wrong. Please try again.")


        return render(request, 'complaints/registerpage.html', {'errors': errors})

    return render(request, 'complaints/registerpage.html')

def login_view(request):
    error=None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            error="Username and password required"

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error="Invalid Credentials"

    return render(request, 'complaints/login.html',{'error': error})

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404

def is_admin(user):
    return user.is_superuser  

@login_required
@user_passes_test(is_admin)
def update_status(request, id):
    complaint = get_object_or_404(Complaints, id=id)

    if request.method == "POST":
        new_status = request.POST.get('status')
        if new_status:  
            complaint.status = new_status
            complaint.save()
            print("Status updated in DB:", complaint.status)
            return redirect('/view_complaint/')

    return render(request, 'complaints/updates.html', {'complaint': complaint})

def logout_view(request):
    logout(request)
    return redirect('home')