from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import yaml
import random
import time
import os
import sys
import threading
from discord_webhook import DiscordWebhook
import datetime
import traceback

conf_import = "./conf.yaml"
secrets_import = "./secrets.yaml"

with open(conf_import, "r") as conf_file:
  config = yaml.safe_load(conf_file)

with open(secrets_import, "r") as secrets_file:
  secrets = yaml.safe_load(secrets_file)

myid = secrets['disord_userid']
webhook_url = secrets['webhook_url']

driver_wait = 10
refresh_time = config['refresh_time']

browser_launched = False

def create_driver():
  if config['headless_mode']:
    chromium_options = Options()
    chromium_options.add_argument("--headless")
    chromium_options.add_argument("--log-level=3")
    chromium_options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(config['driver_file_path'], options=chromium_options)
    return driver
  else:
    driver = webdriver.Chrome(config['driver_file_path'])
    driver.set_window_size(config['browser_width'],config['browser_height'])
    return driver


def send_notif(message,product,price_str):
  item_name = product['name']
  webhook = DiscordWebhook(url=webhook_url,
                  content='{} Stock is available for {} at {}\n{}'.format(myid, item_name, price_str, message))
  response = webhook.execute()

def run_bot_instance(driver_instance, product, product_index):

  #Stagger threads for multiple instances
  time.sleep(refresh_time + (random.random()*10))

  # if config['product_data'][product_index]['purchased']:
  #   return True

  #Create new Chromium driver instance
  driver = driver_instance()

  #Destructure product
  item_name = product['name']
  item_qty = 1
  base_url = 'https://www.amazon.co.uk/dp/'
  item_asin = product['asin']
  item_url = base_url + item_asin

  driver.get(item_url)
  accepted_cookies = False

  try:
    WebDriverWait(driver, driver_wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sp-cc-accept"]'))).click()
    accepted_cookies = True
  except:
    pass

  stock = False
  count = False
  # store_collection = False

  while not stock:
  
    checkout_page = False

    if driver.current_url != item_url:
      driver.get(item_url)

    if accepted_cookies == False:
      try:
        WebDriverWait(driver, driver_wait).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept All Cookies")]'))).click()
      except:
        pass

    try:
      add_to_basket = WebDriverWait(driver, driver_wait).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="buy-now-button"]')))
      
      price_str = driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]').text
      
      checkout_page = True
      if config['discord']:
        send_notif(item_url,product,price_str)

      time.sleep(1)

    except Exception as e:
      if config['debug'] == 1:
        traceback.print_exc()
      elif config['debug'] == 2:
        traceback.print_exc()
        pass
    
    if checkout_page:
        time.sleep(random.random()*refresh_time)
        driver.get(item_url)
    else:
        currentDT = datetime.datetime.now()
        print("Stock is not available for {} | ".format(item_name) + currentDT.strftime("%H:%M:%S"))
        time.sleep(random.random()*refresh_time)
        driver.execute_script("location.reload(true);")

    # pync.notify("Stock available for " + site_link, open=site_link)

if __name__ == "__main__":

  counter = 0
  no_of_items = len(config['product_data'])

  driver = create_driver

  for x in range(no_of_items):
      t = threading.Thread(target=run_bot_instance, args=[driver, config['product_data'][x], x])
      t.start()

