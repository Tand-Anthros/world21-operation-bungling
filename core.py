import os, platform, sys, time, traceback
from mods import __ac__ as tools


if 'tasks':
    def host(): 
        if not os.path.exists('__pycache__'): os.makedirs('__pycache__')
        for filename in os.listdir('__pycache__'):
            if filename.endswith('.pkl'): 
                tools.move(filename)
        
        tools.start('python', __file__, *sys.argv[1:], '__console__')
        tools.start('python', __file__, *sys.argv[1:], '__api__')
        root = tools.file(sys.argv[1])

        while 'host':
            pkl = None
            while not pkl:
                time.sleep(0.016)
                for filename in os.listdir('__pycache__'):
                    if filename.endswith('.pkl') and filename.startswith('-'):
                        pkl = filename
                        
            data = None
            while not data:
                data = tools.file(f'__pycache__/{pkl}')
            tools.move(f'__pycache__/{pkl}')

            out = {}
            if type(data).__name__ == 'dict':
                if data != {'':''}:
                    for key in data.keys():
                        if data[key] == '': out[key] = root.get(key)
                        elif data[key] == None: root.pop(key)
                        else: root[key] = data[key]
                else: out = root

            tools.file(f'__pycache__/~{pkl[1:]}', out)
            tools.move(f'__pycache__/~{pkl[1:]}', f'__pycache__/={pkl[1:]}')

            if root.get('exit'):
                tools.close('')
                sys.exit()

            tools.file(sys.argv[1], root)


    def console():
        def interface(*args):
            if platform.system() == 'Windows': os.system('cls')
            else: os.system('clear')

            for line in args[:-1]: print(line)
            return input(f'\n{args[-1]}')

        while 'console':
            try:
                root = tools.sync({'':''}, name = '__console__')

                keys = ', '.join(root.keys())
                key = interface('/root:', keys, '', '"key?" > ')
                if key == '': continue
                
                if type(root.get(key)).__name__ == 'str': content = f'"{root.get(key)}"'
                else: content = root.get(key)
                value = interface(f'/root:', keys, '', f'"{key}": {content}', '', f'"{key}":? > ')
                value = tools.convert(value)

                if value == '': continue
                elif value == None:
                    answer = interface(f'delete "{key}"?', '', f'(+, y, yes) > ')
                    if answer.lower() in ['+', 'y', 'yes', 'д', 'да']: 
                        try: tools.sync({key:value}, name = '__console__')
                        except KeyError: pass
                    else: continue
                else: tools.sync({key:value}, name = '__console__')

            except KeyboardInterrupt: 
                print('bye!')
                time.sleep(99999)
            except:
                traceback.print_exc()
                time.sleep(99999)
                

    def api():
        from flask import Flask, render_template_string, request
        from flask_cors import CORS

        app = Flask(__name__)
        CORS(app)

        @app.route('/<key>', methods = ['GET', 'POST'])
        def get_value(key):
            # <iframe src="http://localhost:3000" style="width:100%; height:500px; border:none;"></iframe> #для объектов
            if request.method == 'GET':
                return str(tools.sync({key: ''}, name = '__api__')[key]), 200
            elif request.method == 'POST':
                value = request.form.get('value')
                if value:
                    tools.sync({key:value}, name = '__api__')
                    return 'True'
                return 'False'
            
        @app.route('/<key>/<value>', methods = ['GET'])
        def set_value(key, value):
            if key == "''": key = ''
            if value == "''": value = ''
            value = tools.convert(value)

            if key == '' and value == '':
                return tools.sync({key:value}, name = '__api__')
            else:
                tools.sync({key:value}, name = '__api__')
                return 'True'

        if __name__ == '__main__':
            app.run(debug=True)


if 'launch':
    if len(sys.argv) == 2: host()
    elif len(sys.argv) == 3 and sys.argv[2] == '__console__': console()
    elif len(sys.argv) == 3 and sys.argv[2] == '__api__': api()
    else: print('write a project *.json file')
