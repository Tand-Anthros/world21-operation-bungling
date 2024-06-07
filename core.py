import platform, json, os, sys, time, pickle, os, psutil, traceback
from mods import __ac__ as tools


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
        # Можно добавить список с названиями ожидающих значения процессов и отсылать их при первом же появлении
        if not os.path.exists('__pycache__'): os.makedirs('__pycache__')
        proc = start('D:\\Code\\world21-operation-bungling\\core.py', *sys.argv[1:], '__console__') #, window = False)
        root = file(sys.argv[1])

        while 'host':
            pkl = None
            while not pkl:
                time.sleep(0.016)
                for filename in os.listdir('__pycache__'):
                    if filename.endswith('.pkl') and not filename.startswith('~'):
                        pkl = filename
                        
            data = None
            while not data:
                try:
                    with open(f'__pycache__/{pkl}', 'rb') as _file:
                        data = pickle.load(_file)
                except EOFError: time.sleep(0.016)
                except: raise # проверить какая ошибка должна быть, если файл не бинарный
            os.remove(f'__pycache__/{pkl}')

            out = {}
            if type(data).__name__ == 'dict':
                if data != {'':''}:
                    for key in data.keys():
                        if data[key] == '': out[key] = root.get(key)
                        elif data[key] == None: root.pop(key)
                        else: root[key] = data[key]
                else: out = root

            with open(f'__pycache__/~{pkl}', 'wb') as _file:
                pickle.dump(out, _file)

            if root.get('exit'):
                proc.terminate()
                sys.exit()

            file(sys.argv[1], root)


    def console():
        while 'console':
            try:
                root = tools.sync({'':''})

                keys = ', '.join(root.keys())
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
                        try: tools.sync({key:value})
                        except KeyError: pass
                    else: continue
                else: tools.sync({key:value})

            except KeyboardInterrupt: 
                print('bye!')
                time.sleep(99999)
                #sys.exit()
            except:
                traceback.print_exc()
                time.sleep(99999)
                

    def api():
        from flask import Flask, render_template_string, request

        app = Flask(__name__)


        index_html = r'''
        <form method="post">
            {% for key, value in dictionary.items() %}
                <label for="{{ key }}">{{ key }}</label>
                <input type="text" id="{{ key }}" name="{{ key }}" value="{{ value }}"><br>
            {% endfor %}<br>
            
            <input type="text" id="new_key" name="new_key" placeholder="Новый ключ">
            <input type="text" id="new_value" name="new_value" placeholder="Новое значение"><br>
            <button type="submit">Обновить</button>
        </form>
        '''


        dictionary = {"ключ1": "знaчeниe1", "ключ2": "знaчeниe2"}

        @app.route('/', methods=['GET', 'POST'])
        def home():
            if request.method == 'POST':
                for key in dictionary.keys():
                    dictionary[key] = request.form[key]
                
                new_key = request.form['new_key']
                new_value = request.form['new_value']
                if new_key and new_value:
                    dictionary[new_key] = new_value
            
            return render_template_string(index_html, dictionary=dictionary)

        @app.route('/<key>', methods=['GET', 'POST'])
        def get_value(key):
            if request.method == 'GET':
                return dictionary.get(key, 'Nul'), 200
            elif request.method == 'POST':
                new_value = request.form.get('value')
                if new_value:
                    dictionary[key] = new_value
                    return "True"
                return "False"


        if __name__ == '__main__':
            app.run(debug=True)


if 'launch':
    if len(sys.argv) == 2: host()
    elif len(sys.argv) == 3 and sys.argv[2] == '__console__': console()
    elif len(sys.argv) == 3 and sys.argv[2] == '__api__': api()
    else: print('write a project *.json file')
