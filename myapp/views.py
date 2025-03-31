from decimal import Decimal
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
from myapp import models


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
    
    if not request.user.is_staff:
        return redirect('myapp:home_page')

    
    students = StudentApplication.objects.all()

    return render(request, 'admin_dashboard.html', {'students': students})




from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import StudentApplication, SponsorSelection

def download_students_pdf(request):
    # Fetch all students
    students = StudentApplication.objects.all()

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file"
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set up the PDF content
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Students List Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 730, f"Total Students: {students.count()}")

    # Add a table header
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, 710, "Name")
    pdf.drawString(250, 710, "School")
    pdf.drawString(400, 710, "Class")
    pdf.drawString(500, 710, "Annual Cost")
    pdf.drawString(600, 710, "Sponsored")

    # Add student details
    pdf.setFont("Helvetica", 12)
    y = 690
    for student in students:
        pdf.drawString(100, y, student.name)
        pdf.drawString(250, y, student.school)
        pdf.drawString(400, y, student.student_class)
        pdf.drawString(500, y, f"Ksh. {student.annual_cost}")
        pdf.drawString(600, y, "Yes" if student.is_sponsored else "No")
        y -= 20  # Move to the next line

    # Close the PDF object cleanly
    pdf.showPage()
    pdf.save()

    # File response with the PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students_list_report.pdf"'
    return response

def download_donors_pdf(request):
    # Fetch all donors
    donors = SponsorSelection.objects.all()

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file"
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set up the PDF content
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Donors List Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 730, f"Total Donors: {donors.count()}")

    # Add a table header
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, 710, "Donor Name")
    pdf.drawString(250, 710, "Donor Email")
    pdf.drawString(400, 710, "Sponsored Student")
    pdf.drawString(550, 710, "Date Selected")

    # Add donor details
    pdf.setFont("Helvetica", 12)
    y = 690
    for donor in donors:
        pdf.drawString(100, y, donor.sponsor_name)
        pdf.drawString(250, y, donor.sponsor_email)
        pdf.drawString(400, y, donor.student.name)
        pdf.drawString(550, y, donor.date_selected.strftime("%Y-%m-%d"))
        y -= 20  # Move to the next line

    # Close the PDF object cleanly
    pdf.showPage()
    pdf.save()

    # File response with the PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="donors_list_report.pdf"'
    return response




def download_student_report_pdf(request, student_id):
    # Fetch the specific student
    student = StudentApplication.objects.get(id=student_id)
    sponsors = SponsorSelection.objects.filter(student=student)

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file"
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set up the PDF content
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Student Report")
    pdf.setFont("Helvetica", 12)
    
    # Student details
    pdf.drawString(100, 730, f"Name: {student.name}")
    pdf.drawString(100, 710, f"School: {student.school}")
    pdf.drawString(100, 690, f"Class: {student.student_class}")
    pdf.drawString(100, 670, f"Guardian Phone: {student.guardian_phone}")
    pdf.drawString(100, 650, f"Annual Cost: Ksh. {student.annual_cost}")
    pdf.drawString(100, 630, f"Amount Paid: Ksh. {student.amount_paid}")
    pdf.drawString(100, 610, f"Balance: Ksh. {student.balance}")
    pdf.drawString(100, 590, f"Sponsored: {'Fully Sponsored' if student.is_sponsored else 'Partially Sponsored'}")

    # Sponsors list
    pdf.drawString(100, 550, "Sponsors:")
    y = 530
    for sponsor in sponsors:
        pdf.drawString(120, y, f"- {sponsor.sponsor_name} ({sponsor.sponsor_email}): Ksh. {sponsor.amount_contributed} on {sponsor.date_selected.strftime('%Y-%m-%d')}")
        y -= 20
        if y < 50:  # Add new page if running out of space
            pdf.showPage()
            y = 750

    # Close the PDF object cleanly
    pdf.showPage()
    pdf.save()

    # File response with the PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.name}_report.pdf"'
    return response


# def download_student_report_pdf(request, student_id):
#     # Fetch the specific student
#     student = StudentApplication.objects.get(id=student_id)

#     # Create a file-like buffer to receive PDF data
#     buffer = BytesIO()

#     # Create the PDF object, using the buffer as its "file"
#     pdf = canvas.Canvas(buffer, pagesize=letter)

