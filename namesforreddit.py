from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from anticaptchaofficial.recaptchav2proxyless import *
import random
import time
import string
import secrets
import os

def install_extension(options):
    # Add this function to load the extension
    extension_path = os.path.join(os.path.dirname(__file__), '2.0.1_0.crx')
    options.add_extension(extension_path)

def nameGenerator(driver, password):
    # NAME GENERATION
    driver.get('https://en.wikipedia.org/wiki/Special:Random')
    temp = driver.find_element(By.CLASS_NAME, "firstHeading").text
    wikiFinding = temp
    for char in string.punctuation:
        temp = temp.replace(char, '')  # REMOVES ALL PUNCTUATION
    for char in string.digits:
        temp = temp.replace(char, '')  # REMOVES SPACES
    temp = "".join(filter(lambda char: char in string.printable, temp))  # REMOVES NON ASCII CHARACTERS
    name = ''.join(temp.split())
    name = name[:random.randint(5, 7)]  # KEEPS 5 TO 7 LETTERS OF THE ORIGINAL STRING

    randomNumber = random.randint(10000, 99999)

    dirname = os.path.dirname(__file__)
    text_file_path = os.path.join(dirname, 'namesforreddit.txt')
    with open(text_file_path, "a") as text_file:
        text_file.write(f"{name}{randomNumber}|{password}")
        text_file.write("\n")
    finalName = name + str(randomNumber)
    time.sleep(1)
    return finalName, wikiFinding
    # NAME GENERATION FINISHED

def generateAccount(driver):

    # GENERATE PASSWORD
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(16))
    # PASSWORD GENERATION FINISHED

    #NAME GENERATION
    finalName, wikiFinding = nameGenerator(driver, password)
    #NAME GENERATION FINISHED

    # REDDIT ACCOUNT CREATION
    driver.get('https://www.reddit.com/register/')
    driver.find_element(By.ID, 'regEmail').send_keys('email@email.com')
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(),'Continue')]").click()
    time.sleep(3)
    driver.find_element(By.ID, 'regUsername').send_keys(finalName)
    driver.find_element(By.ID, 'regPassword').send_keys(password)
    print("Account generation complete!")
    #print(f"Username: {finalName} | Password: {password}")
    #print(f"Origin of username is {wikiFinding}")
    print("> Captcha is now to be solved! <")
    driver.switch_to.window(driver.current_window_handle)


def main():
    # USES CHROMEDRIVERMANAGER TO AUTO UPDATE CHROMEDRIVER
    options = Options()
    options.add_argument("--lang=en")
    options.add_experimental_option("detach", True)

    # Load the extension before the account generation process
    install_extension(options)

    s = Service(ChromeDriverManager().install())

    times = int(input("How many accounts do you want to generate?: "))
    for i in range(times):
        try:
            time.sleep(5)
            driver = webdriver.Chrome(service=s, options=options)
            generateAccount(driver)
            time.sleep(3)
            captchaSolver(driver)
            time.sleep(3)
            driver.quit()
            print(f'Created account {i} successfully! ')
        except Exception:
            print(f'Got an exception trying to create account {i}')
            continue
    print('All done, exiting program...')

if __name__ == '__main__':
    main()
