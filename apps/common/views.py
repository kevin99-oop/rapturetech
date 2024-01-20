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
            # Check if the status has changed
            if dpu.status != form.cleaned_data['status']:
                return JsonResponse({'status_changed': True})
            form.save()
            return redirect('active_dpu')  # Redirect to the desired page after editing
    else:
        form = DPUForm(instance=dpu)
    
    return render(request, 'common/edit_dpu.html', {'form': form, 'dpu': dpu})
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadCSVForm
from .models import Customer
from io import TextIOWrapper
import csv
from django.http import HttpResponse

def upload_customer_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        
        # Read the CSV file
        csv_content = csv_file.read().decode('utf-8')
        csv_lines = csv_content.splitlines()

        # Extract ST_ID from the first line
        st_id = csv_lines[0].strip()

        # Check if DPU with the specified ST_ID exists
        try:
            dpu = DPU.objects.get(st_id=st_id)
            related_to_user = False
        except DPU.DoesNotExist:
            # Handle the case where no DPU is found
            related_to_user = True

        # Save the CSV file reference with the corresponding DPU and User
        try:
            Customer.objects.create(
                user=request.user,
                st_id=st_id,
                csv_file=csv_file,
                related_to_user=related_to_user,
            )
            messages.success(request, 'CSV file uploaded successfully.')
            return redirect('upload_customer_csv')  # Redirect to the same page after successful upload
        except Exception as e:
            messages.error(request, f'Error processing CSV file: {e}')

    return render(request, 'common/upload_customer_csv.html', {'form': UploadCSVForm()})
def customer_data(request):
    customers = Customer.objects.filter(user=request.user)
    return render(request, 'common/upload_customer_csv.html', {'customers': customers})
def download_latest_csv(request):
    # Get the latest Customer record for the logged-in user
    latest_customer = Customer.objects.filter(user=request.user).order_by('-id').first()

    if latest_customer:
        # Open the CSV file and create an HttpResponse with the file content
        with open(latest_customer.csv_file.path, 'rb') as csv_file:
            response = HttpResponse(csv_file.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{latest_customer.csv_file.name}"'
            return response
    else:
        return HttpResponse("No CSV file found for download.")
import csv
from io import StringIO
from django.http import JsonResponse
from .models import Customer

def get_cid_range(request):
    dpuid = request.GET.get('dpuid', '')

    try:
        # Fetch the latest Customer entry for the given dpuid
        latest_customer = Customer.objects.filter(st_id=dpuid).latest('id')
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'No CSV file found for the specified dpuid.'}, status=404)

    # Retrieve start and end range from the latest_customer model
    start_range = latest_customer.start_range
    end_range = latest_customer.end_range

    # Prepare the JSON response with the range values
    response_data = {'noofcustomer': f'{start_range},{end_range}'}

    return JsonResponse(response_data)


# apps/common/utils.py


def get_customer_data_range(dpuid, start_range, end_range):
    try:
        customer = Customer.objects.filter(st_id=dpuid).latest('id')
        csv_file_path = customer.csv_file.path

        with open(csv_file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            data_range = []

            for row in reader:
                cust_id = int(row.get('CUST_ID', 0))

                if start_range <= cust_id <= end_range:
                    data_range.append(row)

        return data_range
    except Customer.DoesNotExist:
        return []  # Handle case where no customer with the given dpuid is found
    except Exception as e:
        print(f"Error retrieving data range: {e}")
        return []
from django.http import JsonResponse
from .models import Customer

def get_cid_range(request):
    dpuid = request.GET.get('dpuid', '')

    try:
        # Fetch the latest Customer entry for the given dpuid for all users
        latest_customer = Customer.objects.filter(st_id=dpuid).latest('id')

        # Retrieve start and end range from the latest_customer model
        start_range = latest_customer.start_range
        end_range = latest_customer.end_range

        # Prepare the JSON response with the range values
        response_data = {'noofcustomer': f'{start_range},{end_range}'}

        return JsonResponse(response_data)

    except Customer.DoesNotExist:
        return JsonResponse({'error': 'No CSV file found for the specified dpuid.'}, status=404)

    except Exception as e:
        return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)

    
def cust_info(request):
    # Retrieve dpuid and cid from the request
    dpuid = request.GET.get('dpuid', '')
    cid = request.GET.get('cid', '')

    try:
        # Assuming you have a method to get the CSV data based on dpuid
        csv_data = get_csv_data(dpuid)

        # Parse the CSV data
        csv_file = StringIO(csv_data)
        reader = csv.DictReader(csv_file)

        # Find the row with the matching CUST_ID
        for row in reader:
            if row.get('CUST_ID') == cid:
                # Extract additional fields
                cust_id = row.get('CUST_ID')
                name = row.get('NAME')
                mobile = row.get('MOBILE')
                adhaar = row.get('ADHHAR')
                bank_account = row.get('BANK AC')
                ifsc = row.get('IFSC')

                # Construct the response
                response_data = {
                    'dpuid': dpuid,
                    'cid': cid,
                    'cust_id': cust_id,
                    'name': name,
                    'mobile': mobile,
                    'adhaar': adhaar,
                    'bank_account': bank_account,
                    'ifsc': ifsc,
                    # Add other fields as needed
                }

                return JsonResponse(response_data)

        # If the loop completes without finding a matching CUST_ID
        return JsonResponse({'error': 'Customer not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def get_csv_data(dpuid):
    try:
        # Assuming you have a model named Customer with a FileField named csv_file
        customer = Customer.objects.get(st_id=dpuid)

        # Assuming the csv_file field contains the path to the CSV file
        csv_file_path = customer.csv_file.path

        with open(csv_file_path, 'r') as file:
            csv_data = file.read()

        return csv_data

    except Customer.DoesNotExist:
        return f'Customer with dpuid {dpuid} not found'

    except Exception as e:
        return f'Error retrieving CSV data: {str(e)}'