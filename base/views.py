import requests
import os
import csv
import uuid
from django.shortcuts import render,redirect
from django.contrib.auth import  authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import  login_required, user_passes_test
from .forms import AdminLoginForm,SignUpForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from .models import Registration, Transaction, Profile,Registration
from django.http import HttpResponse
from io import StringIO, BytesIO
from zipfile import ZipFile
from django.conf import settings
from .models import Registration
from django.db.models import Count  
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

import sys
import django

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'affimpp_regstration.settings')

# Initialize Django
django.setup()

# Test access to settings
from django.conf import settings




# Create your views here.

def send_ceo_sms():
    """This view alerts the administrator when a successful registration is made."""
    phone_numbers = ["557782728", "0500190290"]
    message = """Dear Administrator,

A new registration form has been submitted. Kindly review and approve it within the next three days. You can access the admin portal at: https://affimpp-regstration.onrender.com/admin/. 

Thank you."""
    encoded_message = requests.utils.quote(message)
    key = settings.MNOTIFY_API_KEY
    sender_id = 'Afimpp'

    for phone_number in phone_numbers:
        url = f"https://apps.mnotify.net/smsapi?key={key}&to={phone_number}&msg={encoded_message}&sender_id={sender_id}"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"SMS sent successfully to {phone_number}")
        else:
            print(f"Failed to send SMS to {phone_number}")


def send_welcome_sms(user):
    """This is a View to send a welcome message to new students who register (sms)"""
    profile = user.profile  # Access the profile where the phone number is stored
    phone_number = profile.phone_number
    name = profile.firstname
    message ="Dear {name}, welcome to the Afimpp-Tvet Course Registration platform! We’re excited to have you on board. Feel free to explore and apply for any courses that interest you. If you encounter any challenges, please don’t hesitate to reach out to the administrator, Kennedy, at 0557782728 or via email at akogokennedy@gmail.com.".format(name=user.first_name)

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
    """This is a View to send a welcome message to new students who register (email) """
    subject = 'Welcome to Our Platform!'
    profile = user.profile
    name = profile.firstname
    message = f"""Dear Prospective Student {name},

On behalf of the African Institution of Mining Professionals and Practitioners (AfIMPP), we warmly welcome you to our community!

Thank you for creating an account .  We are excited to have you on board and look forward to supporting your professional development in the mining industry.

As a participant, you will gain access to our comprehensive course materials, expert instructors, and a network of like-minded professionals. Our courses are designed to enhance your skills, knowledge, and career prospects in the mining sector.

To get started, please follow these next steps:

1. Log in to your account to register for your Course

If you have any questions or need assistance, please do not hesitate to contact us at gagyeik@gmail.com 
 We are always here to help.
Once again, welcome to AfIMPP! We are committed to supporting your growth and success in the mining industry.
 If you encounter any challenges, please don’t hesitate to reach out to the administrator,
 Kennedy, at 0557782728 or via email at akogokennedy@gmail.com.
Best regards,

Prof George Agyei 
CEO
African Institution of Mining Professionals and Practitioners (AfIMPP)"""


   # message = "Hi {name}, welcome to our platform! It's great to see you're ready to advance your skills. Please proceed to apply for your chosen course, and let us know if you need any assistance along the way.".format(name=user.first_name)

    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)


def landing(request):
    """Landing page"""
    return render(request, "base/index.html")


def is_admin(user):
    """admin user login"""
    return user.is_staff


def admin_login(request):
    """Admin user login"""
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


# @login_required(login_url=settings.ADMIN_LOGIN_URL)
# @user_passes_test(is_admin)
# def admin_dashboard(request):
#     """Enhanced admin dashboard with approval/rejection functionality"""
    
#     if request.method == 'POST':
#         registration_id = request.POST.get('registration_id')
#         action = request.POST.get('action')
        
#         try:
#             registration = Registration.objects.get(id=registration_id)
            
