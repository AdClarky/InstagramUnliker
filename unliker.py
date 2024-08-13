import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import history
from urlReader import read_urls
from config import Config

SLEEP_TIME = 20
SLEEP_MIN_LONG = 20


def unlike_all(driver: webdriver.Firefox) -> bool:
    elements = driver.find_elements(By.CSS_SELECTOR, "[aria-label=Unlike]")
    if not len(elements):
        logging.warning(f"No unlike found for {driver.current_url}")
        history.write_empty(driver.current_url)
        return False
    for element in elements:
        element.click()
    time.sleep(SLEEP_TIME)
    elements = driver.find_elements(By.CSS_SELECTOR, "[aria-label=Unlike]")
    if len(elements):
        logging.warning(f"Rate limited: {driver.current_url}")
        for i in range(SLEEP_MIN_LONG):
            logging.info(f"Sleeping for {SLEEP_MIN_LONG-i} minutes...")
            time.sleep(60)
        unlike_all(driver)
    history.write(driver.current_url)
    return True


def is_blank(driver: webdriver.Firefox) -> bool:
    head = driver.find_elements(By.XPATH, "//div[1]")
    return head == []


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    config = Config("config.json")

    done_urls = history.read()

    urls = read_urls(config.liked_posts_path)
    urls = [url.replace("/reel/", "/reels/") for url in urls]

    options = webdriver.FirefoxOptions()
    options.add_argument("-profile")
    options.add_argument(config.firefox_profile_path)
    driver = webdriver.Firefox(options=options)

    num_processed = 0

    for url in urls:
        if url in done_urls:
            logging.info(f"Skipping as already processed: {url}")
            continue
        logging.info(f"Processing {url}")
        driver.get(url)
        if is_blank(driver):
            logging.error(f"Blank page: {url}")
            history.write_empty(url)
            history.write(url)
            continue
        if unlike_all(driver):
            num_processed += 1
            logging.info(f"Successfully processed #{num_processed}: {driver.current_url}")

    driver.quit()


if __name__ == '__main__':
    main()
