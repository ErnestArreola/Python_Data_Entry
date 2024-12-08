# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirement.txt requirement.txt

# Install the required Python packages
RUN pip install -r requirement.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that your Flask app listens on
EXPOSE 8080

# Start the Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app.app"]
