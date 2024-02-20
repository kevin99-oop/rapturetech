# Standard Library Imports
import csv
import datetime
import logging
# Django Imports
from django.views import View
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Count, Sum, Avg
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from apps.common.models import DREC, DPU, Customer, Config
from django.views.generic import TemplateView, CreateView, View
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from apps.common.serializers import UserSerializer, LoginSerializer, DRECSerializer
from apps.common.forms import SignUpForm, UserForm, ProfileForm, DPUForm, UploadCSVForm

# Django Rest Framework Imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView



# Common Views
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
    
class DashboardView(LoginRequiredMixin, TemplateView):
    # DashboardView class definition ...
    template_name = 'example.html'
    login_url = reverse_lazy('home')

    def summary_view(request):
        summary_data = DREC.objects.values('ST_ID__st_id', 'ST_ID__location', 'ST_ID__society', 'RecordingDate', 'SHIFT').annotate(
            fat_avg=Avg('FAT'),
            snf_avg=Avg('SNF'),
            clr_avg=Avg('CLR'),
            water_avg=Avg('WATER'),
            total_ltr=Sum('QT'),  # Assuming QT represents Total Ltr.
            total_amt=Sum('Amount'),
            total_cust=Sum('CSR_NO')
        )
        print(summary_data)
    def get_context_data(self, **kwargs):
        user = self.request.user
        active_dpu_list = DPU.objects.filter(user=user)
        drec_data = DREC.objects.filter(ST_ID__user=user)
        society_customer_count = DREC.objects.filter(ST_ID__user=user).values(
            'ST_ID__society').annotate(customer_count=Count('CUST_ID', distinct=True))
        context = {
            'active_dpu_list': active_dpu_list,
            'drec_data': drec_data,
            'society_customer_count': society_customer_count,
            'last_updated': timezone.now(),  # Add a timestamp
        }
        return context
    
# User Authentication Views
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
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


class ShiftreportView(LoginRequiredMixin, TemplateView):
    template_name = 'common/shift_report.html'


@login_required
def add_dpu(request):
    if request.method == 'POST':
        form = DPUForm(request.POST)
        if form.is_valid():
            dpu = form.save(commit=False)
            dpu.user = request.user
            dpu.save()
            # Redirect to the user's dashboard or any other page
            return redirect('active_dpu')
    else:
        form = DPUForm()

    return render(request, 'common/add_dpu.html', {'form': form})


def active_dpu(request):
    active_dpu_list = DPU.objects.filter(user=request.user)
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

    return render(request, 'common/dpudetails.html', context)

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

def upload_customer_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            # Extract ST_ID from the first line of the CSV file
            csv_content = csv_file.read().decode('utf-8')
            csv_lines = csv_content.splitlines()
            st_id = csv_lines[0].strip()
            # Extract CUST_ID range dynamically
            # Save the CSV file reference with the corresponding user, ST_ID, and dynamic range
            try:
                Customer.objects.create(
                    user=request.user,
                    st_id=st_id,
                    csv_file=csv_file,
                )
                messages.success(request, 'CSV file uploaded successfully.')
                return redirect('upload_customer_csv')
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {e}')
        else:
            messages.error(
                request, 'Invalid form submission. Please check the file format.')
    else:
        form = UploadCSVForm()
    return render(request, 'common/upload_customer_csv.html', {'form': form})

