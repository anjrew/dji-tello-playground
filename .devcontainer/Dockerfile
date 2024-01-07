FROM mcr.microsoft.com/vscode/devcontainers/python:3.10

# Install Git
RUN apt-get update && apt-get install -y git

RUN pip install flake8 black isort mypy djitellopy
