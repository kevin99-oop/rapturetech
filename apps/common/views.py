# Standard Library Imports
import csv
import logging
import os
from datetime import datetime, date
from collections import defaultdict, Counter
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, CreateView, View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.db.models.functions import Round
import string
import random
from django.contrib.auth.views import LoginView


# Django Imports
from apps.common.models import DREC, DPU, Customer, Config, RateTable, CustomerList
from apps.common.forms import (
    SignUpForm,
    UserForm,
    ProfileForm,
    DPUForm,
    UploadCSVForm,
    UploadRateTableForm,
)

# Django Rest Framework Imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from apps.common.serializers import UserSerializer, LoginSerializer, DRECSerializer

# Views Imports
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from apps.common.forms import CustomLoginForm
from django.views.generic import FormView
# ledger code
from django.contrib.admin.views.decorators import staff_member_required

# Common Views

def index(request):
    return render(request, 'index.html')

class HomeView(TemplateView):
    # HomeView class definition ...
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        print(self.request.user.id)
        context['book_list'] = self.request.user
        return context


class CustomLoginView(LoginView):
    template_name = 'common/login.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return response

    def form_valid(self, form):
        # Customize this function if needed (e.g., redirecting to a different page on successful login)
        response = super().form_valid(form)
        
        return response


def custom_login(request):
    template_name = 'common/login.html'
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after successful login
        else:
            # Handle invalid login credentials
            # You can add a message here if needed
            messages.error(request, "Invalid User name or Password")
            return render(request, template_name)  # You can render the template again or redirect to the same login page
    else:
        return render(request, template_name)   



def custom_logout(request):
    # Use Django's logout function to log the user out
    logout(request)
    # Redirect to the desired page after logout
    return redirect(reverse('home'))  # Replace 'home' with the name of your home URL pattern{    login_url = reverse_lazy('home')}

#superadmin Login
@login_required
def super_dashboard(request):
    # Logic for user dashboard
    return render(request, 'common/super_admin/super_dashboard.html')

#This dashboard is for Mandli Main who manage all the st_id and all 
@method_decorator([login_required, ensure_csrf_cookie], name='dispatch')
class DashboardView(TemplateView):
    template_name = 'example.html'
    print("125")
    # login_url = reverse_lazy('home')
    
    def get_drec_data(self, user):
                return DREC.objects.filter(ST_ID__user=user).order_by('-created_at')

    def calculate_averages(self, records):
        total_fat = sum(record.FAT for record in records)
        total_snf = sum(record.SNF for record in records)
        total_clr = sum(record.CLR for record in records)
        total_water = sum(record.WATER for record in records)
        total_ltr = sum(record.QT for record in records)
        total_amt = sum(record.Amount for record in records)

        total_cust_set = {(record.CUST_ID, record.CSR_NO) for record in records}
        total_cust = len(total_cust_set)

        avg_fat = round(total_fat / len(records), 1) if len(records) > 0 else 0.0
        avg_snf = round(total_snf / len(records), 1) if len(records) > 0 else 0.0
        avg_clr = round(total_clr / len(records), 1) if len(records) > 0 else 0.0
        total_ltr = round(sum(record.QT for record in records), 2)
        total_amt = round(sum(record.Amount for record in records), 2)
        avg_water = round(total_water / len(records), 2) if len(records) > 0 else 0.0

        return avg_fat, avg_snf, avg_clr, avg_water, total_ltr, total_amt, total_cust

    def prepare_summary_data(self, drec_data, active_dpu_list):
        grouped_data = defaultdict(list)
        latest_records = {}

        for drec in drec_data:
            key = drec.ST_ID.st_id
            grouped_data[key].append(drec)

            # Track the latest record for each ST_ID
            if key not in latest_records or drec.RecordingDate > latest_records[key].RecordingDate:
                latest_records[key] = drec

        summary_data = []
        for st_id, records in grouped_data.items():
            # Use the latest record from the tracked records
            latest_record = latest_records.get(st_id)

            if latest_record:
                avg_fat, avg_snf, avg_clr, avg_water, total_ltr, total_amt, total_cust = self.calculate_averages(records)

                summary_data.append({
                    'ST_ID__st_id': st_id,
                    'ST_ID__location': latest_record.ST_ID.location,
                    'ST_ID__society': latest_record.ST_ID.society,
                    'RecordingDate': latest_record.RecordingDate,
                    'SHIFT': latest_record.SHIFT,
                    'avg_fat': avg_fat,
                    'avg_snf': avg_snf,
                    'avg_clr': avg_clr,
                    'avg_water': avg_water,
                    'total_ltr': total_ltr,
                    'total_amt': total_amt,
                    'total_cust': total_cust,
                    'latest_record': latest_record,
                })
        # Sort by RecordingDate and SHIFT in descending order
        return summary_data
    
    def get_customer_list(self, user):
        return CustomerList.objects.filter(user=user)

    def calculate_global_averages(self, user):
        avg_fat = DREC.objects.filter(ST_ID__user=user).aggregate(avg_fat=Avg('FAT'))['avg_fat']
        avg_snf = DREC.objects.filter(ST_ID__user=user).aggregate(avg_snf=Avg('SNF'))['avg_snf']
        avg_clr = DREC.objects.filter(ST_ID__user=user).aggregate(avg_clr=Avg('CLR'))['avg_clr']

        return (
            round(avg_fat, 1) if avg_fat is not None else None,
            round(avg_snf, 1) if avg_snf is not None else None,
            round(avg_clr, 1) if avg_clr is not None else None
        )
    def get_drec_data(self, user, selected_date=None):
        queryset = DREC.objects.filter(ST_ID__user=user)
        if selected_date:
            queryset = queryset.filter(RecordingDate=selected_date)
        return queryset.order_by('-created_at')

    def get_recording_dates(self, user):
        return DREC.objects.filter(ST_ID__user=user).values_list('RecordingDate', flat=True).distinct()

    def get_top_10_latest_records(self, user, st_id):
    # Retrieve the top 10 latest records for the given ST_ID
        return DREC.objects.filter(ST_ID__user=user, ST_ID__st_id=st_id).order_by('-RecordingDate', '-SHIFT')[:10]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        drec_data = self.get_drec_data(user)
      # Check if the user is not staff or super admin
        # if not user.is_staff and not user.is_superuser:
        #     messages.error(request, "You are not authorized to access this page.")
        #     return redirect('home')  # Assuming 'home' is the URL name for the homepage

        active_dpu_list = DPU.objects.filter(user=user)
        summary_data = self.prepare_summary_data(drec_data, active_dpu_list)
        customer_list = self.get_customer_list(user)
        avg_fat, avg_snf, avg_clr = self.calculate_global_averages(user)
      
        total_customer_count = CustomerList.objects.filter(user=request.user).count()
        total_dpus = DPU.objects.filter(user=request.user).count()
        if summary_data:
            top_st_id = summary_data[0]['ST_ID__st_id']
            top_10_latest_records = self.get_top_10_latest_records(user, top_st_id)
        else:
            top_st_id = None
            top_10_latest_records = None

        recording_dates = self.get_recording_dates(user)

        context = {
            'active_dpu_list': active_dpu_list,
            'drec_data': drec_data,
            'customer_list': customer_list,
            'summary_data': summary_data,
            'last_updated': timezone.now(),
            'avg_fat': avg_fat,
            'avg_snf': avg_snf,
            'avg_clr': avg_clr,
            'total_customer_count': total_customer_count,
            'total_dpus': total_dpus,
            'dpu_list': ', '.join(dpu.st_id for dpu in active_dpu_list),
            'recording_dates': recording_dates,
            'top_10_latest_records': top_10_latest_records,
        }
        # Redirect non-staff users to the home page
        # if not user.is_staff:
        #     return redirect('home')
        print("Dashboard")      
        return render(request, self.template_name, context)



