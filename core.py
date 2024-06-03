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


root = file(sys.argv[1])

while True:
    key = interface(root, '"key?" > ')
    value = interface(root, f'"{key}":? > ')

    if value == '' and interface(root, f'del"{key}"? > ') in ['+', 'y', 'yes', 'д', 'да']: root.pop(key)
    else: root[key] = value

    file(sys.argv[1], root)