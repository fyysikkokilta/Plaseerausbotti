# Plaseerausbotti

Telegram bot for seating academic dinner parties (sitsit).

Currently, very much work in progress.


## Running Docker
1. Make a `.env`-file containing `PLASSIBOT_TOKEN` and the corresponding token.
2. Run Docker with
    ```bash
    docker run -d --env-file .env ghcr.io/fyysikkokilta/plaseerausbotti
    ```