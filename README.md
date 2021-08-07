# Plaseerausbotti

Telegram bot for seating academic dinner parties (sitsit).

Currently, very much work in progress.


## Deployment with Docker
1. Make a `.env`-file containing `PLASSIBOT_TOKEN` and the corresponding token.
2. Run Docker with
    ```bash
    docker run -d --env-file .env ghcr.io/fyysikkokilta/plaseerausbotti
    ```
    
## Development

1. Clone the repo
2. Install dependencies
    ```bash
    pip install -e .
    ```
    (optional) or the testing dependencies as well
    ```bash
    pip install -e .[test]
    ```
3. Start coding!
