FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Install Git
RUN apt-get update && apt-get install -y git

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
