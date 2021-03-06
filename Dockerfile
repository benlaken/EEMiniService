FROM python:3.6-slim
MAINTAINER Benjamin Laken benjamin.laken@vizzuality.com

ENV NAME flask_app
ENV USER microservice

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libssl-dev libffi-dev python-dev \
		curl \
		gcc \
		libbz2-dev \
		libncurses-dev \
		libreadline-dev \
		libsqlite3-dev \
		libssl-dev \
		make \
		zlib1g-dev \
		zip \
		unzip \
		gfortran \
		g++ \
		pkg-config \
		libfreetype6-dev

RUN groupadd -r $USER && useradd -r -g $USER $USER
RUN mkdir -p /opt/$NAME
COPY requirements.txt /opt/$NAME/requirements.txt
RUN cd /opt/$NAME && pip install -r requirements.txt
COPY python_app/main.py /opt/$NAME/python_app/main.py
COPY python_app/gunicorn.py /opt/$NAME/python_app/gunicorn.py
COPY entrypoint.sh /opt/$NAME/entrypoint.sh

# Copy the application folder inside the container
WORKDIR /opt/$NAME

RUN chown $USER:$USER /opt/$NAME
# Tell Docker we are going to use this port
EXPOSE 5000
USER $USER

# Launch script
ENTRYPOINT ["./entrypoint.sh"]
