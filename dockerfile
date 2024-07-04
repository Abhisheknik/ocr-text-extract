# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Tesseract (adjust paths as needed)
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/
ENV TESSERACT_CMD=/usr/bin/tesseract

# Add Poppler bin directory to PATH if necessary
ENV PATH="${PATH}:/usr/local/bin"

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]
