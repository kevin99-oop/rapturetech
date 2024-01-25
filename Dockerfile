FROM docker.io/python:3.11.7-alpine

WORKDIR /

# Create a non-root user
RUN adduser -D myuser
USER myuser

# Copy only requirements first to leverage Docker cache
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /

EXPOSE 8000

# Set environment variable if needed
# ENV DJANGO_SETTINGS_MODULE=myapp.settings.production

ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]