from django.shortcuts import render,redirect
from django.contrib.auth import  authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import  login_required, user_passes_test
from .forms import AdminLoginForm,SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Profile,Registration
from django.db.models import Count  # Import Count for aggregation

from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings
import requests

from django.contrib.auth.forms import AuthenticationForm

from django.urls import reverse


from django.conf import settings

# Create your views here.


def send_welcome_sms(user):
    profile = user.profile  # Access the profile where the phone number is stored
    phone_number = profile.phone_number
    name = profile.firstname
    message =f"Hi {name}, welcome to our Afimpp-Tvet Course Registration! We're thrilled to have you on board. Please feel free to explore and apply for any courses that interest you.".format(name=user.first_name)

    message = requests.utils.quote(message)

    key = settings.MNOTIFY_API_KEY
    sender_id = 'Afimpp-Tvet'
    url = f"https://apps.mnotify.net/smsapi?key={key}&to={phone_number}&msg={message}&sender_id={sender_id}"

    response = requests.get(url)
    if response.status_code == 200:
        print("SMS sent successfully")
    else:
        print("Failed to send SMS")

def send_welcome_email(user):
    subject = 'Welcome to Our Platform!'
    profile = user.profile
    name = profile.firstname
    message = "Hi {name}, welcome to our platform! It's great to see you're ready to advance your skills. Please proceed to apply for your chosen course, and let us know if you need any assistance along the way.".format(name=user.first_name)

    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)


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
    program_counts = Registration.objects.values('program_title').annotate(count=Count('program_title'))
    student_count = all_students.count()  # Get the count of all student profiles
    return render(request, 'base/admin_dashboard.html', {
        'student_count': student_count,
        'program_counts': program_counts,
    })





   
@login_required
def student_dashboard(request):
  
    firstname = request.user.first_name
    lastname = request.user.last_name
    registrations = Registration.objects.filter(user=request.user)

    context = {
        'firstname': firstname,
        'lastname': lastname,
        'registrations': registrations
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
            send_welcome_sms(user)
            send_welcome_email(user)
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
    






@login_required
def register(request):
    if request.method == 'POST':
        try:
            # Create a new registration object without saving to the database yet
            registration = Registration(
                prefix=request.POST['prefix'],
                first_name=request.POST['firstName'],
                middle_name=request.POST.get('middleName', ''),
                last_name=request.POST['lastName'],
                dob=request.POST['dob'],
                gender=request.POST['gender'],
                nationality=request.POST['nationality'],
                address=request.POST['address'],
                address2=request.POST.get('address2', ''),
                city=request.POST['city'],
                state=request.POST['state'],
                postal_code=request.POST['postalCode'],
                phone=request.POST['phone'],
                email=request.POST['email'],
                program_title=request.POST['programTitle'],
                
                education_level=request.POST['educationLevel'],
                qualifications=request.POST['qualifications'],
                institutions_attended=request.POST['institutions'],
                current_occupation=request.POST.get('occupation', ''),
                years_experience=int(request.POST.get('experience', 0)),
                relevant_skills=request.POST.get('skills', ''),
                photo=request.FILES['photo'],
                birth_certificate=request.FILES['birthCertificate'],
                education_certificates=request.FILES['educationCertificates'],
                proof_of_payment=request.FILES['paymentProof'],
            )

            # Run full clean to catch any model-level validation issues
            registration.full_clean()
            registration.save()
            messages.success(request, "Registration successful!")
            return redirect('student_dashboard')  # Redirect to a success page or dashboard

        except ValidationError as e:
            # Handle specific field errors from Django's validation
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        except Exception as e:
            # Handle unexpected errors
            messages.error(request, f"Unexpected error during registration: {str(e)}")
            return HttpResponse("Error processing your request.", status=500)

    return render(request, 'base/program.html')
