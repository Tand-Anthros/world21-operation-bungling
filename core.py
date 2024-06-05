import platform, json, os, sys, time, pickle, os, multiprocessing
from mods.__ac__ import file as _file


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


if 'tasks':
    def host(): # Если появятся проблемы, возможно стоит ренеймить файлы после записи, что бы во время записи, не было ошибок у другого процесса
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
