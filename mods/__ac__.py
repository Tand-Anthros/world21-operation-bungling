import pickle, time, os, sys, inspect, json, random, platform
try: import psutil, pygetwindow, win32api, win32con, win32process, flask, flask_cors
except: 
    os.system('pip3 install psutil flask flask_cors selenium webdriver_manager pygetwindow')
    sys.exit()


if 'tools':
    def file(path, data = None):
        i = 0
        while True:
            try:
                if data == None:
                    if path.endswith('.pkl'): 
                        with open(path, 'rb') as file: return pickle.load(file)
                    elif path.endswith('.json'): 
                        with open(path, 'r') as file: return json.load(file)
                    else:
                        with open(path, 'r') as file: return file.read()

                if path.endswith('.pkl'):
                    with open(path, 'wb') as file: return pickle.dump(data, file)
                elif path.endswith('.json'): 
                    with open(path, 'w') as file: return json.dump(data, file, indent=4)
                else:
                    with open(path, 'r') as file: return file.write(data)
                
            except Exception as e: 
                if i > 120: raise
            time.sleep(0.016)
            i += 1


    def move(path, move = None):
            i = 0
            while os.path.exists(path):
                try:
                    if move: os.rename(path, move)
                    else: os.remove(path)
        
                except Exception as e:
                    if i > 120: raise
                time.sleep(0.016)
                i += 1


    def sync(value: dict, name: str = None): #всегда возвращает словарь, а так же не ломается при ошибке
        if not name: 
            name = inspect.getmodule(inspect.currentframe().f_back)
            name = name.__file__.split("\\")[-1:][0][:-3]

        if type(value).__name__ == 'dict':
            file(f'__pycache__/{name}.pkl', value)
            move(f'__pycache__/{name}.pkl', f'__pycache__/-{name}.pkl')
            variable = file(f'__pycache__/={name}.pkl')
            move(f'__pycache__/={name}.pkl')
            return variable
        else:
            raise AttributeError(f'\'{type(value).__name__}\' object is not supported')


    def convert(value):
        if value == '': return ''
        if '\n' not in value and value[0] in ['{', '[', '('] or value in ['True', 'False', 'None']:   
            try: return eval(value)
            except SyntaxError: input(f'SyntaxError...')
        else:
            try: return int(value)
            except ValueError: 
                try: return float(value)
                except ValueError: return value


    def close(name):
        if platform.system() == 'Windows': 
            windows = pygetwindow.getWindowsWithTitle(f'AC-Child-{name}')
            for window in windows:
                tid, pid = win32process.GetWindowThreadProcessId(window._hWnd)
                process = psutil.Process(pid)
                win32api.PostMessage(window._hWnd, win32con.WM_CLOSE, 0, 0)
                process.wait()
        else: # Тестовый код для Linux. Возможно это не будет работать.
            result = psutil.Popen(['wmctrl', '-l'], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if f'AC-Child-{name}' in line:
                    window_id = line.split()[0]
                    psutil.Popen(['wmctrl', '-ic', window_id])


    def start(*args, window = True, name = None):
        r'''result.terminate() for close the running process or rough method .kill()'''
        if not name: name = str(random.randint(100000, 999999))
        if window: psutil.Popen(["start", "cmd", "/c", f"title AC-Child-{name} &&", *args], shell = True)
        else: psutil.Popen(["cmd", "/k", *args], shell = True)

        return [close, [f'title AC-Child-{name}']]


if 'beta':
    import psutil, requests


    def get_proc(args):
        i = 0
        while True:
            time.sleep(0.016)
            all_processes = psutil.process_iter()
            for proc in all_processes:
                try:
                    if 'python' in proc.name():
                        skip = False
                        cmdline = proc.cmdline()
                        for arg in args:
                            if arg not in cmdline:
                                skip = True
                        if not skip: return proc
                except: pass
            i += 1
            if i >= 30: raise psutil.NoSuchProcess(args)


    def request_sync(key, value = None, url = 'http://localhost:5000/'):
        if not value: response = requests.get(url + key)
        else: response = requests.post(url + key, data={'value': value})
        return convert(response.text)