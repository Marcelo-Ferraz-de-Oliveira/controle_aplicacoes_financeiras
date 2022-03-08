from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def get_headless_selenium_webdriver():
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  prefs = {"download.default_directory" : "."}
  options.add_experimental_option('prefs',prefs)
  return webdriver.Chrome('chromedriver',options=options)