#             if action == 'approve':
#                 registration.status = 'Approved'
#                 registration.approved_date = now()
#                 registration.save()
                
#                 # Send approval SMS
#                 send_approval_sms(registration)
#                 messages.success(request, f'{registration.first_name} {registration.last_name} has been approved!')
                
#             elif action == 'reject':
#                 rejection_reason = request.POST.get('rejection_reason')
#                 rejection_message = request.POST.get('rejection_message')
                
#                 registration.status = 'Rejected'
#                 registration.rejection_reason = rejection_reason
#                 registration.rejection_message = rejection_message
#                 registration.rejected_date = now()
#                 registration.save()
                
#                 # Send rejection SMS
#                 send_rejection_sms(registration)
#                 messages.success(request, f'{registration.first_name} {registration.last_name} has been rejected.')
                
#         except Registration.DoesNotExist:
#             messages.error(request, 'Registration not found.')
            
#         return redirect('admin_dashboard')
    
#     # Get statistics
#     all_students = Profile.objects.all()
#     registrations = Registration.objects.all().order_by('-date_submitted')
#     program_counts = Registration.objects.values('program_title').annotate(count=Count('program_title'))
    
#     # Status counts
#     student_count = registrations.count()
#     pending_count = registrations.filter(status='Pending').count()
#     approved_count = registrations.filter(status='Approved').count()
#     rejected_count = registrations.filter(status='Rejected').count()
    
