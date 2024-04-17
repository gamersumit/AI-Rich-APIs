# Use the official Python image as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

RUN mkdir /AI-Rich-APIs

# Set work directory
WORKDIR /AI-Rich-APIs

# copy whole project to your docker home directory
ADD . /AI-Rich-APIs/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run the server using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
# CMD ["python", "manage.py", "runserver", "8000"]