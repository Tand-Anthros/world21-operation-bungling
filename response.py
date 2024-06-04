import requests


url = 'http://localhost:5000/'

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

def root(key, value = None):
    if not value: response = requests.get(url + key)
    else: response = requests.post(url + key, data={'value': value})
    return convert(response.text)


print(root('ключ1'))
print(root('kajdawdaaw', '1245145'))