#     return render(request, 'base/admin_dashboard.html', {
#         'student_count': student_count,
#         'pending_count': pending_count,
#         'approved_count': approved_count,
#         'rejected_count': rejected_count,
#         'program_counts': program_counts,
#         'registrations': registrations,
#     })
@login_required(login_url=settings.ADMIN_LOGIN_URL)
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Enhanced admin dashboard with approval/rejection functionality"""
    
    if request.method == 'POST':
        registration_id = request.POST.get('registration_id')
        action = request.POST.get('action')
        
        try:
            registration = Registration.objects.get(id=registration_id)
            
            if action == 'approve':
                registration.status = 'Approved'
                registration.approved_date = now()
                registration.save()
                
                # Send approval SMS and Email
                send_approval_sms(registration)
                send_approval_email(registration)
                messages.success(request, f'{registration.first_name} {registration.last_name} has been approved!')
                
            elif action == 'reject':
                rejection_reason = request.POST.get('rejection_reason')
                rejection_message = request.POST.get('rejection_message')
                
                registration.status = 'Rejected'
                registration.rejection_reason = rejection_reason
                registration.rejection_message = rejection_message
                registration.rejected_date = now()
                registration.save()
                
                # Send rejection SMS and Email
                send_rejection_sms(registration)
                send_rejection_email(registration)
                messages.success(request, f'{registration.first_name} {registration.last_name} has been rejected.')
                
        except Registration.DoesNotExist:
            messages.error(request, 'Registration not found.')
            
        return redirect('admin_dashboard')
    
    # Get statistics
    all_students = Profile.objects.all()
    registrations = Registration.objects.all().order_by('-date_submitted')
    program_counts = Registration.objects.values('program_title').annotate(count=Count('program_title'))
    
    # Status counts
    student_count = registrations.count()
    pending_count = registrations.filter(status='Pending').count()
    approved_count = registrations.filter(status='Approved').count()
    rejected_count = registrations.filter(status='Rejected').count()
    
    return render(request, 'base/admin_dashboard.html', {
        'student_count': student_count,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'program_counts': program_counts,
        'registrations': registrations,
    })

# @login_required
# def student_dashboard(request):
#     """Student Dashboard"""
  
#     firstname = request.user.first_name
#     lastname = request.user.last_name
#     registrations = Registration.objects.filter(user=request.user)

#     context = {
#         'firstname': firstname,
#         'lastname': lastname,
#         'registrations': registrations
#     }

#     return render(request, "base/student_dashboard.html", context)



# Also update your existing student_dashboard view to include user object
@login_required
def student_dashboard(request):
    """Student Dashboard"""
    firstname = request.user.first_name
    lastname = request.user.last_name
    registrations = Registration.objects.filter(user=request.user)
    
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    context = {
        'user': request.user,  # Add this line
        'firstname': firstname,
        'lastname': lastname,
        'registrations': registrations,
        'profile': profile,  # Add this line
    }

    return render(request, "base/student_dashboard.html", context)

def student_register(request):
    """This is the view to handle students registration"""

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


def student_login(request):
    """This is the view to login in students"""
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
    

# @login_required
# def register_program(request):
#     """This is View to register for a particular program"""

#     registration = Registration.objects.filter(user=request.user).last()  
#     if request.method == 'POST':
#         try:
#             # Create a new registration object without saving to the database yet
#             registration = Registration(
#                  user=request.user,
#                 prefix=request.POST['prefix'],
#                 first_name=request.POST['firstName'],
#                 middle_name=request.POST.get('middleName', ''),
#                 last_name=request.POST['lastName'],
#                 dob=request.POST['dob'],
#                 gender=request.POST['gender'],
#                 nationality=request.POST['nationality'],
#                 address=request.POST['address'],
#                 address2=request.POST.get('address2', ''),
#                 city=request.POST['city'],
#                 state=request.POST['state'],
#                 postal_code=request.POST['postalCode'],
#                 phone=request.POST['phone'],
#                 email=request.POST['email'],
#                 program_title=request.POST['programTitle'],
                
#                 education_level=request.POST['educationLevel'],
#                 qualifications=request.POST['qualifications'],
#                 institutions_attended=request.POST['institutions'],
#                 current_occupation=request.POST.get('occupation', ''),
#                 years_experience=int(request.POST.get('experience', 0)),
#                 relevant_skills=request.POST.get('skills', ''),
#                 photo=request.FILES['photo'],
#                 birth_certificate=request.FILES['birthCertificate'],
#                 education_certificates=request.FILES['educationCertificates'],
                
#             )

#             # Run full clean to catch any model-level validation issues
#             registration.full_clean()
#             registration.save()
#             send_ceo_sms()
#             messages.success(request, "Registration successful!")
#             return redirect('student_dashboard')  # Redirect to a success page or dashboard

#         except ValidationError as e:
#             # Handle specific field errors from Django's validation
#             for field, errors in e.message_dict.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")
#         except Exception as e:
#             # Handle unexpected errors
#             messages.error(request, f"Unexpected error during registration: {str(e)}")
#             return HttpResponse("Error processing your request.", status=500)

#     return render(request, 'base/program.html',{'registration': registration,})

@login_required
def register_program(request):
    """View to register for a particular program"""
    
    # Get user's existing registrations to show payment status
    user_registrations = Registration.objects.filter(user=request.user)
    
    if request.method == 'POST':
        try:
            # Create a new registration object
            registration = Registration(
                user=request.user,
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
            )

            # Run validation and save
            registration.full_clean()
            registration.save()
            send_ceo_sms()
            
            messages.success(request, f"Registration successful! You can now proceed to payment.")
            return redirect('student_dashboard')  # Redirect to dashboard where payment button will be available

        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")

    return render(request, 'base/program.html', {
        'registrations': user_registrations,  # Pass existing registrations
    })

def export_registrations_with_files(request):
    """This is a View to export the information of all registered users"""
    # Create an in-memory ZIP file
    buffer = BytesIO()
    with ZipFile(buffer, 'w') as zip_file:
        # Create a CSV file for metadata
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(['User', 'Program Title', 'First Name', 'Last Name', 'Gender', 
                             'Date of Birth', 'Status', 'Date Submitted', 'Photo', 
                             'Birth Certificate', 'Educational Certificates', 'Proof of Payment'])
        
        # Loop through all registrations
        for registration in Registration.objects.all():
            # Write metadata row
            csv_writer.writerow([
                registration.user.username,
                registration.program_title,
                registration.first_name,
                registration.last_name,
                registration.gender,
                registration.dob,
                registration.status,
                registration.date_submitted,
                os.path.basename(registration.photo.name),
                os.path.basename(registration.birth_certificate.name),
                os.path.basename(registration.education_certificates.name),
               
            ])

            # Add files to ZIP
            for field in ['photo', 'birth_certificate', 'education_certificates',]:
                file_field = getattr(registration, field)
                if file_field and file_field.name:  # Check if the file exists
                    file_path = file_field.path
                    zip_file.write(file_path, os.path.join('files', os.path.basename(file_path)))

        # Add the CSV file to the ZIP
        zip_file.writestr('registrations.csv', csv_buffer.getvalue())

    # Return the ZIP file as a response
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="registrations_with_files.zip"'
    return response


def pay_with_paystack(request, registration_id):

    """This is the view to initiate payment with paystack"""

    registration = get_object_or_404(Registration, id=registration_id, user=request.user)

    # Generate a unique transaction ID
    transaction_id = str(uuid.uuid4())

    # Create a new Transaction object
    transaction = Transaction.objects.create(
        transaction_id=transaction_id,
        user=request.user,
        registration=registration,
        amount=registration.amount,  # Use the course-specific fee
    )

    # Initialize Paystack payment
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": request.user.email,
        "amount": int(transaction.amount * 100),  # Convert GHS to kobo
        "reference": transaction.transaction_id,
        "callback_url": request.build_absolute_uri(reverse('payment_callback')),  # Adjusted URL
    }
    response = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, json=data)

    if response.status_code == 200:
        return redirect(response.json()['data']['authorization_url'])
    else:
        return JsonResponse({"error": "Payment initialization failed"}, status=400)


def payment_callback(request):
    """Call back function """

    reference = request.GET.get('reference')
    try:
        # Verify the transaction with Paystack
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }
        response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
        if response.status_code == 200:
            data = response.json()['data']
            if data['status'] == 'success':
                # Update transaction as settled
                transaction = Transaction.objects.get(transaction_id=reference)
                transaction.status = 'Completed'
                transaction.date_settled = now()
                transaction.save()

                # Mark the associated registration as paid
                registration = transaction.registration
                registration.payment_status = True
                registration.save()

                messages.success(request, "Payment successful! Your registration has been completed.")
                return redirect('student_dashboard')
        messages.error(request, "Payment verification failed. Please try again.")
        return redirect('student_dashboard')
    except Transaction.DoesNotExist:
        messages.error(request, "Transaction not found.")
        return redirect('student_dashboard')


def send_approval_sms(registration):
    """Send SMS notification when registration is approved"""
    phone_number = registration.phone
    name = registration.first_name
    program = registration.program_title
    
    message = f"""Dear {name},

