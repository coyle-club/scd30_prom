FROM docker.io/python:3.10.4-slim

COPY scd30_prom /app/scd30_prom

COPY setup.py /app/setup.py

RUN pip install -e /app

ENTRYPOINT ["/usr/local/bin/scd30_prom"]
