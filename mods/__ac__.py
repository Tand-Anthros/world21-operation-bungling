import pickle, time


def sync(value: dict):
    if type(value).__name__ == 'dict':
        with open(f'__pycache__/{__file__}.pkl', 'wb') as file:
            pickle.dump(value, file)
        while True:
            time.sleep(0.016)
            try:
                with open(f'__pycache__/~{__file__}.pkl', 'rb') as file:
                    variable = pickle.load(file)
                return variable
            except FileNotFoundError: pass
    else:
        raise AttributeError(f'\'{type(value).__name__}\' object is not supported')



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
