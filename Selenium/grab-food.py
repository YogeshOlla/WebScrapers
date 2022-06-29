# Importing required libraries
from xml.dom.minidom import Element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep


# URL of a restaurant

website_url = 'https://food.grab.com/sg/en/'

# Intitilizing chromedriver
driver = webdriver.Chrome()

# Setting timeout to 30 seconds
driver.set_page_load_timeout(30)

# Opening the page
driver.get(website_url)

# Cleaning all cookies
driver.delete_all_cookies()

sleep(10)  

# Submiting location to be searched
search_loc = '66 Bayshore Rd'
search_box = driver.find_element(By.XPATH,'.//*[@id="location-input"]')
search_box.send_keys(search_loc)

search_button = driver.find_element(By.XPATH,'.//*[@id="page-content"]/div[2]/div/button')
search_button.click()

sleep(10)  

load_more = driver.find_element(By.XPATH,'.//*[@id="page-content"]/div[4]/div/div/div[4]/div/button')
load_more.click()