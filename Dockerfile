FROM python:3.9.6-slim

LABEL version="0.1" \
    description="Telegram bot for seating academic dinner parties (sitsit)" \
    org.opencontainers.image.source="https://github.com/fyysikkokilta/Plaseerausbotti"

COPY . /src
WORKDIR /src

RUN pip install -e . --no-cache-dir

ENTRYPOINT ["python", "plaseerausbotti/main.py"]