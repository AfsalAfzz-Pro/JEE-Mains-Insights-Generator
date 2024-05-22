# Use a Python slim base image
FROM python:3.9-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app3

# Copy just the requirements file first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Second stage for the final image
FROM python:3.9-slim AS final

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app3

# Copy installed dependencies from the base image
COPY --from=base /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the rest of the application code
COPY . .

# Expose port (consider using a higher port number for non-root access)
EXPOSE 8000

# Command to run the application
CMD python manage.py runserver 0.0.0.0:80