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



import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomerUploadForm
from .models import CustomerUpload

import csv
from django.shortcuts import render, redirect
from .forms import CustomerUploadForm
from .models import CustomerUpload
from apps.common.models import DPU

def customer_upload(request):
    if request.method == 'POST':
        form = CustomerUploadForm(request.POST, request.FILES)
        if form.is_valid():
            st_id = form.cleaned_data['st_id']
            csv_file = form.cleaned_data['csv_file'].read().decode('utf-8').splitlines()

            customer_upload_instance = CustomerUpload(st_id=st_id, csv_file=form.cleaned_data['csv_file'])
            customer_upload_instance.save()

            for row in csv.reader(csv_file):
                cust_id, name, mobile, adhaar, bank_account, ifsc = row
                try:
                    cust_id = int(cust_id)
                except ValueError:
                    continue

                CustomerUpload.objects.create(
                    st_id=st_id,
                    cust_id=cust_id,
                    name=name,
                    mobile=mobile,
                    adhaar=adhaar,
                    bank_account=bank_account,
                    ifsc=ifsc
                )

            return redirect('customer_list')  # Redirect to the customer list view

    else:
        form = CustomerUploadForm()

    return render(request, 'customer_upload.html', {'form': form})

def customer_list(request):
    customers = CustomerUpload.objects.all()
    return render(request, 'common/customer_list.html', {'customers': customers})

class CIDRangeCSVAPIView(APIView):
    def get(self, request, st_id):
        customer_data = CustomerUpload.objects.filter(st_id=st_id)
        if not customer_data.exists():
            return HttpResponse("No customer data found for the specified ST_ID", status=404)

        # Assuming that each customer data object has a unique CSV file
        csv_file_path = customer_data.first().csv_file.path

        with open(csv_file_path, 'rb') as csv_file:
            response = HttpResponse(csv_file.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{st_id}_customer_data.csv"'
            return response