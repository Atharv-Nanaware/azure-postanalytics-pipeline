FROM apache/airflow:2.9.3

USER root

# Install system dependencies if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python packages
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Ensure praw is installed explicitly
RUN pip install --no-cache-dir praw==7.8.1 prawcore==2.4.0
