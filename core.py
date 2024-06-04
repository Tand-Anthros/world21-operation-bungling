import platform, json, os, sys, multiprocessing, time


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
    from flask import Flask, render_template_string, request
    from multiprocessing import Process


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
