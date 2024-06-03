import json

def get_json_from_path(json_data, path):
    keys = path.split('/')
    for key in keys:
        if key:
            json_data = json_data.get(key, {})
    return json_data

def set_json_at_path(json_data, path, new_data):
    keys = path.split('/')
    for key in keys[:-1]:
        json_data = json_data.setdefault(key, {})
    json_data[keys[-1]] = new_data

def load_json_file(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file)

def save_json_file(filename, data):
    try:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return True
    except ValueError as e:
        print(f'Invalid JSON: {e}')
        return False
