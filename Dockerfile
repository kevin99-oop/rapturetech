# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM docker.io/python:3.11.7-alpine
ENV ENV=dev
# by default it will choose production database 
WORKDIR /app

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN ls -l
# Mounts the application code to the image
COPY . /app
WORKDIR /app

EXPOSE 8000

# runs the production servers
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]