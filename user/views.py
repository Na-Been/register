from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.core.exceptions import ValidationError
# from . forms import RegistrationForm

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


# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             # Save the new user
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password1'])  # Hash the password
#             user.save()

#             # Automatically log in the user after registration
#             login(request, user)

#             # Redirect to a success page or home
#             return redirect('home')  # You can change 'home' to the name of your home page URL
#     else:
#         form = RegistrationForm()

#     return render(request, 'register.html', {'form': form})