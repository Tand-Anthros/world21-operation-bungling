from flask import Flask, render_template_string, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# HTML шаблон для главной страницы
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>JSON Editor</title>
</head>
<body>
    <h1>Enter the path to a JSON file</h1>
    <form action="{{ url_for('load_file') }}" method="post">
        <input type="text" name="file_path" placeholder="Enter file path">
        <input type="submit" value="Load">
    </form>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
</body>
</html>
"""

# HTML шаблон для страницы редактирования
edit_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta.charset="UTF-8">
    <title>Edit JSON</title>
</head>
<body>
    <h1>Edit JSON file: {{ filename }}</h1>
    <form action="{{ url_for('edit_file', filename=filename) }}" method="post">
        <textarea name="json_data" rows="20" cols="100">{{ json_data }}</textarea>
        <br>
        <input type="submit" value="Save">
    </form>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/load', methods=['POST'])
def load_file():
    file_path = request.form['file_path']
    if not os.path.isfile(file_path):
        flash('File does not exist')
        return redirect(url_for('index'))
    
    return redirect(url_for('edit_file', filename=file_path))

@app.route('/edit/<path:filename>', methods=['GET', 'POST'])
def edit_file(filename):
    if request.method == 'POST':
        json_data = request.form['json_data']
        try:
            parsed_json = json.loads(json_data)
            with open(filename, 'w') as json_file:
                json.dump(parsed_json, json_file, indent=4)
            flash('File successfully saved')
        except ValueError as e:
            flash(f'Invalid JSON: {e}')
    
    if os.path.exists(filename):
        with open(filename, 'r') as json_file:
            json_data = json.load(json_file)
    else:
        json_data = {}
    
    return render_template_string(edit_html, json_data=json.dumps(json_data, indent=4), filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
