# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
# PYTHONUNBUFFERED ensures that Python output is sent straight to the terminal without being buffered first.
ENV PYTHONUNBUFFERED True
# Set the port the application will listen on. Cloud Run and App Hosting will inject this.
ENV PORT 5000

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be required by Python packages (e.g., for TensorFlow)
# This is a common set; you might need to adjust based on specific library needs if errors occur during pip install.
# For TensorFlow, full build dependencies can be extensive. Using a pre-built TensorFlow wheel usually helps.
# If CPU-only TensorFlow is sufficient (as often is for inference or lighter tasks in smaller containers):
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
# Commenting out apt-get for now to keep the image smaller, assuming wheels will work.

# Install missing os dependencies
RUN apt-get update && apt-get install -y libglib2.0-0 libx11-6 libxext6 libxrender1 libxft2

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# It's good practice to upgrade pip first.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the working directory
COPY . .

# Expose the port the app runs on
EXPOSE ${PORT}

# Define the command to run the application using Gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 600 main:app