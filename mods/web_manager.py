import os, time
import __ac__ as tools
import vk_api


def start_driver():
    from selenium import webdriver
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from webdriver_manager.firefox import GeckoDriverManager

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


print('firefox is starting...')
driver = start_driver()
vk_api.init(driver)
tools.sync({'ident': vk_api.dialogs()[0]})

try:
    while True:
        ident = tools.sync({'ident': ''})['ident']
        if ident: vk_api.check(driver, ident)

        time.sleep(1)
except Exception as e:
    driver.quit()
    raise
