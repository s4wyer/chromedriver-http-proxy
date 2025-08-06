FROM ghcr.io/astral-sh/uv:debian-slim

ENV PROXY_PORT=32323
ENV PROXY_HOST=0.0.0.0
ENV SCRAPER_WAIT_TIME=10
ENV SCRAPER_HEADLESS=True
ENV SCRAPER_USER_AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"

WORKDIR /app
COPY uv.lock pyproject.toml /app
RUN uv sync --locked

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

COPY . /app

CMD uv run proxy.py \
    --port="$PROXY_PORT"\
    --host="$PROXY_HOST"\
    --wait="$SCRAPER_WAIT_TIME" \
    --headless="$SCRAPER_HEADLESS" \
    --user-agent="$SCRAPER_USER_AGENT"
