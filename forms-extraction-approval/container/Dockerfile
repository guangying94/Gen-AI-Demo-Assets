# Use an official Python runtime as a parent image
FROM python:3.10.12-alpine

# Set the working directory to /app
WORKDIR /app

RUN apk update && apk add --no-cache \
mupdf-dev \
gcc \
libc-dev \
musl-dev \
jbig2dec \
openjpeg-dev \
jpeg-dev \
harfbuzz-dev \
swig \
make \
g++ &&  ln -s /usr/lib/libjbig2dec.so.0 /usr/lib/libjbig2dec.so

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the command to start the Flask app
CMD ["python", "main.py"]