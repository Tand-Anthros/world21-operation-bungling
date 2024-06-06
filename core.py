import platform, json, os, sys, time, pickle, os, psutil


if 'tools':
    def file(path, data = None):
        if data == None:
            try: 
                with open(path, 'r') as file: return json.load(file)
            except FileNotFoundError: return {}

        with open(path, 'w') as file:
            json.dump(data, file, indent=4)

    def interface(*args):
        if platform.system() == 'Windows': os.system('cls')
        else: os.system('clear')

        for line in args[:-1]: print(line)
        return input(f'\n{args[-1]}')

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

    def start(*args, window = True):
        r'''result.terminate() for close the running process or rough method .kill()'''
        if window: psutil.Popen(["start", "cmd", "/c", f"title Child && python", *args], shell = True)
        else: psutil.Popen(["cmd", "/k", "python", *args], shell = True)

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


if 'tasks':
    def host(): 
        # Если появятся проблемы, возможно стоит ренеймить файлы после записи, что бы во время записи, не было ошибок у другого процесса
        root = file(sys.argv[1])

        while 'host':
            time.sleep(0.016)
            pkl = None
            while not pkl:
                for filename in os.listdir('__pycache__'):
                    if filename.endswith('.pkl') and not filename.startswith('~'):
                        pkl = filename
            
            try:
                with open(f'__pycache__/{pkl}', 'rb') as file:
                    data = pickle.load(file)
            except:
                raise # проверить какая ошибка должна быть, если файл не бинарный

            # работа с data...

            with open(f'__pycache__/{pkl}', 'wb') as file:
                pickle.dump(data, file)

            file('__pycache__/__root__.json', root)
            file(sys.argv[1], root)

    def console():
        while 'console':
            try:
                root = file(sys.argv[1])
                acts = {'$input': input}

                keys = ', '.join(root.keys()) + '\n' + ', '.join(acts.keys())
                key = interface('/root:', keys, '', '"key?" > ')
                if key == '': continue
                
                if type(root.get(key)).__name__ == 'str': content = f'"{root.get(key)}"'
                else: content = root.get(key)
                value = interface(f'/root:', keys, '', f'"{key}": {content}', '', f'"{key}":? > ')
                value = convert(value)

                if value == '': continue
                elif value == None:
                    answer = interface(f'delete "{key}"?', '', f'(+, y, yes) > ')
                    if answer.lower() in ['+', 'y', 'yes', 'д', 'да']: 
                        try: root.pop(key)
                        except KeyError: pass
                    else: root[key] = value
                else: root[key] = value
                
                file(sys.argv[1], root)

            except KeyboardInterrupt: 
                print('bye!')
                sys.exit()


if 'launch':
    if len(sys.argv) == 2:
        proc = start('D:\\Code\\world21-operation-bungling\\core.py', *sys.argv[1:], '__console__')
        print('5 секунд до закрытия...')
        time.sleep(5)
        proc.terminate()
    elif len(sys.argv) == 3 and sys.argv[2] == '__console__':
        console()
    else:
        print('write a project *.json file')
