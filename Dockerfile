FROM python:3.6.5
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y git gcc libglib2.0-0

ADD ./requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -U --no-cache-dir pip setuptools && \
    pip install --no-cache-dir numpy cython && \
    pip install --no-cache-dir -r requirements.txt

ADD . /app
ADD ./start.sh /start.sh

EXPOSE 8000
CMD ["/bin/bash", "/start.sh"]

