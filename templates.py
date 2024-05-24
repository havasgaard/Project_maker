# templates.py

project_templates = {
    "flask_app": {
        "files": [
            "app.py",
            "requirements.txt",
            "run.py",
            "config.py",
            "app/__init__.py",
            "app/routes.py",
            "app/templates/index.html",
            "app/static/css/styles.css",
            "app/static/js/scripts.js"
        ],
        "content": {
            "app.py": '''from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
''',
            "requirements.txt": "Flask\n",
            "run.py": '''from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
''',
            "config.py": '''import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
''',
            "app/__init__.py": '''from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
''',
            "app/routes.py": '''from flask import Blueprint, render_template

bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')
''',
            "app/templates/index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <div class="container">
        <h1>Welcome to Your New Flask App!</h1>
        <p>Start editing <code>app/routes.py</code> to make changes.</p>
    </div>
    <script src="{{ url_for('static', filename='js/scripts.js') }}"></script>
</body>
</html>
''',
            "app/static/css/styles.css": '''body {
    font-family: Arial, sans-serif;
    background-color: #f8f9fa;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}

.container {
    text-align: center;
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
''',
            "app/static/js/scripts.js": '''document.addEventListener('DOMContentLoaded', (event) => {
    console.log('JavaScript is working!');
});
'''
        }
    }
}


project_templates.update({
    "django_app": {
        "files": [
            "manage.py",
            "requirements.txt",
            "myproject/__init__.py",
            "myproject/settings.py",
            "myproject/urls.py",
            "myproject/wsgi.py",
            "myapp/__init__.py",
            "myapp/admin.py",
            "myapp/apps.py",
            "myapp/models.py",
            "myapp/tests.py",
            "myapp/views.py",
            "myapp/templates/myapp/index.html",
            "myapp/static/myapp/css/styles.css",
            "myapp/static/myapp/js/scripts.js"
        ],
        "content": {
            "manage.py": '''#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
''',
            "requirements.txt": "Django\n",
            "myproject/__init__.py": "",
            "myproject/settings.py": '''import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'your-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
''',
            "myproject/urls.py": '''from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
]
''',
            "myproject/wsgi.py": '''import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = get_wsgi_application()
''',
            "myapp/__init__.py": "",
            "myapp/admin.py": '''from django.contrib import admin
from .models import MyModel

admin.site.register(MyModel)
''',
            "myapp/apps.py": '''from django.apps import AppConfig

class MyappConfig(AppConfig):
    name = 'myapp'
''',
            "myapp/models.py": '''from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
''',
            "myapp/tests.py": '''from django.test import TestCase

class MyModelTest(TestCase):

    def test_string_representation(self):
        entry = MyModel(name="My entry")
        self.assertEqual(str(entry), entry.name)
''',
            "myapp/views.py": '''from django.shortcuts import render

def index(request):
    return render(request, 'myapp/index.html', {'title': 'Home'})
''',
            "myapp/templates/myapp/index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'myapp/css/styles.css' %}">
</head>
<body>
    <div class="container">
        <h1>Welcome to Your New Django App!</h1>
        <p>Start editing <code>myapp/views.py</code> to make changes.</p>
    </div>
    <script src="{% static 'myapp/js/scripts.js' %}"></script>
</body>
</html>
''',
            "myapp/static/myapp/css/styles.css": '''body {
    font-family: Arial, sans-serif;
    background-color: #f8f9fa;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}

.container {
    text-align: center;
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
''',
            "myapp/static/myapp/js/scripts.js": '''document.addEventListener('DOMContentLoaded', (event) => {
    console.log('JavaScript is working!');
});
'''
        }
    }
})
