FROM python:3.7.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gcc \
    libglib2.0-0 \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -U --no-cache-dir pip setuptools && \
    pip install --no-cache-dir numpy cython && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app
COPY ./start.sh /start.sh

EXPOSE 8000
CMD ["/bin/bash", "/start.sh"]

