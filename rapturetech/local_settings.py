# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Import necessary modules
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# # Database settings for the project

#for dev we need to set env variable 
#for production (export ENV=prod)
print("Current Env:- ",os.getenv("ENV","dev"))
if os.getenv("ENV","dev")=="dev":
    print("dev database selected")
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Database engine (SQLite in this case)
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # Database file path
    }
}
else:
    print("Production database selected")
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Database engine (SQLite in this case)
        'NAME': os.path.join(BASE_DIR, 'production.sqlite3'),  # Database file path
    }
}


# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'rapturedb',
#        'USER': 'sgnonsuser',
#        'PASSWORD': 'SgnRapDbPas01',
#        'HOST': '13.234.226.230',
#        'PORT': '5432'
#    }
# }