Congratulations! Your registration for {program} has been APPROVED.

Next Steps:
1. Complete your payment if not done
2. Check your email for course materials
3. Attend orientation on the scheduled date

For support: 0557782728
Email: akogokennedy@gmail.com

Welcome to AfIMMP!"""

    encoded_message = requests.utils.quote(message)
    key = settings.MNOTIFY_API_KEY
    sender_id = 'AfIMMP'

    url = f"https://apps.mnotify.net/smsapi?key={key}&to={phone_number}&msg={encoded_message}&sender_id={sender_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Approval SMS sent successfully to {phone_number}")
    else:
        print(f"Failed to send approval SMS to {phone_number}")


def send_rejection_sms(registration):
    """Send SMS notification when registration is rejected"""
    phone_number = registration.phone
    name = registration.first_name
    reason = registration.rejection_reason
    message = registration.rejection_message or ""
    
    sms_text = f"""Dear {name},

We regret to inform you that your registration has been REJECTED.

Reason: {reason}

{message}

You may reapply after addressing the issues mentioned above.

For assistance: 0557782728
Email: akogokennedy@gmail.com

AfIMMP Admin Team"""

    encoded_message = requests.utils.quote(sms_text)
    key = settings.MNOTIFY_API_KEY
    sender_id = 'AfIMMP'

    url = f"https://apps.mnotify.net/smsapi?key={key}&to={phone_number}&msg={encoded_message}&sender_id={sender_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Rejection SMS sent successfully to {phone_number}")
    else:
        print(f"Failed to send rejection SMS to {phone_number}")

def send_approval_email(registration):
    """Send email notification when registration is approved"""
    subject = '🎉 Registration Approved - AfIMMP'
    name = registration.first_name
    program = registration.program_title
    
    message = f"""Dear {name},