# #St_id User Mobile login User
# @login_required(login_url='/custom-login/')  # Specify a custom login URL
# def user_dashboard(request):
#     user = request.user
#     # Retrieve the DPU instance associated with the logged-in user
#     try:
#         dpu = DPU.objects.get(mobile_number=user.username)
#     except DPU.DoesNotExist:
#         # Handle the case where the DPU does not exist for the logged-in user
#         # You can redirect the user to a page indicating that they need to set up their DPU
#         return HttpResponse("DPU not found for the current user.")
#     # Retrieve DREC data related to the DPU
#     drec_data = DREC.objects.filter(ST_ID=dpu)
#     # Prepare summary data
#     grouped_data = defaultdict(list)
#     latest_records = {}
#     for drec in drec_data:
#         key = drec.ST_ID.st_id
#         grouped_data[key].append(drec)
#         if key not in latest_records or drec.RecordingDate > latest_records[key].RecordingDate:
#             latest_records[key] = drec

#     summary_data = []
#     for st_id, records in grouped_data.items():
#         latest_record = latest_records.get(st_id)
#         if latest_record:
#             avg_fat = round(sum(record.FAT for record in records) / len(records), 2)
#             avg_snf = round(sum(record.SNF for record in records) / len(records), 2)
#             avg_clr = round(sum(record.CLR for record in records) / len(records), 2)
#             avg_water = round(sum(record.WATER for record in records) / len(records), 2)
#             total_ltr = sum(record.QT for record in records)
#             total_amt = sum(record.Amount for record in records)
#             total_cust_set = {(record.CUST_ID, record.CSR_NO) for record in records}
#             total_cust = len(total_cust_set)

#             summary_data.append({
#                 'ST_ID__st_id': st_id,
#                 'ST_ID__location': latest_record.ST_ID.location,
#                 'ST_ID__society': latest_record.ST_ID.society,
#                 'RecordingDate': latest_record.RecordingDate,
#                 'SHIFT': latest_record.SHIFT,
#                 'avg_fat': avg_fat,
#                 'avg_snf': avg_snf,
#                 'avg_clr': avg_clr,
#                 'avg_water': avg_water,
#                 'total_ltr': total_ltr,
#                 'total_amt': total_amt,
#                 'total_cust': total_cust,
#                 'latest_record': latest_record,
#             })

#     # Retrieve customer list related to the DPU
#        # Retrieve customer list related to the DPU
#     customer_list = CustomerList.objects.filter(st_id=dpu.st_id)

#     # Calculate total number of customers
#     total_customer_count = customer_list.count()



#     # Calculate global averages (for the current DPU)
#     # Calculate global averages (for the current DPU) and round them to two decimal places
#     avg_fat = drec_data.aggregate(avg_fat=Avg('FAT'))['avg_fat']
#     avg_snf = drec_data.aggregate(avg_snf=Avg('SNF'))['avg_snf']
#     avg_clr = drec_data.aggregate(avg_clr=Avg('CLR'))['avg_clr']


#     # Get recording dates
#     recording_dates = drec_data.values_list('RecordingDate', flat=True).distinct()

#     # Prepare context
#     context = {
#         'drec_data': drec_data,
#         'customer_list': customer_list,
#         'summary_data': summary_data,
#         'last_updated': timezone.now(),
#         'avg_fat': avg_fat,
#         'avg_snf': avg_snf,
#         'avg_clr': avg_clr,
#         'total_customer_count': len(customer_list),
#         'recording_dates': recording_dates,
#         'total_customer_count': total_customer_count,  # Total count of customers for the DPU

#         # Add other context variables as needed
#     }

#     # Render user_dashboard.html template with context
#     return render(request, 'common/user/user_dashboard.html', context)


# User Authentication Views
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'common/register.html'

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Render the registration template after a successful registration
        return render(request, 'common/register.html', {'message': 'Registration successful!'})
    
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Parse request data as JSON if content type is "text/plain"
            if request.content_type == 'text/plain':
                request_data = JSONParser().parse(request)
            else:
                request_data = request.data
            # Deserialize JSON data using your serializer
            serializer = LoginSerializer(data=request_data)
            print("before if")
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                # Add your authentication logic here (e.g., using Django's built-in authentication)
                user = authenticate(
                    request, username=username, password=password)
                if user is not None:
                    # Authentication successful, create or retrieve a token
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({"token": token.key}, status=status.HTTP_200_OK, content_type='application/json')
                else:
                    # Authentication failed
                    return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED, content_type='application/json')
            else:
                # Invalid input data
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        except Exception as e:
            # Handle other exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'common/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the authentication token for the current user
        token, created = Token.objects.get_or_create(user=self.request.user)
        # Add the token to the context
        context['token'] = token.key
        return context
        
    

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'common/user/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the DPU instance associated with the logged-in user
        try:
            dpu = DPU.objects.get(mobile_number=self.request.user.username)
        except DPU.DoesNotExist:
            dpu = None
        
        # Add the DPU object to the context
        context['dpu'] = dpu
        return context
    
