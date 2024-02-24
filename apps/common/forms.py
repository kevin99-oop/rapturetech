from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.userprofile.models import Profile
from django.forms import ModelForm
from django import forms
from apps.common.models import DPU, Customer

# SignUpForm is a custom form that extends UserCreationForm for user registration
class SignUpForm(UserCreationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

        # Update widget attributes for styling
        self.fields['username'].widget.attrs.update({
            'class':'form-control',        
        })
        self.fields['email'].widget.attrs.update({
            'class':'form-control',        
        })
        self.fields['password1'].widget.attrs.update({
            'class':'form-control',        
        })
        self.fields['password2'].widget.attrs.update({
            'class':'form-control',        
        })
    
    # Additional custom fields for username and email
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

# UserForm is a form for updating user information
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email',
        ]
    
# ProfileForm is a form for updating user profile information
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'phone_number',
        ]

# DPUForm is a form for handling DPU model data
class DPUForm(forms.ModelForm):
    class Meta:
        model = DPU
        fields = ['location', 'st_id', 'society', 'mobile_number', 'owner', 'status']

# UploadCSVForm is a form for handling CSV file uploads for the Customer model
class UploadCSVForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['csv_file']

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']

        # Perform any additional validation for the CSV file if needed

        return csv_file
    
# CustomerForm is a form for handling customer-related data
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['st_id', 'csv_file']  # Add 'date_uploaded'

# forms.py
from django import forms
from apps.common.models import RateTable

class UploadRateTableForm(forms.ModelForm):
    class Meta:
        model = RateTable
        fields = ['csv_file']

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']

        # Perform any additional validation for the RateTable CSV file if needed

        return csv_file
