FROM python:3.11-slim

RUN set -eux; \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        curl \
        locales && \
    localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/* 

RUN pip3 install -U pip wheel setuptools

WORKDIR /app

# Copy requirements file separately to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip3 install -r requirements.txt --no-cache-dir

# Copy the rest of the application
COPY . .

EXPOSE 5200

ENV LANG en_US.utf8

CMD ["python3", "pdf_filler/app.py"]

HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://0.0.0.0:5200/ || exit 1