def download_latest_csv(request, st_id):
    # Get the latest Customer record for the logged-in user and the provided st_id
    latest_customer = get_object_or_404(Customer.objects.filter(
        user=request.user, st_id=st_id).order_by('-date_uploaded')[:1])

    # Open the CSV file and create an HttpResponse with the file content
    with open(latest_customer.csv_file.path, 'rb') as csv_file:
        response = HttpResponse(csv_file.read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{latest_customer.csv_file.name}"'
        return response
    # If there's an issue with the form submission or no st_id is provided, render the form
    return render(request, 'common/dpudetails.html', {'st_id': st_id})
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

def customer_list(request):
    return render(request, 'common/customer_list.html')

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

# apps/common/views.py
from django.shortcuts import render, redirect, get_object_or_404
from apps.common.forms import UploadRateTableForm
from apps.common.models import RateTable
from django.http import HttpResponse

# apps/common/views.py
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from apps.common.forms import UploadRateTableForm
from apps.common.models import RateTable
from django.http import HttpResponse
import csv

# apps/common/views.py
from datetime import datetime
from django.shortcuts import render, redirect
from apps.common.forms import UploadRateTableForm
from apps.common.models import RateTable
from django.http import HttpResponse
import csv
from django.contrib import messages

# views.py
from django.core.exceptions import ValidationError

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

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from apps.common.models import RateTable

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


import csv
import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

logger = logging.getLogger(__name__)

@csrf_exempt
def lastratedate_api(request):
    try:
        animal = request.GET.get('animal', '')
        rate_type = request.GET.get('rate_type', '')
        print(f'Animal: {animal}')
        print(f'Rate Type: {rate_type}')

        if animal == 'BUFFALOW':
            animal = 'BUFFALO'

        # Assuming the CSV files are stored in the 'rate_tables/' directory
        file_pattern = f'{animal[0]}{rate_type}.csv'
        file_path = os.path.join(settings.MEDIA_ROOT, 'rate_tables', file_pattern)

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found for {animal}_{rate_type}")

        # Open the CSV file and read just the first line
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter='\t')  # Assuming it's tab-separated
            # Get the first row from the CSV
            first_row = next(reader)
            # Take the first 10 characters from the first row to get the date
            date_from_csv = first_row[0][:10]

        print(f'Date from CSV: {date_from_csv}')

        # Return both the date and the file path
        return JsonResponse({'date': date_from_csv, 'file_path': file_path})

    except FileNotFoundError as e:
        # Log the error
        logger.error(f'FileNotFoundError in lastratedate_api: {e}')
        return JsonResponse({'error': 'CSV file not found'}, status=404)

    except Exception as e:
        # Log the error
        logger.exception(f'Error in lastratedate_api: {e}')
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from apps.common.models import RateTable
import csv

logger = logging.getLogger(__name__)

@csrf_exempt
def ratesitem_api(request):
    try:
        animal = request.GET.get('animal')
        rate_type = request.GET.get('rate_type')
        date = request.GET.get('date')
        item = request.GET.get('item')

        # Get the latest RateTable entry for the specified animal and rate_type
        latest_rate = RateTable.objects.filter(animal_type=animal, rate_type=rate_type).latest('start_date')

        # Construct the file path based on the latest RateTable entry
        file_path_relative = latest_rate.csv_file.name  # Use the name attribute to get the relative path
        file_path = os.path.join(settings.MEDIA_ROOT, file_path_relative)
        print(f'File path: {file_path}')

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found for {animal}_{rate_type}")

        # Open the CSV file and read the data from the specified row (date) and column (item)
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            date_found = False

            for row in reader:
                if row and row[0] == date:  # Assuming the date is in the first column
                    date_found = True
                    item_index = int(float(item) * 10) + 1  # Assuming items are in increments of 0.1 and starting from the second column

                    if item_index < len(row):
                        row_data = row[item_index]
                        break
                    else:
                        return JsonResponse({'error': f'Item index {item_index} out of range in CSV'}, status=500)

            if not date_found:
                return JsonResponse({'error': f'Data not found for date {date}'}, status=404)

        # Create a JSON response with the row data
        response_data = {'row': row_data}
        return JsonResponse(response_data)

    except FileNotFoundError as e:
        # Log the error
        logger.error(f'FileNotFoundError in ratesitem_api: {e}')
        return JsonResponse({'error': 'CSV file not found'}, status=404)

    except RateTable.DoesNotExist:
        return JsonResponse({'error': 'No rate data available for the specified animal and rate_type.'}, status=404)

    except Exception as e:
        # Log the error
        logger.exception(f'Error in ratesitem_api: {e}')
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
