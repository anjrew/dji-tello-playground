FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Update package lists and install dependencies
RUN apt-get update && apt-get install -y \
    git \
    iputils-ping \
    net-tools

# Copy requirements.txt to the container
COPY requirements.txt requirements.txt

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt
