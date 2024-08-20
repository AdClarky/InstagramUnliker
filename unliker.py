import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import history
from urlReader import read_urls
from config import Config

SLEEP_TIME_SECS = 20
LONG_SLEEP_MINS = 60
LONG_PAUSE_AMOUNT = 300


def long_sleep(minutes: int) -> None:
    for i in range(minutes):
        logging.info(f"Sleeping for {minutes - i} minutes...")
        time.sleep(60)


def unlike_all(driver: webdriver.Firefox) -> bool:
    elements = driver.find_elements(By.CSS_SELECTOR, "[aria-label=Unlike]")
    if not len(elements):
        logging.warning(f"No unlike found for {driver.current_url}")
        history.write_empty(driver.current_url)
        return False
    for element in elements:
        element.click()
    time.sleep(SLEEP_TIME_SECS)
    elements = driver.find_elements(By.CSS_SELECTOR, "[aria-label=Unlike]")
    if len(elements):
        logging.warning(f"Rate limited: {driver.current_url}")
        long_sleep(LONG_SLEEP_MINS)
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

    history_urls = history.read()

    urls = read_urls(config.liked_posts_path)
    urls = [url.replace("/reel/", "/reels/") for url in urls]

    done_urls = set(urls).intersection(set(history_urls))
    logging.info(f"Skipping {len(done_urls)} urls that have already been processed.")

    urls = set(urls) - done_urls
    total = len(urls)
    logging.info(f"Processing {len(urls)} urls.")

    options = webdriver.FirefoxOptions()
    options.add_argument("-profile")
    options.add_argument(config.firefox_profile_path)
    driver = webdriver.Firefox(options=options)

    num_processed = 0

    for url in urls:
        logging.info(f"Processing {url}")
        driver.get(url)
        if is_blank(driver):
            logging.error(f"Blank page: {url}")
            history.write_empty(url)
            history.write(url)
            continue
        if unlike_all(driver):
            num_processed += 1
            logging.info(f"#{num_processed} processed, {round((num_processed / total) * 100, 2)}% complete: "
                         f"{driver.current_url}")
            if (num_processed % LONG_PAUSE_AMOUNT) == 0:
                long_sleep(LONG_SLEEP_MINS)

    driver.quit()


if __name__ == '__main__':
    main()
