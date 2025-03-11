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
    path('admin_download_students/', views.download_students, name='download_students'),
]   
if settings.DEBUG:  # Ensure this only runs during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)