from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.userprofile.models import Profile
from django.forms import ModelForm
from django import forms
from apps.common.models import DPU, Customer,Questions
from django import forms
from apps.common.models import RateTable

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
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.is_staff = True  # Set the user as staff
        if commit:
            user.save()
        return user
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # Perform custom validation or authentication logic here
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError('Invalid username or password.')

        # Check user type
        user_type = self.get_user_type(user)
        if user_type not in ['super_admin', 'admin', 'user']:
            raise ValidationError('Invalid user type.')

        cleaned_data['user'] = user
        cleaned_data['user_type'] = user_type
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')

    def get_user_type(self, user):
        # Implement your logic to determine the user type here
        # Replace this with your actual logic to determine the user type
        # For example, if you have a user_type attribute on your user model:
        # return user.user_type
        # Replace this with your actual logic to determine the user type
        return 'user'  # Placeholder logic

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
    check_options = forms.MultipleChoiceField(
        choices=DPU.CHECKBOX_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = DPU
        fields = [
            'zone', 'location', 'st_id', 'society', 'mobile_number', 'owner', 'status', 'select_dpu', 'check_options'
        ]
        widgets = {
            'zone': forms.TextInput(attrs={'placeholder': 'Enter Zone'}),
            'location': forms.TextInput(attrs={'placeholder': 'Enter Root'}),
            'st_id': forms.TextInput(attrs={'placeholder': 'Enter Station id'}),
            'society': forms.TextInput(attrs={'placeholder': 'Enter Society'}),
            'mobile_number': forms.TextInput(attrs={'placeholder': 'Enter Mobile Number'}),
            'owner': forms.TextInput(attrs={'placeholder': 'Enter Owner Name'}),
            'status': forms.Select(attrs={'placeholder': 'Select Status'}),
            'select_dpu': forms.RadioSelect,
        }

    def clean_check_options(self):
        check_options = self.cleaned_data.get('check_options', [])
        return ','.join(check_options)


# UploadCSVForm is a form for handling CSV file uploads for the Customer model
class UploadCSVForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['csv_file']

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        return csv_file
    
    
# CustomerForm is a form for handling customer-related data
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['st_id', 'csv_file']  # Add 'date_uploaded'


class UploadRateTableForm(forms.ModelForm):
    class Meta:
        model = RateTable
        fields = ['csv_file']

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']

        # Perform any additional validation for the RateTable CSV file if needed

        return csv_file

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['description']


