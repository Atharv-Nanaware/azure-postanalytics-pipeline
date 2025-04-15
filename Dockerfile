FROM apache/airflow:2.9.3

USER root


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow


COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt


RUN pip install --no-cache-dir praw==7.8.1 prawcore==2.4.0
