#!/bin/bash

# by  default it will run dev database 
export ENV=prod 
python3 manage.py runserver 0:8000