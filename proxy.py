import time
import atexit

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
        except Exception as e:
            print(f"Error: {e}", 500)

    app.run(host=server_config.host, port=server_config.port)
