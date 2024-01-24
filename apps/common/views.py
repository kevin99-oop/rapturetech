from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import SignUpForm, UserForm, ProfileForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from apps.userprofile.models import Profile
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from apps.common.serializers import UserSerializer, LoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions, authentication
import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from apps.common.forms import DPUForm
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from .models import DPU
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from apps.common.models import DREC
from apps.common.serializers import DRECSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.common.models import DREC  # Import your Drec model
from django.shortcuts import render, get_object_or_404
from apps.common.models import DPU
from django.db.models import Count
from django.contrib import messages
from django.db.models import Sum,Avg
import csv
import logging
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from apps.common.models import Customer
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadCSVForm
from .models import Customer
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib import messages
from apps.common.forms import UploadCSVForm
from apps.common.models import Customer
from io import TextIOWrapper
import csv



class HomeView(TemplateView):
    template_name = 'common/index.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        print(self.request.user.id)
        context['book_list'] = self.request.user
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
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
        society_customer_count = DREC.objects.filter(ST_ID__user=user).values('ST_ID__society').annotate(customer_count=Count('CUST_ID', distinct=True))

        context = {
            'active_dpu_list': active_dpu_list,
            'drec_data': drec_data,
            'society_customer_count': society_customer_count,
            'last_updated': timezone.now(),  # Add a timestamp

        }
        return context

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
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']

                # Add your authentication logic here (e.g., using Django's built-in authentication)
                user = authenticate(request, username=username, password=password)

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
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

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
            return redirect('add_dpu')  # Redirect to the user's dashboard or any other page
    else:
        form = DPUForm()
    
    return render(request, 'common/add_dpu.html', {'form': form})

def active_dpu(request):
    active_dpu_list = DPU.objects.filter(user=request.user)
    return render(request, 'common/active_dpu.html', {'active_dpu_list': active_dpu_list})

def custom_logout(request):
    logout(request)
    # Additional logout logic if needed
    return redirect('home')  # Redirect to the home page or another URL

class DRECViewSet(viewsets.ModelViewSet):
    queryset = DREC.objects.all()
    serializer_class = DRECSerializer

    def perform_create(self, serializer):
        # You can customize the save process here before calling the super method
        instance = serializer.save()

        # Additional logic, if needed
        # For example, you can perform some actions based on the created instance

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = 200  # Set the status code to 200
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
        current_datetime = datetime.datetime.now()

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
class CacheControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'max-age=86400'  # Cache for one day
        return response
# views.py

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
            return redirect('active_dpu')  # Redirect to the desired page after editing
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
            messages.error(request, 'Invalid form submission. Please check the file format.')
    else:
        form = UploadCSVForm()

    return render(request, 'common/upload_customer_csv.html', {'form': form})
def download_latest_csv(request):
    if request.method == 'POST':
        st_id = request.POST.get('st_id')
        if st_id:
            # Get the latest Customer record for the logged-in user and the provided st_id
            latest_customer = get_object_or_404(Customer, user=request.user, st_id=st_id)

            # Open the CSV file and create an HttpResponse with the file content
            with open(latest_customer.csv_file.path, 'rb') as csv_file:
                response = HttpResponse(csv_file.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{latest_customer.csv_file.name}"'
                return response

    # If there's an issue with the form submission or no st_id is provided, render the form
    return render(request, 'common/dpudetails.html')



import csv
import logging
from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from .models import Customer
from rest_framework.decorators import api_view

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
# views.py
# views.py

from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from .models import Customer

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
# views.py
# views.py

# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.common.models import TextFile
from apps.common.serializers import TextFileSerializer
from rest_framework.permissions import IsAuthenticated

class TextFileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        st_id = request.data.get('st_id')
        file = request.data.get('file')

        # Validate st_id and file
        if not st_id or not file:
            return Response({'error': 'Invalid st_id or file'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a TextFile instance
        text_file = TextFile(user=user, st_id=st_id, file=file)
        text_file.save()

        # Serialize the response
        serializer = TextFileSerializer(text_file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        # Retrieve and serialize all text files
        text_files = TextFile.objects.all()
        serializer = TextFileSerializer(text_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
