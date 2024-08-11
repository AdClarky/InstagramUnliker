import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from urlReader import read_urls
from config import Config


def unlike_all(driver: webdriver.Firefox):
    elements = driver.find_elements(By.CSS_SELECTOR, "[aria-label=Unlike]")
    for element in elements:
        element.click()


def main():
    config = Config("config.json")

    urls = read_urls(config.liked_posts_path)

    options = webdriver.FirefoxOptions()
    options.add_argument("-profile")
    options.add_argument(config.firefox_profile_path)
    driver = webdriver.Firefox(options=options)

    for url in urls:
        driver.get(url)
        time.sleep(10)
        unlike_all(driver)
        time.sleep(10)


if __name__ == '__main__':
    main()
