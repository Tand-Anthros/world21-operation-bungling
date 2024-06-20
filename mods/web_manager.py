# сделать api как словарь. а так же сделать там стандартный ключ со значениями которые будут выставленны по умолчанию при запуске

from flask import Flask, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")  # Разрешить запросы только с http://localhost:3000

@app.route('/get-element-html', methods=['GET'])
def get_element_html():
    # options = webdriver.FirefoxOptions()
    # options.profile = f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\syly4wu8.default-release'

    # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    # driver.get('https://vk.com/im?sel=221270089')

    # try:
    #     element = driver.find_element(By.CLASS_NAME, '_im_peer_history')
    #     element_html = element.get_attribute('outerHTML')
    # except Exception as e:
    #     driver.quit()
    #     return jsonify({'error': str(e)}), 500

    # driver.quit()
    with open('element.html', 'r', encoding='utf-8', errors='ignore') as file:
        element_html = file.read()
    return jsonify({'element_html': element_html})

if __name__ == '__main__':
    app.run(port=5000)




# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager
# import threading
# import time, os


# def open_browser():
#     options = webdriver.FirefoxOptions()
#     options.profile = f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\syly4wu8.default-release'
    
#     driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
#     driver.get('https://vk.com/im?sel=221270089')
    
#     element = driver.find_element(By.CLASS_NAME, '_im_peer_history')
    
#     with open('element.html', 'w', encoding='utf-8') as file:
#         file.write(element.get_attribute('outerHTML'))
    
#     # time.sleep(99999)
#     driver.quit()


# if __name__ == "__main__":
#     window_1 = threading.Thread(target=open_browser) #args=(, ))
#     window_1.start()
#     window_1.join()
