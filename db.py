import subprocess
import time
from multiprocessing import Manager, Process


def child_script(shared_dict):
    # Имитация работы скрипта
    time.sleep(5)
    # Изменение ключа в словаре
    shared_dict['key'] = True

def run_script():
    with Manager() as manager:
        # Создаем словарь, который будет доступен из обоих процессов
        shared_dict = manager.dict()
        # Инициализируем ключ словаря
        shared_dict['key'] = False

        # Создаем и запускаем дочерний процесс
        p = Process(target=child_script, args=(shared_dict,))
        p.start()

        # Главный скрипт ожидает изменения в словаре
        while not shared_dict['key']:
            #print('Ожидание изменения ключа...')
            time.sleep(1)

        # Ключ изменен, завершаем дочерний процесс
        p.terminate()
        p.join()  # Дожидаемся полного завершения процесса
        #print('Дочерний процесс завершен.')

if __name__ == '__main__':
    run_script()






# import subprocess

# # Запуск файла db.py как отдельного процесса без блокировки основного скрипта
# process = subprocess.Popen(['py', 'db.py'])

# # Запуск файла db.py как отдельного процесса
# process = subprocess.Popen(['py', 'db.py'])

# # ... ваш код ...

# # Мягкое завершение процесса
# process.terminate()

# # Если процесс все еще запущен, принудительно завершаем его
# if process.poll() is None:
#     process.kill()

# from subprocess import Popen, check_call

# # Запуск файла db.py как отдельного процесса
# process = Popen('py db.py', shell=True)

# # ... ваш код ...

# # Принудительное завершение процесса и всех дочерних процессов
# check_call(["TASKKILL", "/F", "/PID", str(process.pid), "/T"])

