import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import history
from urlReader import read_urls
from config import Config


def unlike_all(driver: webdriver.Firefox):
    elements = driver.find_elements(By.CSS_SELECTOR, "[aria-label=Unlike]")
    if not len(elements):
        logging.warning(f"No unlike found for {driver.current_url}")
        history.write_empty(driver.current_url)
    for element in elements:
        element.click()
    history.write(driver.current_url)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    config = Config("config.json")

    done_urls = history.read()

    urls = read_urls(config.liked_posts_path)

    options = webdriver.FirefoxOptions()
    options.add_argument("-profile")
    options.add_argument(config.firefox_profile_path)
    driver = webdriver.Firefox(options=options)

    for url in urls:
        if url in done_urls:
            logging.info(f"Skipping as already processed: {url}")
            continue
        logging.info(f"Processing {url}")
        driver.get(url)
        time.sleep(10)
        unlike_all(driver)
        time.sleep(10)

    driver.quit()


if __name__ == '__main__':
    main()
