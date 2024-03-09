FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Install Git
RUN apt-get update && apt-get install -y git iputils-ping net-tools 

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