class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'common/profile-update.html'
    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None
        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(
            post_data, file_data, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse_lazy('profile'))
        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form
        )
        return self.render_to_response(context)
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def generate_random_password( length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

#admin can do this 
@login_required
def add_dpu(request):
    if request.method == 'POST':
        form = DPUForm(request.POST)
        if form.is_valid():
            dpu = form.save(commit=False)
            password = generate_random_password()
            print("password : ", password)
            user = User.objects.create_user(request.POST.get("mobile_number"),  "dummy@gmail.com", password)
            user.save()
            dpu.plain_password = password
            dpu.user = request.user
            dpu.dpu_user = user.id        
            dpu.save()
            # Redirect to the user's dashboard or any other page
            return redirect('active_dpu')
    else:
        if not request.user.is_staff and not request.user.is_superuser:
            messages.error(request, 'You are not authorised to add DPU')
            return redirect("dashboard")
        form = DPUForm()
    return render(request, 'common/add_dpu.html', {'form': form})

def active_dpu(request):
    # for super user
    if request.user.is_staff and request.user.is_superuser:
        active_dpu_list = DPU.objects.filter(user=request.user)
    # for Staff user    
    elif request.user.is_staff and not request.user.is_superuser:   
        active_dpu_list = DPU.objects.filter(user=request.user)
    # for no staff no super user (Normal)  
    elif not request.user.is_staff and not request.user.is_superuser:
        user_id = request.user.id
        active_dpu_list = DPU.objects.filter(dpu_user=user_id)

    return render(request, 'common/active_dpu.html', {'active_dpu_list': active_dpu_list})
    
class DRECViewSet(viewsets.ModelViewSet):
    queryset = DREC.objects.all()
    serializer_class = DRECSerializer
    print("perform create before")

    def perform_create(self, serializer):
        # You can customize the save process here before calling the super method
        instance = serializer.save()
        print("perform create")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = 200  # Set the status code to 200
        print("perform create", response)
        return response

    def save(self, *args, **kwargs):
        # Replace None values with "null"
        for field in self._meta.fields:
            value = getattr(self, field.name)
            if value is None:
                setattr(self, field.name, "null")

        # Assuming dpuid is a ForeignKey to DPU model
        if self.dpuid:
            self.dpuid = self.dpuid.st_id

        super().save(*args, **kwargs)

class NtpDatetimeView(View):
    def get(self, request, *args, **kwargs):
        # Get the current system date and time
        current_datetime = datetime.now()

        # Format the date and time as a string
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Create a dictionary with the response data
        response_data = {'datetime': formatted_datetime}

        # Return the response as a JSON object
        return JsonResponse(response_data)

def dpudetails(request, dpuid):
    dpu = get_object_or_404(DPU, st_id=dpuid)
    drecs = dpu.drecs.all()  # Use the correct related name
    context = {
        'dpu': dpu,
        'drecs': drecs,
    }
 # Fetch DPU based on dpu_id
    dpu = DPU.objects.get(st_id=dpuid)
    # Fetch customer names for the specific DPU
    customer_list = CustomerList.objects.filter(st_id=dpuid)
    # Fetch DREC entries for the specific DPU
    drecs = DREC.objects.filter(ST_ID=dpu)
    dpu = get_object_or_404(DPU, st_id=dpuid)
    context = {
        'dpu': dpu,
        'drecs': drecs,
    }

    context = {
        'dpu': dpu,
        'customer_list': customer_list,
        'drecs': drecs,

    }
    return render(request, 'common/dpudetails.html', context)

class UserDpuDetails(TemplateView):
    template_name = 'common/user/user_dpudetails.html'  # Assuming the template is named 'user_dpudetails.html'
    
    def get_context_data(self, **kwargs):
        st_id = self.kwargs.get('st_id')  # Get st_id from URL
        dpu = get_object_or_404(DPU, st_id=st_id)
        
        customer_list = CustomerList.objects.filter(st_id=st_id)
        drecs = DREC.objects.filter(ST_ID=dpu)
        
        context = {
            'dpu': dpu,
            'customer_list': customer_list,
            'drecs': drecs,
        }
        return context

def edit_dpu(request, st_id):
    dpu = get_object_or_404(DPU, st_id=st_id)

    if request.method == 'POST':
        form = DPUForm(request.POST, instance=dpu)
        if form.is_valid():
            form.save()
            # Check if the status has changed
            if dpu.status != form.cleaned_data['status']:
                return JsonResponse({'status_changed': True})
            form.save()
            # Redirect to the desired page after editing
            return redirect('active_dpu')
    else:
        form = DPUForm(instance=dpu)

    return render(request, 'common/edit_dpu.html', {'form': form, 'dpu': dpu})

def extract_cust_id_range(csv_file):
    # Read the CSV file and extract the start and end range based on CUST_ID values
    csv_content = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(csv_content)
    # Extract CUST_ID values
    cust_ids = [int(row['CUST_ID']) for row in reader]
    # Determine start and end range
    start_range = min(cust_ids) if cust_ids else 1
    end_range = max(cust_ids) if cust_ids else 10

    return start_range, end_range

import logging

logger = logging.getLogger(__name__)

def upload_customer_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = form.cleaned_data['csv_file']
                csv_content = csv_file.read().decode('utf-8')
                csv_lines = csv_content.splitlines()

                # Fetch the first 10 characters from the top-left cell as st_id
                st_id = csv_lines[0][:10].strip()
                # Fetch the corresponding DPU instance
                dpu_instance = DPU.objects.get(st_id=st_id)
                # Check if CSV file for the given st_id already exists
                existing_customer = Customer.objects.filter(user=request.user, st_id=dpu_instance).first()
                if existing_customer:
                    # Update the existing CSV file with the new data
                    existing_customer.csv_file = csv_file
                    existing_customer.save()
                    messages.success(request, 'CSV file updated successfully.')
                else:
                    # Create a new Customer instance with the CSV file and associated DPU
                    Customer.objects.create(
                        user=request.user,
                        st_id=dpu_instance,
                        csv_file=csv_file,
                    )
                    messages.success(request, 'CSV file uploaded successfully.')
                # Process the CSV content and save data to CustomerList model
                process_csv_content(request.user, st_id, csv_lines)
                # Redirect to customer-list with st_id parameter
                return redirect('customer-list', st_id=st_id)

            except FileNotFoundError:
                logger.error('Error processing CSV file: File not found.')
                messages.error(request, 'Error processing CSV file: File not found.')
            except DPU.DoesNotExist:
                logger.error(f'DPU with st_id {st_id} does not exist.')
                messages.error(request, f'DPU with st_id {st_id} does not exist.')
            except Exception as e:
                logger.error(f'Error processing CSV file: {e}')
                messages.error(request, f'Error processing CSV file: {e}')
        else:
            logger.error('Invalid form submission. Please check the file format.')
            messages.error(request, 'Invalid form submission. Please check the file format.')
    else:
        form = UploadCSVForm()

    # Log the SQL queries
    logger.info(connection.queries)

    return render(request, 'common/upload_customer_csv.html', {'form': form})

def process_csv_content(user, st_id, csv_lines):
    # Skip the header row
    header = csv_lines.pop(0)
    # Get the list of existing cust_id values for the given st_id
    existing_cust_ids = CustomerList.objects.filter(user=user, st_id=st_id).values_list('cust_id', flat=True)
    # Iterate through the remaining lines and create, update, or delete CustomerList instances
    for line in csv_lines:
        data = line.split(',')
        # Check if the line has the expected number of values
        if len(data) != 6:
            # Log or handle the error accordingly
            print(f"Error processing CSV file row: {line}")

            continue

        cust_id, name, mobile, adhaar, bank_ac, ifsc = data

        # Skip lines that do not start with a number (assuming it's a header or label)
        if not cust_id.isdigit():
            continue

        # Check if CustomerList instance with the same cust_id and st_id exists
        existing_customer = CustomerList.objects.filter(user=user, st_id=st_id, cust_id=cust_id).first()
        if existing_customer:
            # Update the existing instance with the new data
            existing_customer.name = name
            existing_customer.mobile = mobile
            existing_customer.adhaar = adhaar
            existing_customer.bank_ac = bank_ac
            existing_customer.ifsc = ifsc
            existing_customer.save()
        else:
            # Create a new CustomerList instance
            CustomerList.objects.create(
                user=user,
                st_id=st_id,
                cust_id=cust_id,
                name=name,
                mobile=mobile,
                adhaar=adhaar,
                bank_ac=bank_ac,
                ifsc=ifsc,
            )
    # Delete rows that are in the database but not in the CSV file
    CustomerList.objects.filter(user=user, st_id=st_id).exclude(cust_id__in=existing_cust_ids).delete()
@login_required
def customer_list(request, st_id):
    # Fetch the customer list for the given st_id
    customer_list = CustomerList.objects.filter(st_id=st_id)

    # Pass the customer_list to the template
    context = {'customer_list': customer_list, 'st_id': st_id}
    
    return render(request, 'common/customer_list.html', context)
@login_required
def user_customer_list(request, st_id):
    # Fetch the customer list for the given st_id
    customer_list = CustomerList.objects.filter(st_id=st_id)

    # Pass the customer_list to the template
    context = {'customer_list': customer_list, 'st_id': st_id}
    
    return render(request, 'common/user/user_customer_list.html', context)

def download_latest_csv(request, st_id):
    try:
        latest_customer = get_object_or_404(Customer.objects.filter(
            user=request.user, st_id=st_id).order_by('-date_uploaded')[:1])

        with open(latest_customer.csv_file.path, 'rb') as csv_file:
            response = HttpResponse(csv_file.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{latest_customer.csv_file.name}"'
            return response

    except FileNotFoundError:
        messages.error(request, 'CSV file not found.')
    except Exception as e:
        messages.error(request, f'Error downloading CSV file: {e}')

    return redirect('error_view')

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_cid_range(request):
    dpuid = request.GET.get('dpuid', '')
    try:
        # Fetch all Customer entries for the given dpuid
        customer_entries = get_list_or_404(Customer, st_id=dpuid)
        if not customer_entries:
            return JsonResponse({'error': f'No CSV file found for dpuid: {dpuid}'}, status=404)
        # Get the latest Customer entry based on id
        latest_customer = max(customer_entries, key=lambda entry: entry.id)
        # Retrieve the CSV file path from the latest_customer model
        csv_file_path = latest_customer.csv_file.path
        # Read CSV data and calculate start and end range
        with open(csv_file_path, 'r') as file:
            # Skip the header row
            next(file)
            reader = csv.DictReader(file)
            cust_ids = [int(row['CUST_ID']) for row in reader]
        # Calculate start and end range
        start_range = 1 if cust_ids else 0
        end_range = max(cust_ids) if cust_ids else 0
        # Prepare the JSON response with the range values
        response_data = {'noofcustomer': f'{start_range},{end_range}'}
        return JsonResponse(response_data)
    except Exception as e:
        logger.exception(f'Error processing request for dpuid {dpuid}: {e}')
        return JsonResponse({'error': f'Internal Server Error'}, status=500)

def get_cust_info(request):
    dpuid = request.GET.get('dpuid', '')
    cid = request.GET.get('cid', '')
    try:
        # Fetch all Customer entries for the given dpuid
        customer_entries = get_list_or_404(Customer, st_id=dpuid)
        if not customer_entries:
            return JsonResponse({'error': f'No CSV file found for dpuid: {dpuid}'}, status=404)
        # Get the latest Customer entry based on id
        latest_customer = max(customer_entries, key=lambda entry: entry.id)
        # Retrieve the CSV file path from the latest_customer model
        csv_file_path = latest_customer.csv_file.path
        # Read CSV data and find the row with the given CID
        with open(csv_file_path, 'r') as file:
            # Skip the header row
            next(file)
            for row in csv.DictReader(file):
                if 'CUST_ID' in row and row['CUST_ID'] == cid:
                    # Prepare the JSON response with the customer info
                    response_data = {
                        'cinfo': f"{row['CUST_ID']},{row['NAME']},{row['MOBILE']},{row['ADHHAR']},{row['BANK_AC']},{row['IFSC']}"
                    }
                    return JsonResponse(response_data)
        # If no matching row is found
        return JsonResponse({'error': f'No customer found with CID: {cid}'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Internal Server Error'}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def config_api(request):
    if request.method == 'POST':
        try:
            # Assuming the data is received in the request body
            text_data = request.body.decode('utf-8')
            print(text_data)
            # Extract ST_ID from the text data before the "DT" part
            st_id_start = text_data.find("ST_ID:") + len("ST_ID:")
            dt_start = text_data.find("DT:")
            st_id = text_data[st_id_start:dt_start].strip()
            # Assuming the user is authenticated, you can access the user from the request
            user = request.user
            # Check if a Config object with the same ST_ID exists
            existing_config = Config.objects.filter(st_id=st_id).first()
            if existing_config:
                # If exists, update the text data and delete the old text
                existing_config.text_data = text_data
                existing_config.save()
            else:
                # If not exists, create a new Config object
                Config.objects.create(
                    user=user, st_id=st_id, text_data=text_data)
            return JsonResponse({"success": True, "message": "Config created/updated successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request method."})

@csrf_exempt
@permission_classes([IsAuthenticated])
def download_config_by_st_id(request, st_id):
    configs = Config.objects.filter(st_id=st_id, user=request.user)
    # Check if there are any configs matching the criteria
    if not configs.exists():
        raise Http404("Config not found for the specified st_id.")
    # Concatenate and format text data from all matching configs
    formatted_text_data = "\n".join(format_text_data(
        config.text_data) for config in configs)
    # Create the response with the formatted text data
    response = HttpResponse(formatted_text_data, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={st_id}_config.txt'
    return response

def format_text_data(text_data):
    formatted_lines = []
    # Split the input text by space and remove empty elements
    elements = [elem.strip() for elem in text_data.split(' ') if elem.strip()]
    # Iterate over the elements and format them
    for element in elements:
        if ':' in element:
            key, value = element.split(':', 1)
            formatted_lines.append(f"{key}: {value}")
        else:
            formatted_lines.append(element)
    return '\n'.join(formatted_lines)

def upload_rate_table(request):
    if request.method == 'POST':
        form = UploadRateTableForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']

            # Extract start_date from the CSV file content (assuming it's in the left-top corner)
            start_date = None
            try:
                # Decode the CSV content from bytes to string
                csv_content = csv_file.read().decode('utf-8')
                # Split the lines and get the first line
                first_line = csv_content.splitlines()[0]
                # Assuming the date is in the first column of the CSV file
                date_str = first_line.split(',')[0].strip()
                start_date = datetime.strptime(date_str, '%d-%m-%Y').date() if date_str else None
            except Exception as e:
                messages.error(request, f'Error extracting start date from CSV: {e}')

            # Extract information from the CSV file name
            filename_parts = csv_file.name.split('_')
            animal_type_code = filename_parts[0][0].upper()  # Extract the first letter (animal type code)
            rate_type = filename_parts[0][1:4].upper()  # Extract the next 3 characters (rate type)

            # Convert animal_type_code to full animal type
            animal_type = 'COW' if animal_type_code == 'C' else 'BUFFALOW' if animal_type_code == 'B' else None

            if animal_type:
                # Save the RateTable entry with the corresponding user, animal type, rate type, and CSV file
                rate_table = RateTable(
                    user=request.user,
                    animal_type=animal_type,
                    rate_type=rate_type,
                    csv_file=csv_file,
                    start_date=start_date,
                )
                rate_table.save()

                messages.success(request, 'Rate table uploaded successfully.')
                return redirect('rate_table_list')
            else:
                messages.error(request, 'Invalid animal type code in the file name.')
        else:
            messages.error(request, 'Invalid form submission. Please check the file format.')
    else:
        form = UploadRateTableForm()

    rate_tables = RateTable.objects.filter(user=request.user)
    return render(request, 'common/rate_table_upload.html', {'form': form, 'rate_tables': rate_tables})

def rate_table_list(request):
    # Fetch all rate tables for the current user
    rate_tables = RateTable.objects.filter(user=request.user)

    context = {
        'rate_tables': rate_tables,
    }

    return render(request, 'common/rate_table_list.html', context)

# Import the logging module
def download_rate_table(request, rate_table_id):
    # Fetch the rate table object by ID
    rate_table = get_object_or_404(RateTable, id=rate_table_id)

    # Ensure that the rate table belongs to the current user
    if rate_table.user == request.user:
        # Open the CSV file and create an HttpResponse with the file content
        with open(rate_table.csv_file.path, 'rb') as csv_file:
            response = HttpResponse(csv_file.read(), content_type='text/csv')

        # Modify the filename to include the username
        filename_parts = rate_table.csv_file.name.split('.')
        username = request.user.username
        new_filename = f"{filename_parts[0]}_{username}.{filename_parts[1]}"

        response['Content-Disposition'] = f'attachment; filename="{new_filename}"'
        return response

    # If the rate table doesn't belong to the current user, return a 404 response
    return HttpResponse(status=404)

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def lastratedate_api(request):
    try:
        animal = request.GET.get('animal', '')
        rate_type = request.GET.get('rate_type', '')
        user = request.user
        print(f'Animal: {animal}')
        print(f'Rate Type: {rate_type}')
        print(f'User id  {user.id}')

        if animal == 'BUFFALO':
            animal = 'BUFFALOW'

        csv_file_object = RateTable.objects.filter(rate_type= rate_type,animal_type= animal, user=user.id ).order_by("-uploaded_at") # get the latest csv file object

        if len(csv_file_object) > 0:
            file_path = csv_file_object[0].csv_file.path
            print("In if")
            # Check if the file exists
            if not os.path.exists(file_path):
                print("in 2nd if error one")
                raise FileNotFoundError(f"CSV file not found for {animal}_{rate_type}")


            Response_obj = {'date': csv_file_object[0].start_date.strftime('%d-%m-%Y'), 'file_path': file_path, 'id': csv_file_object[0].id }
            print(Response_obj)
            # Return both the date and the file path
            return JsonResponse(Response_obj)
        else:
            logger.error(f'FileNotFoundError in lastratedate_api: {e}')
            return JsonResponse({'error': 'No csv found' })
    except FileNotFoundError as e:
        # Log the error
        logger.error(f'FileNotFoundError in lastratedate_api: {e}')
        return JsonResponse({'error': 'CSV file not found'}, status=404)

    except Exception as e:
        # Log the error
        logger.exception(f'Error in lastratedate_api: {e}')
        return JsonResponse({'error': 'Internal Server Error'}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def ratesitem_api(request):
    try:
        # Extract parameters from the GET request
        animal = request.GET.get('animal')
        date_str = request.GET.get('date').split("-")
        rate_type = request.GET.get('rate_type')
        item = request.GET.get('item')
        user = request.user
        print(animal, date_str, rate_type, item, user.username, user.id)
        print
        # Convert date string to date object
        date_obj = date(int(date_str[2]), int(date_str[1]), int(date_str[0]))
        
        # Query the RateTable model for the latest CSV file object
        csv_file_object = RateTable.objects.filter(rate_type=rate_type, animal_type=animal, user=user.id, start_date=date_obj).order_by("-uploaded_at")
        
        print("before if")
        print(date_obj)
        if len(csv_file_object) > 0:
            file_path = csv_file_object[0].csv_file.path
            print("file path:", file_path)
            
            # Check if the file exists
            if not os.path.exists(file_path):
                logger.error(f'FileNotFoundError in lastratedate_api: {e}')
                raise FileNotFoundError(f"CSV file not found for {animal}_{rate_type}")
                
            # Read CSV file
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                data = [row for row in reader]
            
            # Find the row corresponding to the requested item
            values_row = None
            for data_row in data:
                if data_row[0] == item:
                    values_row = data_row
                    break
            
            if not values_row:
                return JsonResponse({'error': f'Item not found in CSV {animal}_{rate_type} and {item}'}, status=404)
            
            # Format output
            output_data = {"row": ",".join(values_row)}
            
            return JsonResponse(output_data)

        else:
            return JsonResponse({'error': f'CSV file not found for {animal}_{rate_type} and {user.username}'}, status=404)
    
    except FileNotFoundError as e:
        return JsonResponse({'error': f'CSV file not found for {animal}_{rate_type} and {user.username}'}, status=404)

    except Exception as e:
        # Handle other exceptions appropriately
        print(f'Error in ratesitem_api: {e}')
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
    

@login_required
def shift_report(request):
    # Fetch dynamic values for dropdowns from the database

    # staff and super user
    if request.user.is_staff or request.user.is_superuser:
        locations = DPU.objects.filter(user=request.user).values_list('location', flat=True).distinct()
        dpus = DPU.objects.filter(user=request.user).values_list('st_id', flat=True).distinct()
        societies = DPU.objects.filter(user=request.user).values_list('society', flat=True).distinct()
        shifts = DREC.objects.filter(ST_ID__user=request.user, SHIFT__in=['M', 'E']).values_list('SHIFT', flat=True).distinct()


        # Count distinct locations, dpus, and societies
        total_locations = DPU.objects.filter(user=request.user).values('location').distinct().count()
        total_dpus = DPU.objects.filter(user=request.user).count()
        total_societies = DPU.objects.filter(user=request.user).values('society').distinct().count()
        customer_list = CustomerList.objects.filter(user=request.user)

    else:
        # normal user
        print("before if else")
        locations = DPU.objects.filter(dpu_user=request.user.id).values_list('location', flat=True).distinct()
        dpus = DPU.objects.filter(dpu_user=request.user.id).values_list('st_id', flat=True).distinct()
        societies = DPU.objects.filter(dpu_user=request.user.id).values_list('society', flat=True).distinct()
        shifts = DREC.objects.filter(ST_ID__dpu_user=request.user.id, SHIFT__in=['M', 'E']).values_list('SHIFT', flat=True).distinct()

        print(locations, dpus, societies, shifts)

        # Count distinct locations, dpus, and societies
        total_locations = DPU.objects.filter(user=request.user).values('location').distinct().count()
        total_dpus = DPU.objects.filter(user=request.user).count()
        total_societies = DPU.objects.filter(user=request.user).values('society').distinct().count()
        customer_list = CustomerList.objects.filter(user=request.user)



    # Get initial data for dropdowns
    initial_data = {
        'locations': list(locations),
        'dpus': list(dpus),
        'societies': list(societies),
    }

    context = {
        'locations': locations,
        'dpus': dpus,
        'societies': societies,
        'shifts': shifts,
        'total_locations': total_locations,
        'total_dpus': total_dpus,
        'total_societies': total_societies,
        'initial_data': initial_data,  # Include initial data in the context
        'customer_list': customer_list,  # Include customer list in the context
    }

    if request.method == 'POST':
        location = request.POST.get('location')
        dpu = request.POST.get('dpu')
        society = request.POST.get('society')
        shift = request.POST.get('shift')
        start_date_str = request.POST.get('start_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None

        print("sgnons")
        # Replace the following lines with your actual data retrieval logic
        summary_data = get_summary_data(location, dpu, society, shift, start_date)
        detail_data = get_detail_data(request, location, dpu, society, shift, start_date)


        context.update({
            'selected_location': location,
            'selected_dpu': dpu,
            'selected_society': society,
            'selected_shift': shift,
            'selected_start_date': start_date_str,
            'summary_data': summary_data,
            'detail_data': detail_data,
        })
    print("sgnons ", context)
    return render(request, 'common/shift_report.html', context)

def get_dpus_by_location(request):
    location = request.GET.get('location')
    print("calling in location")
    if request.user.is_staff or request.user.is_superuser:
        print("location if")
        dpus = DPU.objects.filter(user=request.user, location=location).values_list('st_id', flat=True).distinct()
    else:  
        print("location else")  
        dpus = DPU.objects.filter(dpu_user=request.user.id, location=location).values_list('st_id', flat=True).distinct()
    return JsonResponse(list(dpus), safe=False)

def get_societies_by_dpu(request):
    location = request.GET.get('location')
    dpu = request.GET.get('dpu')
    if request.user.is_staff or request.user.is_superuser:
        societies = DPU.objects.filter(user=request.user, location=location, st_id=dpu).values_list('society', flat=True).distinct()
    else:    
        societies = DPU.objects.filter(dpu_user=request.user.id, location=location, st_id=dpu).values_list('society', flat=True).distinct()    
    
    return JsonResponse(list(societies), safe=False)

def get_summary_data(location, dpu, society, shift, start_date):
    # Replace this function with your actual data retrieval logic for summary data
    # Example: Using aggregates to get summary data
    summary_data = DREC.objects.filter(
        ST_ID__location=location,
        ST_ID__st_id=dpu,
        ST_ID__society=society,
        SHIFT=shift,
        RecordingDate=start_date,
    ).aggregate(
        TotalCustomer=Count('CUST_ID'),
        TotalQT=Sum('QT'),
        TotalAmount=Sum('Amount'),
        TotalCAmount=Sum('CAmount'),
        AvgFAT=Round(Avg('FAT'), 1),
        AvgSNF=Round(Avg('SNF'), 1),
        AvgCLR=Round(Avg('CLR'), 1),

    )

    return summary_data

def get_detail_data(request, location, dpu, society, shift, start_date):
    # Replace this function with your actual data retrieval logic for detail data
    # Example: Querying detailed data

    detail_data = DREC.objects.filter(
        ST_ID__location=location,
        ST_ID__st_id=dpu,
        ST_ID__society=society,
        SHIFT=shift,
        RecordingDate=start_date,
    ).values(
        'CUST_ID',
        'MType',
        'FAT',
        'SNF',
        'CLR',
        'WATER',
        'QT',
        'RATE',
        'Amount',
        'CAmount',
    )

    # Fetch customer names for the given st_id and update detail_data
    st_id_customer_names = {customer.cust_id: customer.name for customer in CustomerList.objects.filter(user=request.user, st_id=dpu)}

    for record in detail_data:
        record['CustomerName'] = st_id_customer_names.get(record['CUST_ID'], '')

    return detail_data

import logging

logger = logging.getLogger(__name__)


@login_required
def user_shift_report(request):
    # Retrieve the logged-in user
    user = request.user

    # Retrieve the DPU instance associated with the logged-in user's mobile number
    dpu = get_object_or_404(DPU, mobile_number=user.username)

    # Retrieve dynamic values for dropdowns from the database
    locations = [dpu.location]
    dpus = [dpu.st_id]
    societies = [dpu.society]
    shifts = ['M', 'E']  # Hardcoded shifts for now

    # Count distinct locations, dpus, and societies
    total_locations = 1
    total_dpus = 1
    total_societies = 1

    # Get initial data for dropdowns
    initial_data = {
        'locations': locations,
        'dpus': dpus,
        'societies': societies,
    }

    context = {
        'locations': locations,
        'dpus': dpus,
        'societies': societies,
        'shifts': shifts,
        'total_locations': total_locations,
        'total_dpus': total_dpus,
        'total_societies': total_societies,
        'initial_data': initial_data,  # Include initial data in the context
    }

    if request.method == 'POST':
        location = request.POST.get('location')
        dpu = request.POST.get('dpu')
        society = request.POST.get('society')
        shift = request.POST.get('shift')
        start_date_str = request.POST.get('start_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None

        # Retrieve summary data
        summary_data = get_summary_data(location, dpu, society, shift, start_date)
        print("Summary data:", summary_data)

        # Retrieve detail data
        print("Before calling user_get_detail_data")
        detail_data = user_get_detail_data(request, location, dpu, society, shift, start_date)
        print("After calling user_get_detail_data")
        print("Updated detail data with CustomerName:", detail_data)
        
        context.update({
            'selected_location': location,
            'selected_dpu': dpu,
            'selected_society': society,
            'selected_shift': shift,
            'selected_start_date': start_date_str,
            'summary_data': summary_data,
            'detail_data': detail_data,
        })

    return render(request, 'common/user/user_shift_report.html', context)
def user_get_dpus_by_location(request):
    location = request.GET.get('location')
    user = request.user
    dpus = DPU.objects.filter(user=user, location=location).values_list('st_id', flat=True).distinct()
    return JsonResponse(list(dpus), safe=False)

def user_get_societies_by_dpu(request):
    location = request.GET.get('location')
    dpu = request.GET.get('dpu')
    user = request.user
    societies = DPU.objects.filter(user=user, location=location, st_id=dpu).values_list('society', flat=True).distinct()
    return JsonResponse(list(societies), safe=False)

def user_get_summary_data(user, location, dpu, society, shift, start_date):
    # Replace this function with your actual data retrieval logic for summary data
    # Example: Using aggregates to get summary data
    summary_data = DREC.objects.filter(
        ST_ID__location=location,
        ST_ID__st_id=dpu,
        ST_ID__society=society,
        SHIFT=shift,
        RecordingDate=start_date,
    ).aggregate(
        TotalCustomer=Count('CUST_ID'),
        TotalQT=Sum('QT'),
        TotalAmount=Sum('Amount'),
        TotalCAmount=Sum('CAmount'),
        AvgFAT=Avg('FAT'),
        AvgSNF=Avg('SNF'),
        AvgCLR=Avg('CLR'),
    )

    return summary_data

def user_get_detail_data(request, location, dpu, society, shift, start_date):
    # Retrieve detail data
    detail_data = DREC.objects.filter(
        ST_ID__location=location,
        ST_ID__st_id=dpu,
        ST_ID__society=society,
        SHIFT=shift,
        RecordingDate=start_date,
    ).values(
        'CUST_ID',
        'MType',
        'FAT',
        'SNF',
        'CLR',
        'WATER',
        'QT',
        'RATE',
        'Amount',
        'CAmount',
    )

    # Fetch customer names for the given st_id and update detail_data
    st_id_customer_names = {customer.cust_id: customer.name for customer in CustomerList.objects.filter(st_id=dpu)}

    for record in detail_data:
        cust_id = record['CUST_ID']
        if cust_id in st_id_customer_names:
            record['CustomerName'] = st_id_customer_names[cust_id]
        else:
            record['CustomerName'] = 'Unknown'  # Default to 'Unknown' if customer name not found

    return detail_data







@login_required
def ledger_report(request):
    # Fetch dynamic values for dropdowns from the database
    locations = DPU.objects.filter(user=request.user).values_list('location', flat=True).distinct()
    dpus = DPU.objects.filter(user=request.user).values_list('st_id', flat=True).distinct()
    societies = DPU.objects.filter(user=request.user).values_list('society', flat=True).distinct()

    # Get distinct customer IDs for the current user
    customer_ids = CustomerList.objects.filter(user=request.user).values_list('cust_id', flat=True).distinct()
 # Count distinct locations, dpus, and societies
    total_locations = DPU.objects.filter(user=request.user).values('location').distinct().count()
    total_dpus = DPU.objects.filter(user=request.user).count()
    total_societies = DPU.objects.filter(user=request.user).values('society').distinct().count()
    customer_list = CustomerList.objects.filter(user=request.user)


    context = {
        'locations': locations,
        'dpus': dpus,
        'societies': societies,
        'customer_ids': customer_ids,
        'total_locations': total_locations,
        'total_dpus': total_dpus,
        'total_societies': total_societies,
        'customer_list': customer_list,  # Include customer list in the context

    }

    if request.method == 'POST':
        location = request.POST.get('location')
        dpu = request.POST.get('dpu')
        society = request.POST.get('society')
        start_id = request.POST.get('start_id')
        end_id = request.POST.get('end_id')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        # Parse the start and end dates from the string to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

        # Replace the following lines with your actual data retrieval logic
        
        summary_data = get_ledger_summary_data(location, dpu, society, start_id, end_id, start_date, end_date)
        detail_data = get_ledger_detail_data(location, dpu, society, start_id, end_id, start_date, end_date)
        payment_summary_data = get_payment_summary_data(
                location, dpu, start_date, end_date, start_id, end_id
            )
        context.update({
            'selected_location': location,
            'selected_dpu': dpu,
            'selected_society': society,
            'selected_start_id': start_id,
            'selected_end_id': end_id,
            'selected_start_date': start_date_str,
            'selected_end_date': end_date_str,
            'ledger_summary_data': summary_data,
            'ledger_detail_data': detail_data,
            'payment_summary_data': payment_summary_data,  # Add payment_summary_data to the context

        })

    return render(request, 'common/ledger_report.html', context)

def get_ledger_summary_data(location, dpu, society, start_id, end_id, start_date, end_date):
    # Get distinct customer IDs within the specified range
    distinct_cust_ids = DREC.objects.filter(
        ST_ID__location=location,
        ST_ID__st_id=dpu,
        ST_ID__society=society,
        CUST_ID__gte=start_id,
        CUST_ID__lte=end_id,
        RecordingDate__gte=start_date,
        RecordingDate__lte=end_date
    ).values_list('CUST_ID', flat=True).distinct()

    summary_data_list = []

    for cust_id in distinct_cust_ids:
        # Using aggregates to get summary data for each CUST_ID
        summary_data = DREC.objects.filter(
            ST_ID__location=location,
            ST_ID__st_id=dpu,
            ST_ID__society=society,
            CUST_ID=cust_id,
            RecordingDate__gte=start_date,
            RecordingDate__lte=end_date
        ).values(
            'CUST_ID',
            'ST_ID__location',  # Include location in values
            'ST_ID__society',   # Include society in values
            'ST_ID__st_id',     # Include st_id in values
        ).annotate(
            TotalQT=Sum('QT'),
            TotalAmount=Sum('Amount'),
            TotalCAmount=Sum('CAmount'),
            AvgFAT=Round(Avg('FAT'), 1),
            AvgSNF=Round(Avg('SNF'), 1),
            AvgCLR=Round(Avg('CLR'), 1),
        ).order_by('CUST_ID').first()

        if summary_data:
            # If summary_data is not None, add the cust_id to the summary_data dictionary
            summary_data['CUST_ID'] = cust_id
             # Add customer name to the summary_data
            customer_name = CustomerList.objects.filter(cust_id=cust_id).values_list('name', flat=True).first()
            summary_data['CustomerName'] = customer_name

            # Append the summary_data to the list
            summary_data_list.append(summary_data)

            # Print the values for debugging

    return summary_data_list

def get_ledger_detail_data(location, dpu, society, start_id, end_id, start_date, end_date):
    # Replace this function with your actual data retrieval logic for ledger detail data
  
    # Example: Querying detailed data with select_related
    detail_data = DREC.objects.filter(
        ST_ID__location=location,
        ST_ID__st_id=dpu,
        ST_ID__society=society,
        CUST_ID__gte=start_id,
        CUST_ID__lte=end_id,
        RecordingDate__gte=start_date,
        RecordingDate__lte=end_date
    ).select_related('ST_ID')

    return detail_data

def get_payment_summary_data(location, dpu, start_date, end_date, start_id, end_id):
    payment_data = DREC.objects.filter(
        ST_ID__location=location,
        ST_ID__st_id=dpu,
        RecordingDate__range=[start_date, end_date],
        CUST_ID__range=[start_id, end_id]
    )

    payment_summary_data = {
        'GrandTotalQT': payment_data.aggregate(GrandTotalQT=Sum('QT'))['GrandTotalQT'] or 0,
        'GrandTotalAmount': payment_data.aggregate(GrandTotalAmount=Sum('Amount'))['GrandTotalAmount'] or 0,
        'CustomerData': [],
    }

    # Get individual customer data
    customer_data = payment_data.values('CUST_ID').annotate(
        NoOfShifts=Count('SHIFT'),
        TotalQT=Sum('QT'),
        TotalAmount=Sum('Amount'),
        TotalCAmount=Sum('CAmount'),
        AvgFAT=Round(Avg('FAT'), 1),
        AvgSNF=Round(Avg('SNF'), 1),
        AvgCLR=Round(Avg('CLR'), 1),
        AvgRATE=Round(Avg('RATE'),2),
        
    ).order_by('CUST_ID')

    # Iterate through the customer data and add customer name
    for entry in customer_data:
        cust_id = entry['CUST_ID']
        customer_name = CustomerList.objects.filter(cust_id=cust_id).values_list('name', flat=True).first()
        entry['CustomerName'] = customer_name

    payment_summary_data['CustomerData'] = list(customer_data)

    return payment_summary_data
