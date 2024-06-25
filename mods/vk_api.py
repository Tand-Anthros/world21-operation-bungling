import time
import __ac__ as tools
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = None
def init(_driver):
    r'''starting with this function!'''
    global driver
    driver = _driver
    driver.get('https://vk.com/im')


def dialogs():
    global driver
    scroll_content = driver.find_element(By.CLASS_NAME, "_im_page_dialogs")
    dialogs = scroll_content.find_elements(By.CLASS_NAME, "_im_dialog")

    msg_ids = []
    for dialog in dialogs:
        try: msg_ids.append(dialog.get_attribute("data-peer"))
        except: pass
    return msg_ids


def switch(driver, ident: Union[int, str]): # возможно стоит сделать прокрутку или открытие в случае если эллемента сейчас нет в списке
    if str(ident) not in driver.current_url:
        element = driver.find_element(By.CLASS_NAME, f"_im_dialog_{ident}")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        
        action = ActionChains(driver)
        action.move_to_element(element).click().perform()



def send_message(driver, ident, message):
    switch(driver, ident)

    input_box = driver.find_element(By.CLASS_NAME, 'im_editable')
    input_box.send_keys(message)
    input_box.send_keys(Keys.RETURN)


def get_history(driver, ident):
    switch(driver, ident)

    element = driver.find_element(By.CLASS_NAME, '_im_peer_history')
    print('get:', driver.current_url)

    out = []
    for elm in element.find_elements(By.CLASS_NAME, '_im_mess_stack'):
        comp = dict()
        # avatar = driver.find_element(By.CSS_SELECTOR, "div.nim-peer--photo a.im_grid img")
        # comp['avatar'] = avatar.get_attribute("src")

        # comp['ident'] = None
        comp['author'] = elm.find_element(By.CLASS_NAME, 'im-mess-stack--lnk')

        content = elm.find_element(By.CLASS_NAME, '_im_log_body')
        if len(content.find_elements(By.XPATH, './*')) > 0: 
            content = 'not supported'
        else: content = content.text
        comp['content'] = content

        out.append(comp)
        
    return out


def check(driver, ident):
    try:
        tools.actions([dialogs])

        try:
            result = ''
            out = get_history(driver, ident)
            for elm in out:
                result += '<p>' + elm['author'].text + '</p>'
                result += '<div>' + elm['content'] + '</div>'
            result = '<div>' + result + '</div>'
        except: pass

        tools.sync({'messages': result})

        answer = tools.sync({'answer': ''})['answer']
        if answer:
            send_message(driver, ident, answer)
            tools.sync({'answer': None})

    except Exception as e:
        driver.quit()
        raise