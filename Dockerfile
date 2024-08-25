FROM ubuntu:22.04

ARG PYTHON_VERSION=3.10

RUN apt-get update && \
    apt-get install -y python${PYTHON_VERSION} python3-pip && \
    apt-get clean

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
&& apt-get -y install --no-install-recommends postgresql-client \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN pip install --default-timeout=1000 future
RUN pip3 install -r requirements.txt

COPY start.sh /app
RUN chmod 777 /app/start.sh

CMD ["/app/start.sh"]
# CMD ["chainlit", "run", "app.py"]