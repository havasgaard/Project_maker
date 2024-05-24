from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import os
import subprocess
import platform
import openai
from templates import project_templates

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize OpenAI API
openai.api_key = 'your-open-ai-key'  # Replace with your OpenAI API key


@app.route('/')
def index():
    return render_template('index.html', templates=project_templates.keys())


@app.route('/get_structure', methods=['POST'])
def get_structure():
    data = request.get_json()
    user_input = data.get('user_input')

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are an assistant that helps generate file structures for coding projects."},
            {"role": "user", "content": f"Generate a file structure for a {user_input}"}
        ]
    )

    file_structure = response.choices[0].message['content'].strip()
    return jsonify({"file_structure": file_structure})


def parse_manual_structure(structure):
    lines = structure.strip().split('\n')
    parsed_structure = []
    stack = []
    for line in lines:
        line = line.strip().replace('\r', '')  # Remove carriage returns
        indent_level = 0
        while line[indent_level] in [' ', '│', '├', '└']:
            indent_level += 1
        indent_level //= 4

        line = line.strip(' │├└─')
        while len(stack) > indent_level:
            stack.pop()

        current_path = os.path.join(*stack, line)
        stack.append(line)
        parsed_structure.append(current_path.replace("\\", "/"))

    return parsed_structure


@app.route('/create_files', methods=['POST'])
def create_files():
    project_name = request.form['project_name']
    destination = request.form['destination']
    framework = request.form['framework']
    install_dependencies = 'install_dependencies' in request.form
    superuser_username = request.form.get('superuser_username')
    superuser_email = request.form.get('superuser_email')
    superuser_password = request.form.get('superuser_password')
    file_structure = request.form['file_structure']

    project_path = os.path.join(destination, project_name)

    try:
        os.makedirs(project_path, exist_ok=True)

        # Generate the files based on file_structure
        parsed_structure = parse_manual_structure(file_structure)
        for file_path in parsed_structure:
            full_path = os.path.join(project_path, file_path)
            if file_path.endswith('/'):
                os.makedirs(full_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write('')

        venv_path = os.path.join(project_path, 'venv')

        if platform.system() == 'Windows':
            python_executable = os.path.join(venv_path, 'Scripts', 'python.exe')
            pip_executable = os.path.join(venv_path, 'Scripts', 'pip.exe')
        else:
            python_executable = os.path.join(venv_path, 'bin', 'python')
            pip_executable = os.path.join(venv_path, 'bin', 'pip')

        if framework == 'flask' and install_dependencies:
            subprocess.run(['python', '-m', 'venv', venv_path])
            subprocess.run([pip_executable, 'install', 'flask'])

        if framework == 'django':
            subprocess.run(['python', '-m', 'venv', venv_path])
            subprocess.run([pip_executable, 'install', 'django'])
            subprocess.run([python_executable, '-m', 'django', 'startproject', 'myproject', project_path])
            app_path = os.path.join(project_path, 'myproject', 'myapp')
            os.makedirs(app_path, exist_ok=True)
            subprocess.run([python_executable, os.path.join(project_path, 'manage.py'), 'startapp', 'myapp'],
                           cwd=project_path)

            # Apply migrations
            subprocess.run([python_executable, os.path.join(project_path, 'manage.py'), 'migrate'], cwd=project_path)

            if superuser_username and superuser_email and superuser_password:
                # Create superuser
                create_superuser_script = f"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='{superuser_username}').exists():
    User.objects.create_superuser('{superuser_username}', '{superuser_email}', '{superuser_password}')
"""
                with open(os.path.join(project_path, 'create_superuser.py'), 'w') as f:
                    f.write(create_superuser_script)
                subprocess.run([python_executable, os.path.join(project_path, 'create_superuser.py')], cwd=project_path)
                os.remove(os.path.join(project_path, 'create_superuser.py'))

        flash('Project and files created successfully!', 'success')
    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
