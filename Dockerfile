FROM python:2

RUN apt-get update && \
    apt-get install -y libboost-python-dev cmake && \
    apt-get autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    mkdir -p /app

COPY requirements.txt /app

RUN cd /app && \
    virtualenv env && \
    . env/bin/activate && \
    pip install -r requirements.txt

COPY data/ /app/data/
COPY resources/ /app/resources/
COPY src/ /app/src/

CMD ["sleep", "99999"]
