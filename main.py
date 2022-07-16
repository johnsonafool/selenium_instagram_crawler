import time
import urllib.request

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

s = Service("/opt/homebrew/bin/chromedriver")
driver = webdriver.Chrome(service=s)

# PATH = r"/opt/homebrew/bin/chromedriver"
# driver = webdriver.Chrome(PATH)
driver.get("https://www.instagram.com/")

elements = driver.find_elements(By.TAG_NAME, "div")

with open("test.txt", "w") as f:
    e = str(elements)
    f.write(e)


for e in elements:
    print(e.text)


def main():
    # login
    time.sleep(12)
    username = driver.find_element_by_css_selector(
        "input[name='Phone number, username, or email']"
    )
    password = driver.find_element_by_css_selector("input[name='Password']")
    username.clear()
    password.clear()
    username.send_keys("xxxxxx")
    password.send_keys("123456")
    login = driver.find_element_by_css_selector("button[type='submit']").click()

    # save your login info?
    time.sleep(10)
    notnow = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
    # turn on notif
    time.sleep(10)
    notnow2 = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

    # searchbox
    time.sleep(5)
    searchbox = driver.find_element_by_css_selector("input[placeholder='Search']")
    searchbox.clear()
    searchbox.send_keys("host.py")
    time.sleep(5)
    searchbox.send_keys(Keys.ENTER)
    time.sleep(5)
    searchbox.send_keys(Keys.ENTER)


    # scroll
    scrolldown = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;"
    )
    match = False
    while match == False:
        last_count = scrolldown
        time.sleep(3)
        scrolldown = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;"
        )
        if last_count == scrolldown:
            match = True

    # posts
    posts = []
    links = driver.find_elements_by_tag_name("a")
    for link in links:
        post = link.get_attribute("href")
        if "/p/" in post:
            posts.append(post)

    print(posts)


    # get videos and images
    download_url = ""
    for post in posts:
        driver.get(post)
        shortcode = driver.current_url.split("/")[-2]
        time.sleep(7)
        if (
            driver.find_element_by_css_selector("img[style='object-fit: cover;']")
            is not None
        ):
            download_url = driver.find_element_by_css_selector(
                "img[style='object-fit: cover;']"
            ).get_attribute("src")
            urllib.request.urlretrieve(download_url, "{}.jpg".format(shortcode))
        else:
            download_url = driver.find_element_by_css_selector(
                "video[type='video/mp4']"
            ).get_attribute("src")
            urllib.request.urlretrieve(download_url, "{}.mp4".format(shortcode))
        time.sleep(5)


if __name__ == "__main__":
    main()
