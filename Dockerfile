FROM python:3.10.2-slim
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

LABEL version="0.1" \
    description="Telegram bot for seating academic dinner parties (sitsit)" \
    org.opencontainers.image.source="https://github.com/fyysikkokilta/Plaseerausbotti"

COPY . /src
WORKDIR /src

RUN pip install -e . --no-cache-dir

ENTRYPOINT ["python", "plaseerausbotti/main.py"]