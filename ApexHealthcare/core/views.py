# Import necessary modules and classes
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Medical, User, Appointment, Profile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
import numpy as np
import os
from django.contrib import messages
import joblib as joblib
from django.contrib.auth.hashers import make_password

# Define the home view function
def home(request):
    # Render the home template
    return render(request, 'home.html')

# Define the registerView view function
def registerView(request):
    # Render the registration template
    return render(request, 'register.html')

# Define the registerUser view function
def registerUser(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Get username, email, and password from the POST data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Hash the password
        password = make_password(password)
        
         # Create the user
        user = User.objects.create(username=username, email=email, password=password)
        user.save()  
        messages.success(request, 'Account Was Created Successfully')
        
# Note: The code to create and save the user to the database is missing. 
# You need to add that logic here.

# End of the registerUser view function
