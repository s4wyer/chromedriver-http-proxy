# chromedriver-http-proxy

Simple HTTP proxy that renders pages with undetected-chromedriver and returns the rendered HTML.

## Features

- Solves [Anubis](https://anubis.techaro.lol/)
- Solves [go-away](https://git.gammaspectra.live/git/go-away)
- Solves similiar POW challenges
- Sometimes bypasses Cloudflare Turnstile

## Installation

uv: 

```sh
sudo apt install chromium # or sudo pacman -S chromium
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
uvx playwright install
```

pip: 

```sh
sudo apt install chromium # or sudo pacman -S chromium
pip install -r requirements.txt
playwright install
```

## Usage

Run `proxy.py`, and make a request to `localhost:32323/?url=https://ifconfig.me`.

You can also pass several arguments.

```sh
# default port: 32323
# default host: 0.0.0.0
# default wait: 10 (seconds)
# default user agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36
# default headless mode: True
python proxy.py --host 127.0.0.1 --port 1337 --wait 5 --headless False --user-agent "Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.0.1) Gecko/20020921 Netscape/7.0"
```

## Notes

I built this mainly to solve Anubis challenges for my Miniflux RSS instance, so it's a little rough around the edges.

This proxy has no authentication, and I don't plan to add any (PRs welcome though!). Don't expose it to the internet.  

## TODO

[ ] Docker image
[ ] Custom Chromium binary locations
[ ] More CLI arguments to control ChromeDriver behavior
[ ] Error handling (404, 403, 429)
[ ] Screenshot endpoint
[ ] Allow custom headers
[ ] POST requests

## Similiar Projects

- [Kad](https://github.com/AmanoTeam/Kad) -  A simple HTTP proxy server that forwards all requests through curl-impersonate 
