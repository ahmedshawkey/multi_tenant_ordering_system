# Use Python 3.10 slim image
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config


# Set working directory
WORKDIR /app

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install pipenv
RUN pip install pipenv

# Copy dependency files first
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

# Copy full project
COPY . .

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
