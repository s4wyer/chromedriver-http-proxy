import time
from dataclasses import dataclass
import argparse

import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions

from flask import Flask, request


@dataclass
class ScraperConfig:
    wait_time: float
    headless: bool
    user_agent: str


@dataclass
class ServerConfig:
    host: str
    port: int


class Scraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.driver = None

    def __enter__(self):
        self._setup_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cleanup()

    def _cleanup(self):
        driver = self.driver
        driver.close()
        driver.quit()

    def _setup_driver(self):
        chrome_options = ChromeOptions()
        chrome_options.add_argument(f"--user-agent={self.config.user_agent}")

        self.driver = uc.Chrome(
            headless=self.config.headless,
            options=chrome_options,
            use_subprocess=False
        )

    def render_page(self, url):
        wait_time = self.config.wait_time
        driver = self.driver

        driver.get(url)

        WebDriverWait(self.driver, wait_time).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        time.sleep(wait_time)

        return self.driver.page_source


if __name__ == "__main__":
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

    port = args.port
    host = args.host

    wait = args.wait
    headless = args.headless
    user_agent = args.user_agent

    server_config = ServerConfig(host=host, port=port)
    scraper_config = ScraperConfig(wait_time=wait, headless=headless, user_agent=user_agent)

    # run the server
    app = Flask(__name__)

    @app.route("/")
    def proxy_route():
        url = request.args.get("url")
        with Scraper(scraper_config) as scraper:
            try:
                html = scraper.render_page(url)
                return html
            except Exception as e:
                print(f"Error: {e}")

    app.run(host=server_config.host, port=server_config.port)
