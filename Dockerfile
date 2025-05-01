FROM apache/airflow:2.8.1-python3.11

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-venv python3-dev build-essential \
    libglib2.0-0 libnss3 libgconf-2-4 libx11-xcb1 \
    libxrandr2 libxdamage1 libxcomposite1 libasound2 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libgbm1 libgtk-3-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/acploads

COPY ./acploads/requirements.txt /opt/acploads/requirements.txt

RUN python3 -m venv /opt/acploads/.venv && \
    /opt/acploads/.venv/bin/pip install --no-cache-dir -U pip setuptools wheel && \
    /opt/acploads/.venv/bin/pip install --no-cache-dir -r /opt/acploads/requirements.txt

USER airflow

ENV PATH="/opt/acploads/.venv/bin:$PATH"
