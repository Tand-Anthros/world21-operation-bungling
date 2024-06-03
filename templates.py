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

edit_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit JSON</title>
    <script>
        function addKey() {
            var newKey = document.createElement('div');
            var keyCount = document.getElementById('key_count').value;
            newKey.innerHTML = '<div id="key_' + keyCount + '"><input type="text" name="key_' + keyCount + '" placeholder="New Key"><input type="text" name="value_' + keyCount + '" placeholder="New Value"><button type="button" onclick="deleteKey(' + keyCount + ')">Delete</button></div>';
            document.getElementById('keys').appendChild(newKey);
            document.getElementById('key_count').value = parseInt(keyCount) + 1;
        }
        function deleteKey(keyIndex) {
            var keyElement = document.getElementById('key_' + keyIndex);
            if (keyElement) {
                var keyInput = keyElement.querySelector('input[name^="key_"]');
                if (keyInput) {
                    var hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = 'deleted_keys';
                    hiddenInput.value = keyInput.value;
                    document.getElementById('keys').appendChild(hiddenInput);
                }
                keyElement.remove();
            }
        }
    </script>
</head>
<body>
    <h1>Edit JSON file: {{ filename }}</h1>
    <form action="{{ url_for('edit_file', filename=filename, path=path) }}" method="post">
        <div id="keys">
            {% for key, value in json_data.items() %}
                <div id="key_{{ loop.index0 }}">
                    <input type="text" name="key_{{ loop.index0 }}" value="{{ key }}">
                    {% if value is mapping or value is iterable and value is not string %}
                        <button type="button" onclick="window.location.href='{{ url_for('edit_file', filename=filename, path=path + '/' + key) }}'">Edit</button>
                    {% else %}
                        <input type="text" name="value_{{ loop.index0 }}" value="{{ value }}">
                    {% endif %}
                    <button type="button" onclick="deleteKey({{ loop.index0 }})">Delete</button>
                </div>
            {% endfor %}
        </div>
        <input type="hidden" id="key_count" name="key_count" value="{{ json_data|length }}">
        <button type="button" onclick="addKey()">Add Key</button>
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
