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
from django.contrib.auth import authenticate


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
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser


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
    
    def post(self, request, *args, **kwargs):
        parser_classes = [JSONParser]

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
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
            # Deserialize JSON data using your serializer
            serializer = LoginSerializer(data=request.data)
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

