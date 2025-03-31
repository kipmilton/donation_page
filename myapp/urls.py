from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myapp'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('accounts/login/', views.login_page, name='login_page'),
    path('accounts/register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('sponsor_home/', views.sponsor_home, name='sponsor_home'),
    path('apply/', views.apply, name='apply'),
    path('sponsor/<int:student_id>/', views.sponsor, name='sponsor'),
    path('pay/', views.pay, name='pay'),
    path('stk/', views.stk, name='stk'),
    path('token/', views.token, name='token'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('download-students-pdf/', views.download_students_pdf, name='download_students_pdf'),
    path('download-donors-pdf/', views.download_donors_pdf, name='download_donors_pdf'),
    path('download-student-report-pdf/<int:student_id>/', views.download_student_report_pdf, name='download_student_report_pdf'),
    path('download-donor-report-pdf/<int:donor_id>/', views.download_donor_report_pdf, name='download_donor_report_pdf'),
    path('download-users-pdf/', views.download_users_pdf, name='download_users_pdf'),
]   
if settings.DEBUG:  # Ensure this only runs during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)