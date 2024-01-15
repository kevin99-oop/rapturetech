"""
URL configuration for rapturetech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import path,include
from apps.common import views
from apps.common.views import HomeView, SignUpView, DashboardView, ProfileUpdateView, ProfileView, ShiftreportView, UserRegistrationView, UserLoginView, add_dpu, active_dpu,DRECViewSet,NtpDatetimeView,dpudetails


from django.contrib.auth import views as auth_views
from django.urls import path,include
from apps.common import views
from django.urls import path
from django.urls import path, include
from apps.common import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('register/', SignUpView.as_view(), name="register"),

    path('api/api_register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/api_login/', UserLoginView.as_view(), name='user-login'),


    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'
    ), name="login"),

  
    path('logout/', auth_views.LogoutView.as_view(
        
    ), name="logout"),

    path('dashboard/', DashboardView.as_view(), name="dashboard"),

    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='common/change-password.html',
            success_url='/'
        ),
        name='change-password'
    ),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password-reset/password_reset.html',
             subject_template_name='common/password-reset/password_reset_subject.txt',
             email_template_name='common/password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),


    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),
   
    path('shift_report/', ShiftreportView.as_view(), name='shift_report'),

    path('add_dpu/', add_dpu, name='add_dpu'),
    path('active_dpu/', active_dpu, name='active_dpu'),
    path('api/drec/', DRECViewSet.as_view({'get': 'list', 'post': 'create'}), name='drec'),
   
    path('api/ntpdatetime/', NtpDatetimeView.as_view(), name='ntp_datetime_api'),

    path('dpudetails/<str:dpuid>/', dpudetails, name='dpudetails'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)



