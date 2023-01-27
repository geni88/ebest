
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

if __name__ == "__main__":
    driver = webdriver.Firefox(executable_path = 'D:\OWNER\Desktop\mywork/gekidriver')
    driver.wait = WebDriverWait(driver, 2)

    driver.get("http://google.com")
    