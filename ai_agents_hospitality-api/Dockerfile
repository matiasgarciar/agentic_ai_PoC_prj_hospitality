# Use the official Python image from the Docker Hub
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make the start script executable for proper signal handling
RUN chmod +x start.sh

# Expose the port (default 8001 for this service)
EXPOSE 8001

# Command to run the application
CMD ["/bin/bash", "start.sh"]