Congratulations! We are pleased to inform you that your registration for {program} has been APPROVED.

Your journey with the African Institution of Mining Professionals and Practitioners (AfIMMP) begins now!

NEXT STEPS:
═══════════════════════════════════════════════════════════
1. Complete Payment: If not already done, please complete your program fee payment
2. Course Materials: Check your student dashboard for downloadable resources
3. Orientation: Attend the mandatory orientation session (details will be sent separately)
4. Academic Calendar: Review the program schedule and important dates

PROGRAM DETAILS:
═══════════════════════════════════════════════════════════
Program: {program}
Fee: GHS 250.00
Status: ✅ APPROVED
Approval Date: {registration.approved_date.strftime('%B %d, %Y')}

SUPPORT & CONTACT:
═══════════════════════════════════════════════════════════
📞 Phone: 0557782728
📧 Email: akogokennedy@gmail.com
🌐 Portal: https://affimpp-regstration.onrender.com/

We are excited to have you join our community of mining professionals and look forward to supporting your career development.

Welcome to AfIMMP!

Best regards,

Prof George Agyei
CEO, African Institution of Mining Professionals and Practitioners (AfIMMP)

---
This is an automated message. Please do not reply to this email.
For support, contact us using the information provided above."""

    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [registration.email]
    
    try:
        send_mail(subject, message, email_from, recipient_list)
        print(f"Approval email sent successfully to {registration.email}")
    except Exception as e:
        print(f"Failed to send approval email to {registration.email}: {str(e)}")


def send_rejection_email(registration):
    """Send email notification when registration is rejected"""
    subject = '❌ Registration Status Update - AfIMMP'
    name = registration.first_name
    program = registration.program_title
    reason = registration.rejection_reason
    additional_message = registration.rejection_message or ""
    
    message = f"""Dear {name},

Thank you for your interest in the African Institution of Mining Professionals and Practitioners (AfIMMP).

After careful review of your application for {program}, we regret to inform you that your registration has been REJECTED.

REJECTION DETAILS:
═══════════════════════════════════════════════════════════
Program Applied: {program}
Rejection Reason: {reason}
Rejection Date: {registration.rejected_date.strftime('%B %d, %Y')}

{f'''
ADDITIONAL FEEDBACK:
═══════════════════════════════════════════════════════════
{additional_message}
''' if additional_message else ''}

NEXT STEPS:
═══════════════════════════════════════════════════════════
- Review the rejection reason(s) carefully
- Address the issues mentioned above
- You may reapply once you have resolved the concerns
- Contact us if you need clarification on the requirements

REAPPLICATION PROCESS:
═══════════════════════════════════════════════════════════
You are welcome to submit a new application after addressing the issues mentioned above. Please ensure all requirements are met before reapplying.

SUPPORT & CONTACT:
═══════════════════════════════════════════════════════════
📞 Phone: 0557782728
📧 Email: akogokennedy@gmail.com
🌐 Portal: https://affimpp-regstration.onrender.com/

