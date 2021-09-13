# JOB DESCRIPTION:
# So i join a few different subredits
# and put the sorting to new , then in my
# home page i let the sorting to new and
# everyone who posts in one of the subredits
# shows to me as the first person in feed ,
# i dm that person and send him a dm with a copy pasted message
# C:\Windows\System32

from selenium import webdriver
import time
import schedule
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=r'C:\Windows\System32\geckodriver.exe')
driver.maximize_window()

with open("settings.config") as f:
    settings = str(f.read())
    print(settings)
    settingsarr = settings.split("\n")
    username, password, message = (
        x.split(":")[1].strip() for x in settingsarr)

# login sequence
driver.get("http://www.reddit.com/login")
time.sleep(5)
usernamefield = driver.find_element_by_id("loginUsername")
pwfield = driver.find_element_by_id("loginPassword")
usernamefield.send_keys(username)
pwfield.send_keys(password)

submit_button = driver.find_element_by_class_name("AnimatedForm__submitButton")

hover = ActionChains(driver).move_to_element(submit_button)
hover.perform()
submit_button.click()
time.sleep(5)
dmed = []


def dm(username):
    p = driver.current_window_handle
    tabs = driver.window_handles
    for tab in tabs:
        if tab != p:
            driver.switch_to.window(tab)
            time.sleep(1)
            break
    buttons = driver.find_elements_by_class_name("_2q1wcTx60QKM_bQ1Maev7b")
    for button in buttons:
        if button.text == "Chat":
            try:
                button.click()
            except NoSuchElementException:
                pass
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, '_24sbNUBZcOO5r5rr66_bs4'))
        WebDriverWait(driver, 20).until(element_present)
        messageBox = driver.find_element_by_class_name("_24sbNUBZcOO5r5rr66_bs4")
        messageBox.send_keys(message)
        messageBox.send_keys(Keys.RETURN)
        time.sleep(5)
        blocker = driver.find_element_by_class_name('bwxXoigjZ4E9ofWIggxmp')
        blocker.click()
    except TimeoutException:
        print("Took too long to load message box")
    time.sleep(3)
    driver.close()
    driver.switch_to.window(p)


def arrangePage():
    global dmed
    p = driver.current_window_handle
    tabs = driver.window_handles
    for tab in tabs:
        if tab != p:
            driver.switch_to.window(tab)
            driver.close()
    # sorting by new and username stuff
    driver.get("http://www.reddit.com/new/")
    dmUsernames = driver.find_elements_by_class_name("_2tbHP6ZydRpjI44J3syuqC")
    for username in dmUsernames:
        if username.text != "" and username.text not in dmed:
            print("dm-ing", username.text)
            driver.execute_script(
                f'window.open("https://www.reddit.com/user/{username.text[2:]}", "_blank");')
            time.sleep(5)
            dmed += [username.text]
            dm(username)


schedule.every(10).minutes.do(arrangePage)
arrangePage()

while True:
    schedule.run_pending()
