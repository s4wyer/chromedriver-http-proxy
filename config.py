import argparse
from dataclasses import dataclass


@dataclass
class ScraperConfig:
    wait_time: float
    headless: bool
    user_agent: str


@dataclass
class ServerConfig:
    host: str
    port: int


def get_configs():
    parser = argparse.ArgumentParser(prog="ChromeDriver HTTP Proxy",
                                     description="Simple HTTP proxy that renders pages with undetected-chromedriver and returns the HTML",
                                     usage="")
    parser.add_argument(
        "--port",
        help="Port the proxy runs on.",
        required=False,
        type=int,
        default=32323
    )

    parser.add_argument(
        "--host",
        help="Host the proxy to runs on.",
        required=False,
        type=str,
        default="0.0.0.0"
    )

    parser.add_argument(
        "--wait",
        help="Seconds to wait before returning content.",
        required=False,
        type=float,
        default=10
    )

    parser.add_argument(
        "--headless",
        help="Whether or not to run Chrome headless.",
        required=False,
        type=bool,
        default=True
    )

    parser.add_argument(
        "--user-agent",
        help="Chrome user agent. Changing with the current ChromeDriver version recommended.",
        required=False,
        type=str,
        default="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    )

    args = parser.parse_args()

    server_config = ServerConfig(host=args.host,
                                 port=args.port)

    scraper_config = ScraperConfig(wait_time=args.wait,
                                   headless=args.headless,
                                   user_agent=args.user_agent)

    return server_config, scraper_config
