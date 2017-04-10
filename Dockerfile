FROM python:2.7

COPY requirements.txt /tmp

RUN groupadd --gid 1000 user && \
    useradd --uid 1000 --gid user --shell /bin/bash --create-home user && \
    apt-get update && \
    apt-get install -y libboost-python-dev cmake && \
    apt-get autoremove && \
    apt-get clean && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    mkdir -p /app && \
    chown user:user /app

USER user
WORKDIR /app

COPY resources/ /app/resources/
COPY src/ /app/src/

CMD ["sleep", "99999"]
