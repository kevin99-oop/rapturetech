# # backends.py
# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model
# from .models import DPU  # Import the DPU model from your app

# User = get_user_model()

# class CustomAuthenticationBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         if username is None or password is None:
#             return None
        
#         try:
#             # Check if the username is a mobile number in the DPU model
#             dpu = DPU.objects.get(mobile_number=username)

#             # Verify the password against the plain_password field of the DPU model
#             if dpu.plain_password == password:
#                 # Get or create the associated user object
#                 user, created = User.objects.get_or_create(username=username)
#                 # Update user attributes if necessary
#                 if created:
#                     # Set user attributes based on DPU data if needed
                    
#                     user.set_unusable_password()  # Ensuring password is not usable for authentication
#                     user.save()
#                 # Ensure the user is active
#                 if user.is_active:
#                     return user
#                 else:
#                     return None  # User is not active
#             else:
#                 return None  # Password does not match
#         except DPU.DoesNotExist:
#             # If the username is not found in the DPU model,
#             # try authenticating with the username in the User model
#             return None
