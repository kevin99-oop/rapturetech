from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from apps.common.views import (
    HomeView, SignUpView, DashboardView, ProfileUpdateView, ProfileView,
    shift_report,ledger_report ,UserRegistrationView, UserLoginView, add_dpu, active_dpu,CustomLoginView,custom_logout,
    DRECViewSet, NtpDatetimeView, dpudetails, edit_dpu,upload_customer_csv,download_latest_csv,
    get_cid_range,get_cust_info,customer_list,config_api,download_config_by_st_id,
    upload_rate_table,rate_table_list,download_rate_table,lastratedate_api,ratesitem_api,get_dpus_by_location,get_societies_by_dpu

)
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('register/', SignUpView.as_view(), name="register"),

    # API URLs
    path('api/api_register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/api_login/', UserLoginView.as_view(), name='user-login'),
    path('api/drec/', DRECViewSet.as_view({'get': 'list', 'post': 'create'}), name='drec'),
    path('api/ntpdatetime/', NtpDatetimeView.as_view(), name='ntp_datetime_api'),

    # Authentication URLs
    #path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name="login"),
    path('login/', CustomLoginView.as_view(), name='login'),

    #path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('logout/', custom_logout, name='logout'),

    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='common/change-password.html', success_url='/'), name='change-password'),
    # Forget Password URLs
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password-reset/password_reset.html',
             subject_template_name='common/password-reset/password_reset_subject.txt',
             email_template_name='common/password-reset/password_reset_email.html',
         ), name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password-reset/password_reset_done.html'
         ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password-reset/password_reset_confirm.html'
         ), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password-reset/password_reset_complete.html'
         ), name='password_reset_complete'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('shift_report/', shift_report, name='shift_report'),
    path('get_dpus_by_location/', get_dpus_by_location, name='get_dpus_by_location'),
    path('get_societies_by_dpu/', get_societies_by_dpu, name='get_societies_by_dpu'),

    path('ledger/', ledger_report, name='ledger_report'),
    # DPU-related URLs
    path('add_dpu/', add_dpu, name='add_dpu'),
    path('active_dpu/', active_dpu, name='active_dpu'),
    path('dpudetails/<str:dpuid>/', dpudetails, name='dpudetails'),
    path('edit_dpu/<str:st_id>/', edit_dpu, name='edit_dpu'),
    #Customer Upload/download/add
    path('upload_customer_csv/', upload_customer_csv, name='upload_customer_csv'),
    path('download_latest_csv/<str:st_id>/', download_latest_csv, name='download_latest_csv'),
    path('api/cidrange/', get_cid_range, name='get_cid_range'),
    path('api/cust_info/', get_cust_info, name='get_cust_info'),
    path('customer-list/<str:st_id>/', customer_list, name='customer-list'),
    #/config_file
    path('api/config/', config_api, name='config-api'),
    path('download/<str:st_id>/', download_config_by_st_id, name='download_config_by_st_id'),
    # Add other URLs as needed
    path('upload_rate_table/', upload_rate_table, name='upload_rate_table'),
    path('rate_table_list/', rate_table_list, name='rate_table_list'),
    path('download-rate-table/<int:rate_table_id>/', download_rate_table, name='download_rate_table'),
    path('api/lastratedate/', lastratedate_api, name='lastratedate_api'),
    path('api/ratesitem/', ratesitem_api, name='ratesitem_api'),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)