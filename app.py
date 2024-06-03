from flask import Flask, render_template_string, request, redirect, url_for, flash
import os, json
from templates import index_html, edit_html
from json_utils import get_json_from_path, set_json_at_path, load_json_file, save_json_file

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/load', methods=['POST'])
def load_file():
    file_path = request.form['file_path']
    if not os.path.isfile(file_path):
        flash('File does not exist')
        return redirect(url_for('index'))
    
    return redirect(url_for('edit_file', filename=file_path, path=''))

@app.route('/edit/<path:filename>', methods=['GET', 'POST'])
def edit_file(filename):
    path = request.args.get('path', '')
    if request.method == 'POST':
        json_data = {}
        key_count = int(request.form['key_count'])
        for i in range(key_count):
            key = request.form.get(f'key_{i}')
            value = request.form.get(f'value_{i}')
            if key is not None:
                try:
                    value = json.loads(value)
                except (ValueError, TypeError):
                    pass  # Keep it as string if it is not valid JSON
                json_data[key] = value

        new_key = request.form.get('new_key')
        new_value = request.form.get('new_value')
        if new_key and new_value:
            try:
                new_value = json.loads(new_value)
            except ValueError:
                pass  # Keep it as string if it is not valid JSON
            json_data[new_key] = new_value

        deleted_keys = request.form.getlist('deleted_keys')
        for key in deleted_keys:
            if key in json_data:
                del json_data[key]

        full_data = load_json_file(filename)
        set_json_at_path(full_data, path, json_data)

        if save_json_file(filename, full_data):
            flash('File successfully saved')
        else:
            flash('Failed to save the file')

    if os.path.exists(filename):
        full_data = load_json_file(filename)
        json_data = get_json_from_path(full_data, path)
    else:
        json_data = {}
    
    return render_template_string(edit_html, json_data=json_data, filename=filename, path=path)

if __name__ == '__main__':
    app.run(debug=True)
