# Project Maker

Project Maker is a Flask-based web application that helps users create and manage projects. Users can input project details and the application will handle project creation, management, and provide a user-friendly interface to interact with the projects.

## Features

- Create new projects with specified details
- Manage and view existing projects
- User-friendly interface with a clean and modern design

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/havasgaard/project_maker.git
    cd project_maker
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```bash
    python run.py
    ```

2. Open your browser and go to `http://127.0.0.1:5000`.

3. Use the interface to create and manage projects.

## Project Structure

- `app/` - Contains the application code
  - `__init__.py` - Initializes the Flask application and registers blueprints
  - `views.py` - Defines the routes and view functions
  - `templates/` - HTML templates for rendering views
  - `static/` - Static files such as CSS and JavaScript

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
