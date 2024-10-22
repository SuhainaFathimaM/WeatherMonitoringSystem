# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip and install dependencies from requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container (optional, only if a web server is running)
EXPOSE 80

# Define the command to run your weather_data.py script
CMD ["python", "/app/weather_data.py"]
