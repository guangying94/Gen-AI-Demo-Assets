# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install necessary packages
# RUN apt update && apt upgrade -y

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 8501 for the Flask app
EXPOSE 8501

# Run the command to start the Flask app
CMD ["streamlit", "run", "Home.py", "--server.port", "8501"]