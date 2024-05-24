from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import threading
import time, os

# Укажите путь к вашему пользовательскому профилю Firefox
profile_path = f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\syly4wu8.default-release'

def open_browser(url, search_query=None):
    # Настройка параметров Firefox с использованием пользовательского профиля
    options = webdriver.FirefoxOptions()
    options.profile = profile_path
    
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    driver.get(url)
    
    if search_query:
        # Найдите элемент поиска Google и выполните запрос
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
    
    time.sleep(99999)
    driver.quit()

if __name__ == "__main__":
    # Открытие первого окна браузера и выполнение поискового запроса
    thread1 = threading.Thread(target=open_browser, args=('https://furbooru.com', 'oc:katia managan'))
    
    # Открытие второго окна браузера
    # thread2 = threading.Thread(target=open_browser, args=('https://vk.com',))

    thread1.start()
    # thread2.start()

    thread1.join()
    # thread2.join()









# import asyncio, os, json, time, shutil, sqlite3
# from pyppeteer import launch


# chrome_guest_profile_folder = f'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Guest Profile'
# destination_folder = f'saved_chrome_data'


# async def main():
#     browser = await launch(headless=False, executablePath='C:\\Program Files\\Mozilla Firefox\\firefox.exe')
#     page = await browser.newPage()

#     await page.goto('https://google.com')
#     await page.waitFor(99999)

#     await browser.close()


# asyncio.get_event_loop().run_until_complete(main())
