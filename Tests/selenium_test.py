from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://0.0.0.0:5000/")

#assert "Python" in driver.title
print(driver.title)


driver.close()