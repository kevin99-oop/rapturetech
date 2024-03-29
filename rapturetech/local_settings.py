# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Import necessary modules
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Database settings for the project
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Database engine (SQLite in this case)
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # Database file path
    }
}

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'rapturetechdb',
#        'USER': 'rapturetech_mas',
#        'PASSWORD': 'Raptur3t3chN0S3cPass',
#        'HOST': 'db-instance-rapturetech.c7msy0kga8dr.ap-south-1.rds.amazonaws.com',
#        'PORT': '5432'
#    }
# }