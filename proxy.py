import time
from dataclasses import dataclass
import argparse
import atexit

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
        self._setup_driver()

    def _setup_driver(self):
        chrome_options = ChromeOptions()
        chrome_options.add_argument(f"--user-agent={self.config.user_agent}")

        self.driver = uc.Chrome(
            headless=self.config.headless,
            options=chrome_options,
            use_subprocess=False
        )

    def cleanup(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error during cleanup: {e}")
            finally:
                self.driver = None

    def render_page(self, url):
        self.driver.get(url)

        WebDriverWait(self.driver, timeout=self.config.wait_time).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        time.sleep(self.config.wait_time)

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

    server_config = ServerConfig(host=args.host, port=args.port)
    scraper_config = ScraperConfig(wait_time=args.wait, headless=args.headless, user_agent=args.user_agent)

    scraper = Scraper(scraper_config)

    atexit.register(scraper.cleanup)

    # run the server
    app = Flask(__name__)

    @app.route("/")
    def proxy_route():
        url = request.args.get("url")

        try:
            html = scraper.render_page(url)
            return html
        except Exception as e:
            print(f"Error: {e}", 500)

    app.run(host=server_config.host, port=server_config.port)
