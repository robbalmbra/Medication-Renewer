# Renew medication on cron or manual call - V1.01
# Logs in and renews medication on the tpp-uk system

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def load_webpage(driver,url):
  # Load and wait for page
  current_url = driver.current_url
  driver.get(url)
  WebDriverWait(driver, 15).until(EC.url_changes(current_url))

def run(username,password):

  # Open up tpp for renewal
  driver = webdriver.PhantomJS()
  driver.set_window_size(1120, 550)

  # Load and wait webpage
  load_webpage(driver,"https://systmonline.tpp-uk.com/2/Login");

  # Fill out form
  current_url = driver.current_url
  driver.find_element_by_name('Username').send_keys(username)
  driver.find_element_by_name('Password').send_keys(password)
  driver.find_element_by_id('button').click()

  # Wait for login to complete
  WebDriverWait(driver, 15).until(EC.url_changes(current_url))

  # Check for username/password error
  try:
    error_msg = driver.find_element_by_id("errorText")
    print "Error - " + error_msg.get_attribute('innerHTML')
    sys.exit(1);
  except:
    pass

  # Load renewal webpage
  try:
    current_url = driver.current_url
    medication_block = driver.find_elements_by_id("plaintable")[1];
    medication_form = medication_block.find_elements_by_xpath(".//form")[0];
    medication_form.submit();
  except:
    sys.exit(1);

  # Wait for medication repeat to load
  WebDriverWait(driver, 15).until(EC.url_changes(current_url))
  current_url = driver.current_url

  # Repeat
  repeat_button = driver.find_elements_by_name("MedRequestType")[0];
  repeat_button_enabled = repeat_button.is_enabled();

  # Check for any alert messages regarding medication
  if repeat_button_enabled == False:
      # Return error message
      medication_form = driver.find_element_by_name("MedRequestForm");
      message_text = medication_form.find_element_by_xpath("//div[1]/table/tbody/tr[2]/td[2]");
      message_block = message_text.get_attribute('innerHTML').split("<br>")
      print "Warning - " + message_block[len(message_block)-1]
  else:
      # Renew meds
      repeat_button.click();
      medication_form = driver.find_element_by_name("MedRequestForm");
      medication_form.submit()

if len(sys.argv) < 3:
  print "USAGE: " + sys.argv[0] + " [USERNAME] [PASSWORD]"
  sys.exit(1);

username = sys.argv[1];
password = sys.argv[2];

# Run medication routine
run(username,password)