We appreciate your interest in AfIMMP and encourage you to reapply once you have addressed the concerns mentioned above.

Best regards,

AfIMMP Admissions Team
African Institution of Mining Professionals and Practitioners

---
This is an automated message. Please do not reply to this email.
For support, contact us using the information provided above."""

    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [registration.email]
    
    try:
        send_mail(subject, message, email_from, recipient_list)
        print(f"Rejection email sent successfully to {registration.email}")
    except Exception as e:
        print(f"Failed to send rejection email to {registration.email}: {str(e)}")




def send_approval_email(registration):
    """Send email notification when registration is approved"""
    subject = '🎉 Registration Approved - AfIMMP'
    name = registration.first_name
    program = registration.program_title
    
    message = f"""Dear {name},

Congratulations! We are pleased to inform you that your registration for {program} has been APPROVED.

Your journey with the African Institution of Mining Professionals and Practitioners (AfIMMP) begins now!

NEXT STEPS:
═══════════════════════════════════════════════════════════
1. Complete Payment: If not already done, please complete your program fee payment
2. Course Materials: Check your student dashboard for downloadable resources
3. Orientation: Attend the mandatory orientation session (details will be sent separately)
4. Academic Calendar: Review the program schedule and important dates

PROGRAM DETAILS:
═══════════════════════════════════════════════════════════
Program: {program}
Fee: GHS 250.00
Status: ✅ APPROVED
Approval Date: {registration.approved_date.strftime('%B %d, %Y')}

SUPPORT & CONTACT:
═══════════════════════════════════════════════════════════
📞 Phone: 0557782728
📧 Email: akogokennedy@gmail.com
🌐 Portal: https://affimpp-regstration.onrender.com/

We are excited to have you join our community of mining professionals and look forward to supporting your career development.

Welcome to AfIMMP!

Best regards,

Prof George Agyei
CEO, African Institution of Mining Professionals and Practitioners (AfIMMP)

---
This is an automated message. Please do not reply to this email.
For support, contact us using the information provided above."""

    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [registration.email]
    
    try:
        send_mail(subject, message, email_from, recipient_list)
        print(f"Approval email sent successfully to {registration.email}")
    except Exception as e:
        print(f"Failed to send approval email to {registration.email}: {str(e)}")


def send_rejection_email(registration):
    """Send email notification when registration is rejected"""
    subject = '❌ Registration Status Update - AfIMMP'
    name = registration.first_name
    program = registration.program_title
    reason = registration.rejection_reason
    additional_message = registration.rejection_message or ""
    
    message = f"""Dear {name},

Thank you for your interest in the African Institution of Mining Professionals and Practitioners (AfIMMP).

After careful review of your application for {program}, we regret to inform you that your registration has been REJECTED.

REJECTION DETAILS:
═══════════════════════════════════════════════════════════
Program Applied: {program}
Rejection Reason: {reason}
Rejection Date: {registration.rejected_date.strftime('%B %d, %Y')}

{f'''
ADDITIONAL FEEDBACK:
═══════════════════════════════════════════════════════════
{additional_message}
''' if additional_message else ''}

NEXT STEPS:
═══════════════════════════════════════════════════════════
- Review the rejection reason(s) carefully
- Address the issues mentioned above
- You may reapply once you have resolved the concerns
- Contact us if you need clarification on the requirements

REAPPLICATION PROCESS:
═══════════════════════════════════════════════════════════
You are welcome to submit a new application after addressing the issues mentioned above. Please ensure all requirements are met before reapplying.

SUPPORT & CONTACT:
═══════════════════════════════════════════════════════════
📞 Phone: 0557782728
📧 Email: akogokennedy@gmail.com
🌐 Portal: https://affimpp-regstration.onrender.com/

We appreciate your interest in AfIMMP and encourage you to reapply once you have addressed the concerns mentioned above.

Best regards,

AfIMMP Admissions Team
African Institution of Mining Professionals and Practitioners

