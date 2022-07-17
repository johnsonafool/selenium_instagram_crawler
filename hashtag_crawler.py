#!/usr/bin/env python
# coding: utf-8

# In[67]:

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# In[68]:


s = Service("/opt/homebrew/bin/chromedriver")
driver = webdriver.Chrome(service=s)

driver.get("http://www.instagram.com")

username = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']"))
)
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']"))
)

username.clear()
username.send_keys("USER")
password.clear()
password.send_keys("PASSWORD")

button = (
    WebDriverWait(driver, 2)
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    .click()
)

# In[69]:


time.sleep(5)
alert = (
    WebDriverWait(driver, 15)
    .until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))
    )
    .click()
)

# In[106]:


searchbox = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))
)
searchbox.clear()

keyword = "#咖啡廳"  # your keyword
searchbox.send_keys(keyword)

time.sleep(5)
link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@href, '/" + keyword[1:] + "/')]")
    )
)
link.click()  # this didnt trigger the click envet on input, i am still fixing the issue, will return an error

# searchbox.send_keys(Keys.ENTER)

# In[107]:


n_scrolls = 1
for j in range(0, n_scrolls):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

# In[121]:


anchors = driver.find_elements(By.TAG_NAME, "a")
anchors = [a.get_attribute("href") for a in anchors]

anchors = [a for a in anchors if a.startswith("https://www.instagram.com/p/")]
anchors[:5]

# anchors = [a for a in anchors if a.startswith("https://www.instagram.com/explore/locations/")]#\
# print('Found ' + str(len(anchors)) + ' links to images')

# In[126]:


locations = []

for anchor in anchors:
    try:
        driver.get(anchor)
        time.sleep(5)
        location = driver.find_elements(By.TAG_NAME, "a")
        location = [a.get_attribute("href") for a in location]
        location = [
            l
            for l in location
            if l.startswith("https://www.instagram.com/explore/locations/")
        ]

        if str(location) == "https://www.instagram.com/explore/locations/":
            continue

        if len(location) == 0:
            str = "no location for this post"
            locations.append(str)
        locations.append(location)
    except:
        pass

locations[:5]
