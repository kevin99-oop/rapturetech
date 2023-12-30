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
from apps.common.serializers import UserSerializer, LoginSerializer,DRECSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions, authentication

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
from rest_framework.authtoken.views import ObtainAuthToken
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
from rest_framework.decorators import parser_classes
from rest_framework.authtoken.models import Token

# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.common.models import Customer
from apps.common.forms import CustomerForm
# common/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from .models import Customer
from .serializers import CustomerSerializer
import pandas as pd  # Assuming you use pandas for Excel processing
import csv
import requests
import csv
from io import TextIOWrapper

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
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        # Render the login template after a successful login
        return render(request, 'common/login.html', {'token': token.key, 'user_id': token.user_id})
    
    def get(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid() == 'text/plain' :
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Add your authentication logic here (e.g., using Django's built-in authentication)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Authentication successful, create or retrieve a token
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Invalid input data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
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
                    return Response({"token": token.key}, status=status.HTTP_200_OK, content_type='application/text')
                else:
                    # Authentication failed
                    return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED, content_type='application/text')
            else:
                # Invalid input data
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type='application/text')
        except Exception as e:
            # Handle other exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/text')

    
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

def customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            excel_data = read_excel_data(form.cleaned_data['excel_file'])
            call_api_custupload(excel_data)
            return HttpResponse("File uploaded successfully and API called.")
    else:
        form = CustomerForm()

    return render(request, 'common/customer_list.html', {'form': form})

def read_excel_data(excel_file):
    csv_data = []
    with TextIOWrapper(excel_file, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_data.append(row)
    return csv_data

def call_api_custupload(csv_data):
    api_url = 'http://3.87.129.89:8000/api/custupload'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, json=csv_data, headers=headers)

    if response.status_code == 200:
        print("API call successful")
    else:
        print(f"API call failed with status code: {response.status_code}")
from django.http import JsonResponse

def custload(request):
    if request.method == 'POST':
        # Handle POST request logic here
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
def customer_list(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    customers = Customer.objects.all()
    print(customers)  # Add this line to check if customers are retrieved
    return render(request, 'common/customer_list.html', {'customers': customers})


class DRECCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        dpuid = data.get('dpuid', None)

        try:
            dpu = DPU.objects.get(dpu_id=dpuid)
        except DPU.DoesNotExist:
            return Response({"error": f"DPU with dpuid {dpuid} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DRECSerializer(data=data)

        if serializer.is_valid():
            serializer.validated_data['dpu'] = dpu
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)