---
This is an automated message. Please do not reply to this email.
For support, contact us using the information provided above."""

    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [registration.email]
    
    try:
        send_mail(subject, message, email_from, recipient_list)
        print(f"Rejection email sent successfully to {registration.email}")
    except Exception as e:
        print(f"Failed to send rejection email to {registration.email}: {str(e)}")


def send_approval_sms(registration):
    """Send SMS notification when registration is approved"""
    phone_number = registration.phone
    name = registration.first_name
    program = registration.program_title
    
    message = f"""🎉 APPROVED! Dear {name},

Your registration for {program} has been APPROVED!

Next Steps:
✅ Complete payment if pending
✅ Check email for details
✅ Attend orientation

Support: 0557782728
Email: akogokennedy@gmail.com

Welcome to AfIMMP! 🎓"""

    encoded_message = requests.utils.quote(message)
    key = settings.MNOTIFY_API_KEY
    sender_id = 'AfIMMP'

    url = f"https://apps.mnotify.net/smsapi?key={key}&to={phone_number}&msg={encoded_message}&sender_id={sender_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Approval SMS sent successfully to {phone_number}")
    else:
        print(f"Failed to send approval SMS to {phone_number}")


def send_rejection_sms(registration):
    """Send SMS notification when registration is rejected"""
    phone_number = registration.phone
    name = registration.first_name
    reason = registration.rejection_reason
    
    message = f"""❌ REJECTED: Dear {name},

Your registration has been rejected.

Reason: {reason}

You may reapply after addressing the issues. Check your email for full details.

Support: 0557782728
Email: akogokennedy@gmail.com

AfIMMP Admin Team"""

    encoded_message = requests.utils.quote(message)
    key = settings.MNOTIFY_API_KEY
    sender_id = 'AfIMMP'

    url = f"https://apps.mnotify.net/smsapi?key={key}&to={phone_number}&msg={encoded_message}&sender_id={sender_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Rejection SMS sent successfully to {phone_number}")
    else:
        print(f"Failed to send rejection SMS to {phone_number}")


@login_required
def student_profile(request):
    """Student Profile View"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None
    
    registrations = Registration.objects.filter(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile,
        'registrations': registrations,
    }
    
    return render(request, "base/student_dashboard.html", context)



@login_required(login_url=settings.ADMIN_LOGIN_URL)
@user_passes_test(is_admin)
def get_registration_details(request, registration_id):
    """Get detailed registration information"""
    try:
        registration = Registration.objects.get(id=registration_id)
        data = {
            'id': registration.id,
            'prefix': registration.prefix,
            'firstName': registration.first_name,
            'middleName': registration.middle_name,
            'lastName': registration.last_name,
            'email': registration.email,
            'phone': registration.phone,
            'dob': registration.dob.strftime('%Y-%m-%d'),
            'gender': registration.gender,
            'nationality': registration.nationality,
            'address': registration.address,
            'address2': registration.address2,
            'city': registration.city,
            'state': registration.state,
            'postalCode': registration.postal_code,
            'programTitle': registration.program_title,
            'status': registration.status,
            'paymentStatus': registration.payment_status,
            'amount': str(registration.amount),
            'dateSubmitted': registration.date_submitted.strftime('%B %d, %Y'),
            'educationLevel': registration.education_level,
            'qualifications': registration.qualifications,
            'institutions': registration.institutions_attended,
            'occupation': registration.current_occupation,
            'experience': registration.years_experience,
            'skills': registration.relevant_skills,
            'rejectionReason': registration.rejection_reason,
            'rejectionMessage': registration.rejection_message,
            'rejectedDate': registration.rejected_date.strftime('%B %d, %Y') if registration.rejected_date else None,
        }
        return JsonResponse(data)
    except Registration.DoesNotExist:
        return JsonResponse({'error': 'Registration not found'}, status=404)