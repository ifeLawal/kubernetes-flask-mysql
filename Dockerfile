FROM python:3.6-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install \
    nginx \
    python3-dev \
    build-essential \
    default-libmysqlclient-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt --src /usr/local/src

COPY . .

EXPOSE 5000
CMD [ "python3", "flaskapi.py" ]
