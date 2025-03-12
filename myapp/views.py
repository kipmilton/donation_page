import json
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import StudentApplication, SponsorSelection
from .forms import StudentApplicationForm
from myapp.credentials import LipanaMpesaPpassword, MpesaAccessToken
import requests
from requests.auth import HTTPBasicAuth
from .models import StudentApplication


# Create your views here.

def home_page(request):
    context = {}
    return render(request, "index.html", context)

def login_page(request):
    """Display the appointment page"""
    return render(request, "accounts/login.html")

def logout_user(request):
    """Logs out the user and redirects to login page."""
    logout(request)
    return redirect('myapp:login_page') 

def login_page(request):
    """Login view"""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('myapp:home_page') 
        else:
            messages.error(request, "Invalid login credentials")
    
    return render(request, 'accounts/login.html')


def register(request):
    """Registration view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "Account created successfully.")
                return redirect('myapp:login_page')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'accounts/register.html')



@login_required
def admin_dashboard(request):
    # Check if the user is an admin
    if not request.user.is_staff:
        return redirect('myapp:home_page')  # Or show a 403 error if preferred

    # Get all student applications
    students = StudentApplication.objects.all()

    return render(request, 'admin_dashboard.html', {'students': students})



import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import StudentApplication

@login_required
def download_students(request):
    if not request.user.is_staff:
        return redirect('myapp:home_page')

    # Create the HTTP response with CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'School', 'Class', 'Guardian Phone', 'Annual Cost', 'Sponsored'])
    
    # Write student data to the CSV
    students = StudentApplication.objects.all()
    for student in students:
        writer.writerow([student.name, student.school, student.student_class, student.guardian_phone, student.annual_cost, student.is_sponsored])

    return response






def sponsor_home(request):
    students = StudentApplication.objects.filter(is_sponsored=False)
    return render(request, 'sponsor_home.html', {'students': students})

# views.py
def apply(request):
    if request.method == 'POST':
        form = StudentApplicationForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('myapp:home_page')
    else:
        form = StudentApplicationForm()
    return render(request, 'apply.html', {'form': form})


def sponsor(request, student_id):
    student = StudentApplication.objects.get(id=student_id)
    if request.method == 'POST':
        sponsor_name = request.POST.get('sponsor_name')
        sponsor_email = request.POST.get('sponsor_email')
        SponsorSelection.objects.create(student=student, sponsor_name=sponsor_name, sponsor_email=sponsor_email)
        student.is_sponsored = True
        student.save()
        return redirect('myapp:home_page')
    return render(request, 'sponsor.html', {'student': student})



# Adding the mpesa functions

def pay(request):
    """ Renders the form to pay """
    storage = messages.get_messages(request)
    for _ in storage: 
        pass
    return render(request, 'pay.html')



# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'EJwbmTGr391sTpntpVLLRZzv52oxwVSxXfa8qeaGKL4XxzLw'
    consumer_secret = 'UBIqynIJbG1tete0bDtMFnbhOAh0RUnfwqRFGfQIzl1ya7BqB21dWMFAQb2PzkKM'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth = HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


from django.shortcuts import render


def stk(request):
    """ Sends the stk push prompt """
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        stk_request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://yourdomain.com/callback-url/",
            "AccountReference": "MiltonDNets",
            "TransactionDesc": "Pay for IT"
        }

        try:
            response = requests.post(api_url, json=stk_request, headers=headers)
            response_data = response.json()

            if response.status_code == 200 and "ResponseCode" in response_data:
                messages.success(request, "Payment request sent successfully! Please check your phone.")
                return redirect("myapp:pay")
            else:
                error_message = response_data.get("errorMessage", "An error occurred.")
                messages.error(request, f"Payment failed: {error_message}")
                return redirect("myapp:pay")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return redirect("myapp:pay")
    return redirect("myapp:pay")
