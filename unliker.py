import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import history
from urlReader import read_urls
from config import Config


def unlike_all(driver: webdriver.Firefox) -> None:
    elements = driver.find_elements(By.CSS_SELECTOR, "[aria-label=Unlike]")
    if not len(elements):
        logging.warning(f"No unlike found for {driver.current_url}")
        history.write_empty(driver.current_url)
        return
    for element in elements:
        element.click()
    elements = driver.find_elements(By.CSS_SELECTOR, "[aria-label=Unlike]")
    if len(elements):
        logging.error(f"Rate limited: {driver.current_url}")
        time.sleep(3600)
        unlike_all(driver)
    history.write(driver.current_url)


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

    for url in urls:
        if url in done_urls:
            logging.info(f"Skipping as already processed: {url}")
            continue
        logging.info(f"Processing {url}")
        driver.get(url)
        if is_blank(driver):
            logging.error(f"Blank page: {url}")
            history.write_empty(url)
            continue
        time.sleep(5)
        unlike_all(driver)
        time.sleep(5)

    driver.quit()


if __name__ == '__main__':
    main()
