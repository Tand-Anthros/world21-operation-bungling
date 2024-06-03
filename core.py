import platform, json, os, sys, time


def file(path, data = None):
    if data == None:
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

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
        except SyntaxError: return None     
    else:
        try: return int(value)
        except ValueError: 
            try: return float(value)
            except ValueError: return None


def delete(root, key):
    answer = interface(f'delete "{key}"?', '', f'(+, y, yes) > ')
    if answer.lower() in ['+', 'y', 'yes', 'д', 'да']: 
        root.pop(key)
    return root

def update(root, key, value):
    root[key] = value
    return root


root = file(sys.argv[1])
# ctxs = {}
# objs = {}
acts = {'$delete': delete, '$update': update}

while True:
    try:
        key = interface(
            '/root:', ', '.join(root.keys()), '',
            # '/#ctx\'s:', ', '.join(ctxs.keys()), '',
            # '/@obj\'s:', ', '.join(objs.keys()), '',
            '/$act\'s:', ', '.join(acts.keys()), '',
            '"key?" > ')
        
        value = interface(f'/root:', ', '.join(root.keys()), '', f'"{key}": {root.get(key)}', f'"{key}":? > ')
        value = convert(value)

        if key in acts.keys() and type(value).__name__ == 'tuple': root = acts[key](root, *value)
        
        file(sys.argv[1], root)

    except KeyboardInterrupt: 
        print('bye!')
        sys.exit()