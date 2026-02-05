# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim as base

ARG DEBIAN_FRONTEND=noninteractive

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"


# Set the port the application will listen on. Cloud Run and App Hosting will inject this.
ENV PORT 5000

WORKDIR /app

# Install wheel files to speed up builds.
# This step is optional but recommended for production deployments.
# To generate the wheel files, run:
#   pip wheel -r requirements.txt -w wheelhouse/
# and place the generated wheelhouse/ directory alongside this Dockerfile.
# Then, the following lines will copy and use them during pip install.
# COPY wheelhouse/ ./wheelhouse/
# ENV PIP_NO_INDEX=1
# ENV PIP_FIND_LINKS=./wheelhouse/

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/app" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install missing os dependencies
RUN DEBIAN_FRONTEND=${DEBIAN_FRONTEND} apt-get update && \
    apt-get install -y --no-install-recommends \
      libglib2.0-0 \
      libx11-6 \
      libxext6 \
      libxrender1 \
      libxft2 && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
# It's good practice to upgrade pip first.
COPY requirements.txt .

RUN python -m venv ${VIRTUAL_ENV}

RUN pip install --upgrade pip --no-cache-dir && \
    pip install -r requirements.txt --no-cache-dir

# Ensure appuser has a writable HOME at runtime.
ENV HOME=/app
RUN chown -R appuser:appuser /app

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port the app runs on
EXPOSE ${PORT}

# Define the command to run the application using Gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 600 main:app
