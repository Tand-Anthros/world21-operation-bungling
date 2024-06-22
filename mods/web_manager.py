import os, time
import __ac__ as tools

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


def start_driver():
    try:          
        path = f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles'
        for name in os.listdir(path):
            if '.default-release' in name: profile = path + '\\' + name
        profile
    except: raise Exception('firefox profile not exist')

    options = webdriver.FirefoxOptions()
    options.profile = profile

    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    return driver


driver = start_driver()
driver.get('https://vk.com/im?sel=266717581')

while not tools.sync({'exit': ''}).get('exit'):
    try:
        element = driver.find_element(By.CLASS_NAME, '_im_peer_history')
        print(element)

        out = []
        for elm in element.find_elements(By.CLASS_NAME, '_im_mess_stack'):
            content = elm.find_element(By.CLASS_NAME, '_im_log_body')
            author = elm.find_element(By.CLASS_NAME, 'im-mess-stack--lnk')
            out.append(content.get_attribute('outerHTML') + author.text)
            
        out = '<div>' + ''.join(out) + '</div>'
        tools.sync({'messages': out})

        answer = tools.sync({'answer': ''})['answer']
        if answer:
            input_box = driver.find_element(By.CLASS_NAME, 'im_editable')
            input_box.send_keys(answer)
            input_box.send_keys(Keys.RETURN)
            tools.sync({'answer': None})

    except Exception as e:
        driver.quit()
        raise

    time.sleep(1)
    
driver.quit()
