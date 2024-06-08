from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from apps.common.views import (
    # Importing views
    render_website_page, custom_404_page, SignUpView, DashboardView,
    ProfileUpdateView, ProfileView, shift_report, ledger_report,
    UserRegistrationView, UserLoginView, add_dpu, active_dpu,
    custom_login, custom_logout, DRECViewSet, NtpDatetimeView,
    dpudetails, edit_dpu, upload_customer_csv, download_latest_csv,
    get_cid_range, get_cust_info, customer_list, config_api,
    download_config_by_st_id, upload_rate_table, rate_table_list,
    download_rate_table, lastratedate_api, ratesitem_api,
    get_dpus_by_location, get_societies_by_dpu, FetchDRECDataView,
    health, admin_question_view, update_question_view,
    ask_question_view, question_history_view,old_drec_data_edited_list
)

# URL patterns
urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Website Pages
    path('', render_website_page, {'page_name': 'index'}, name='home'),
    path('website_products/', render_website_page, {'page_name': 'products'}, name='website_products'),
    path('website_dpu/', render_website_page, {'page_name': 'dpu'}, name='website_dpu'),
    path('website_2_in_1_smart_mini_combo/', render_website_page, {'page_name': '2_in_1_smart_mini_combo'}, name='website_2_in_1_smart_mini_combo'),
    path('website_all_in_1_smart_combo/', render_website_page, {'page_name': 'all_in_1_smart_combo'}, name='website_all_in_1_smart_combo'),
    path('website_solar_charger/', render_website_page, {'page_name': 'solar_charger'}, name='website_solar_charger'),
    path('website_ultrasonic_digital_stirrer/', render_website_page, {'page_name': 'ultrasonic_digital_stirrer'}, name='website_ultrasonic_digital_stirrer'),
    path('website_ultrasonic_digital_stirrer_ss/', render_website_page, {'page_name': 'ultrasonic_digital_stirrer_ss'}, name='website_ultrasonic_digital_stirrer_ss'),
    path('website_ultrasonic_digital_stirrer_v2/', render_website_page, {'page_name': 'ultrasonic_digital_stirrer_v2'}, name='website_ultrasonic_digital_stirrer_v2'),
    path('website_ultrasonic_milk_analyzer/', render_website_page, {'page_name': 'ultrasonic_milk_analyzer'}, name='website_ultrasonic_milk_analyzer'),

    # Authentication URLs
    path('register/', SignUpView.as_view(), name='register'),
    path('api/api_register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/api_login/', UserLoginView.as_view(), name='user-login'),
    path('api/drec/', DRECViewSet.as_view({'get': 'list', 'post': 'create'}), name='drec'),
    path('api/ntpdatetime/', NtpDatetimeView.as_view(), name='ntp_datetime_api'),
    path('api/lastratedate/', lastratedate_api, name='lastratedate_api'),
    path('api/ratesitem/', ratesitem_api, name='ratesitem_api'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),

    # Dashboard and Profile URLs
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='common/change-password.html', success_url='/'), name='change-password'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='common/password-reset/password_reset.html',
        subject_template_name='common/password-reset/password_reset_subject.txt',
        email_template_name='common/password-reset/password_reset_email.html',
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='common/password-reset/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='common/password-reset/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='common/password-reset/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Reports URLs
    path('shift_report/', shift_report, name='shift_report'),
    path('ledger/', ledger_report, name='ledger_report'),

    # DPU-related URLs
    path('get_dpus_by_location/', get_dpus_by_location, name='get_dpus_by_location'),
    path('get_societies_by_dpu/', get_societies_by_dpu, name='get_societies_by_dpu'),
    
    path('add_dpu/', add_dpu, name='add_dpu'),
    path('active_dpu/', active_dpu, name='active_dpu'),
    path('dpudetails/<str:dpuid>/', dpudetails, name='dpudetails'),
    path('edit_dpu/<str:st_id>/', edit_dpu, name='edit_dpu'),

    # Customer-related URLs
    path('upload_customer_csv/', upload_customer_csv, name='upload_customer_csv'),
    path('download_latest_csv/<str:st_id>/', download_latest_csv, name='download_latest_csv'),
    path('api/cidrange/', get_cid_range, name='get_cid_range'),
    path('api/cust_info/', get_cust_info, name='get_cust_info'),
    path('customer-list/<str:st_id>/', customer_list, name='customer-list'),

    # Configuration URLs
    path('api/config/', config_api, name='config-api'),
    path('download/<str:st_id>/', download_config_by_st_id, name='download_config_by_st_id'),
    path('upload_rate_table/', upload_rate_table, name='upload_rate_table'),
    path('rate_table_list/', rate_table_list, name='rate_table_list'),
    path('download-rate-table/<int:rate_table_id>/', download_rate_table, name='download_rate_table'),

    # Other URLs
    path('fetch_drec_data/', FetchDRECDataView.as_view(), name='fetch_drec_data'),
    path('health/', health, name='health'),
    path('admin-question/', admin_question_view, name='admin-question'),
    path('update-question/<int:pk>/', update_question_view, name='update-question'),
    path('ask-question/', ask_question_view, name='ask-question'),
    path('question-history/', question_history_view, name='question-history'),
    path('old_drec_data_edited_list/', old_drec_data_edited_list, name='old_drec_data_edited_list'),

    # Custom 404 page
    path('<path:not_found>/', custom_404_page, name='custom_404_page'),
]

# Handler for 404 error
handler404 = custom_404_page

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
