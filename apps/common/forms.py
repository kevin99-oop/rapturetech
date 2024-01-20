from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from apps.userprofile.models import Profile
from django.forms import ModelForm
from django import forms
from apps.common.models import DPU,Customer


class SignUpForm(UserCreationForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

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
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email',

            
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
      
            'phone_number',
        ]

# forms.py


class DPUForm(forms.ModelForm):
    class Meta:
        model = DPU
        
        fields = ['location', 'st_id', 'society', 'mobile_number', 'owner', 'status']


class UploadCSVForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['csv_file']