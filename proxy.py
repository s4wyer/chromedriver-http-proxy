import time
import atexit
import logging

from config import get_configs, ScraperConfig

import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ChromeOptions

from flask import Flask, request


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

        logger.info("Driver started.")

    def cleanup(self):
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Driver closed.")
            except Exception as e:
                logger.error(f"Exception during cleanup: {e}")
            finally:
                self.driver = None

    def render_page(self, url):
        logger.info(f"Fetching {url}...")
        self.driver.get(url)

        WebDriverWait(self.driver, timeout=self.config.wait_time).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

        time.sleep(self.config.wait_time)

        logger.info(f"Fetched {url}.")

        return self.driver.page_source


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    server_config, scraper_config = get_configs()

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
            logger.info(f"Successfully sent {url} to client.")
        except Exception as e:
            logger.error(f"Error sending {url} to client: {e}", 500)

    app.run(host=server_config.host, port=server_config.port)
