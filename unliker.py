import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from urlReader import read_urls
from config import Config


def unlike_all(driver: webdriver.Firefox):
    elements = driver.find_elements(By.CSS_SELECTOR, "[aria-label=Unlike]")
    if not len(elements):
        logging.warning(f"[WARNING] No unlike found for {driver.current_url}")
    for element in elements:
        element.click()


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    config = Config("config.json")

    urls = read_urls(config.liked_posts_path)

    options = webdriver.FirefoxOptions()
    options.add_argument("-profile")
    options.add_argument(config.firefox_profile_path)
    driver = webdriver.Firefox(options=options)

    for url in urls:
        logging.info(f"Processing {url}")
        driver.get(url)
        time.sleep(10)
        unlike_all(driver)
        time.sleep(10)


if __name__ == '__main__':
    main()
