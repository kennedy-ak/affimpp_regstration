from django.shortcuts import render,redirect
from django.contrib.auth import  authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import  login_required, user_passes_test
from .forms import AdminLoginForm,SignUpForm
from django.contrib.auth.decorators import login_required

from .models import Profile

from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse


from django.conf import settings

# Create your views here.
def landing(request):
    return render(request, "base/index.html")


def is_admin(user):
    return user.is_staff

def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and is_admin(user):
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials or you are not an admin.')
    else:
        form = AdminLoginForm()
    return render(request, 'base/admin_login_form.html', {'form': form})


@login_required(login_url=settings.ADMIN_LOGIN_URL)
@user_passes_test(is_admin)
def admin_dashboard(request):
    all_students = Profile.objects.all()
    student_count = all_students.count()  # Get the count of all student profiles
    return render(request, 'base/admin_dashboard.html', {'student_count': student_count})




@login_required
def student_dashboard(request):
  
    firstname = request.user.first_name
    lastname = request.user.last_name


    context = {
        'firstname': firstname,
        'lastname': lastname
    }

    return render(request, "base/student_dashboard.html", context)


# def student_register(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Create Profile instance
#             Profile.objects.create(
#                 user=user,
#                 email=form.cleaned_data['email'],
#                 phone_number=form.cleaned_data['phone_number'],
#                 firstname=form.cleaned_data['firstname'],
#                 last_name=form.cleaned_data['last_name']
#             )
#             login(request, user)
#             messages.success(request, 'You have successfully registered and are now logged in.')
#             return redirect('student_dashboard')  # Ensure this named URL is correctly configured in your urls.py
#         else:
#             messages.error(request, 'Please correct the errors in the form.')
#     else:
#         form = SignUpForm()
#     return render(request, 'base/students_register.html', {'form': form})


def student_register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create Profile instance
            Profile.objects.create(
                user=user,
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                firstname=form.cleaned_data['firstname'],
                last_name=form.cleaned_data['last_name']
            )
            login(request, user)
            messages.success(request, 'You have successfully registered and are now logged in.')
            return redirect('student_dashboard')
        else:
            # Loop over the form errors to add them to the messages
            for field, errors in form.errors.items():
                for error in errors:
                    # Get the verbose name of the field
                    field_name = form.fields[field].label if form.fields[field].label else field
                    messages.error(request, f"{field_name}: {error}")
    else:
        form = SignUpForm()

    return render(request, 'base/students_register.html', {'form': form})


# def custom_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             # Retrieve the username and password from the validated form data
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')

#             # Authenticate the user
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 # Redirect to a success page.
#                 return HttpResponseRedirect(reverse('student_dashboard'))
#             else:
#                 messages.error(request, 'Invalid username or password.') 
#                 return render(request, 'base/student_login.html', {'form': form, 'error_message': 'Invalid username or password.'})
#         else:
#             # If the form is not valid, render the page with form errors
#             return render(request, 'base/student_login.html', {'form': form})
#     else:
#         # If a GET (or any other method) we'll create a blank form
#         form = AuthenticationForm()
#         return render(request, 'base/student_login.html', {'form': form,})



def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('student_dashboard'))
            else:
                messages.error(request, 'Invalid username or password.')  # Correctly adding a message here
                return render(request, 'base/student_login.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')  # Adding a general form error message
            return render(request, 'base/student_login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'base/student_login.html', {'form': form})