#     # Set up the PDF content
#     pdf.setFont("Helvetica-Bold", 16)
#     pdf.drawString(100, 750, "Student Report")
#     pdf.setFont("Helvetica", 12)
#     pdf.drawString(100, 730, f"Name: {student.name}")
#     pdf.drawString(100, 710, f"School: {student.school}")
#     pdf.drawString(100, 690, f"Class: {student.student_class}")
#     pdf.drawString(100, 670, f"Guardian Phone: {student.guardian_phone}")
#     pdf.drawString(100, 650, f"Annual Cost: Ksh. {student.annual_cost}")
#     pdf.drawString(100, 630, f"Sponsored: {'Yes' if student.is_sponsored else 'No'}")

#     # Close the PDF object cleanly
#     pdf.showPage()
#     pdf.save()

#     # File response with the PDF
#     buffer.seek(0)
#     response = HttpResponse(buffer, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{student.name}_report.pdf"'
#     return response



def download_donor_report_pdf(request, donor_id):
    # Fetch the specific donor
    donor = SponsorSelection.objects.get(id=donor_id)

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file"
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set up the PDF content
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Donor Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 730, f"Donor Name: {donor.sponsor_name}")
    pdf.drawString(100, 710, f"Donor Email: {donor.sponsor_email}")
    pdf.drawString(100, 690, f"Sponsored Student: {donor.student.name}")
    pdf.drawString(100, 670, f"Date Selected: {donor.date_selected.strftime('%Y-%m-%d')}")

    # Close the PDF object cleanly
    pdf.showPage()
    pdf.save()

    # File response with the PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{donor.sponsor_name}_report.pdf"'
    return response



@login_required
def sponsor_home(request):
    # Show students who still need sponsorship
    students = [student for student in StudentApplication.objects.all() 
               if student.amount_paid < student.annual_cost]
    return render(request, 'sponsor_home.html', {'students': students})




@login_required
def apply(request):
    if request.method == 'POST':
        form = StudentApplicationForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('myapp:home_page')
    else:
        form = StudentApplicationForm()
    return render(request, 'apply.html', {'form': form})




@login_required
def sponsor(request, student_id):
    student = StudentApplication.objects.get(id=student_id)
    
    if request.method == 'POST':
        sponsor_name = request.POST.get('sponsor_name')
        sponsor_email = request.POST.get('sponsor_email')
        amount_contributed = Decimal(request.POST.get('amount_contributed', 0))
        
        # Validate the amount
        if amount_contributed <= 0:
            messages.error(request, "Amount must be greater than zero")
            return render(request, 'sponsor.html', {'student': student})
            
        if amount_contributed > student.balance:
            messages.error(request, f"Amount exceeds remaining balance of Ksh. {student.balance}")
            return render(request, 'sponsor.html', {'student': student})
        
        # Create the sponsorship record
        sponsorship = SponsorSelection.objects.create(
            student=student,
            sponsor_name=sponsor_name,
            sponsor_email=sponsor_email,
            amount_contributed=amount_contributed
        )
        
        # Update student's paid amount
        student.amount_paid += amount_contributed
        student.update_sponsorship_status()
        
        messages.success(request, f"Thank you for your sponsorship of Ksh. {amount_contributed}!")
        return redirect('myapp:pay')  # Redirect to payment page
    
    return render(request, 'sponsor.html', {'student': student})






# Adding the mpesa functions
@login_required
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
            "AccountReference": "UBUNTU",
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




from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib.auth.models import User

@login_required
def download_users_pdf(request):
    if not request.user.is_superuser:
        return redirect('myapp:home_page')  # Only superusers can access this

    # Fetch all users
    users = User.objects.all()

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file"
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set up the PDF content
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Users List Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 730, f"Total Users: {users.count()}")

    # Add a table header (without First and Last Name)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, 710, "Username")
    pdf.drawString(250, 710, "Email")
    pdf.drawString(450, 710, "Is Superuser")
    pdf.drawString(550, 710, "Is Staff")

    # Add user details (without First and Last Name)
    pdf.setFont("Helvetica", 12)
    y = 690
    for user in users:
        pdf.drawString(100, y, user.username)
        pdf.drawString(250, y, user.email)
        pdf.drawString(450, y, "Yes" if user.is_superuser else "No")
        pdf.drawString(550, y, "Yes" if user.is_staff else "No")
        y -= 20  # Move to the next line

    # Close the PDF object cleanly
    pdf.showPage()
    pdf.save()

    # File response with the PDF
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="users_list_report.pdf"'
    return response
