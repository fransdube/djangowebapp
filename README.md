# Task Automation Dashboard

A Django-based web application for managing and automating tasks.

## Features

- **Dashboard**: View all tasks, filter by status or search by name.
- **Task Management**: Create, edit, delete, and schedule tasks.
- **Automation Logic**: Example implementations for email and scraping tasks.
- **User Authentication**: Secure registration, login, and logout.
- **REST API**: Manage tasks programmatically via API endpoints.
- **Execution Logs**: Track the history and status of task executions.

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Open your browser and navigate to `http://127.0.0.1:8000`.
2. Register for a new account or login.
3. Use the "Create New Task" button to add tasks.
4. Manage your tasks from the dashboard.

## API Documentation

The API is available at `/api/`.
- **List Tasks**: `GET /api/tasks/`
- **Create Task**: `POST /api/tasks/`
- **Execute Task**: `POST /api/tasks/<id>/run/`

## Deployment

For production:
1. Set `DEBUG = False` in `settings.py`.
2. Configure `ALLOWED_HOSTS`.
3. Use a production WSGI server like Gunicorn.
4. Serve static files using Nginx or WhiteNoise.
