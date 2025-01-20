from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.core.exceptions import ValidationError

from . forms import ProfileForm
from .models import Profile

# Create your views here.


def register(request):
    if request.method == 'POST':
        # Get form data from the request
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate password match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'user/register.html')  # Re-render the form with error

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'user/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return render(request, 'user/register.html')

        # Create the user
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            fullname = full_name.split(' ')
            user.first_name = fullname[0] 
            user.last_name = fullname[1]
            user.save()

            # Log the user in after registration
            login(request, user)

            # Redirect to the home page or another page
            return redirect('home')  # You can change 'home' to the name of your home page URL
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, 'user/register.html')  # Handle any unexpected errors
    else:
        return render(request, 'user/register.html')


def showForm(request):
    if request.method == 'POST':
        # Instantiate the form with POST data and FILES data
        form = ProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the form data (including image)
            form.save()
            # Redirect to another page (you can modify the redirect URL as needed)
            return redirect('form')  # Replace with the name of your success page or list view
            
    else:
        # If the request method is GET, create an empty form
        form = ProfileForm()

    # Render the form in the template
    return render(request,'user/form.html',{'form':form})

def profile_list(request):
    # Get the most recently created profile or all profiles
    profiles = Profile.objects.all()  
    return render(request, 'user/profile_list.html', {'profiles': profiles})
