# Task Management API

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.115.6-blue" alt="FastAPI Version">
  <img src="https://img.shields.io/badge/Python-3.12-informational" alt="Python Version">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0.36-orange" alt="SQLAlchemy Version">
  <img src="https://img.shields.io/badge/PostgreSQL-supported-green" alt="Database Support">
</p>

## Description

A simple RESTful API for managing tasks, built with Python, FastAPI, SQLAlchemy, and PostgreSQL.

The API provides CRUD operations for tasks, along with pagination, filtering, sorting, title search, validation, health checks, automated tests, and production deployment with Gunicorn and systemd.

## Features

- Create, retrieve, update, and delete tasks
- Search tasks by title
- Filter tasks by completion status
- Sort tasks by supported fields
- Pagination with `skip` and `limit`
- Request and response validation with Pydantic
- PostgreSQL integration with SQLAlchemy
- Health check endpoint
- Interactive Swagger UI and ReDoc documentation
- Automated API tests with pytest
- Production deployment with Gunicorn and systemd

## Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI 0.115.6
- **ORM:** SQLAlchemy 2.0.36
- **Database:** PostgreSQL
- **Database Driver:** psycopg2
- **Configuration:** pydantic-settings
- **Testing:** pytest, httpx
- **Production Server:** Gunicorn with Uvicorn workers
- **Process Management:** systemd

## Project Structure

```text
task-management-api/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── crud.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       └── tasks.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_tasks.py
```

## Requirements

- Python 3.12
- PostgreSQL
- Linux for production deployment

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Mahdiwav/task-management-api.git
cd task-management-api
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```dotenv
DATABASE_URL=postgresql+psycopg2://task_api_user:password@localhost:5432/task_management
```

Do not commit `.env` to Git.

## Database Setup

Create the PostgreSQL database and user before starting the application.

Example:

```sql
CREATE USER task_api_user WITH PASSWORD 'your_password';
CREATE DATABASE task_management OWNER task_api_user;
```

Make sure the `DATABASE_URL` in `.env` matches your PostgreSQL configuration.

The application creates the required database tables from the SQLAlchemy metadata when it starts.

## Running Locally

Start the development server with:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

Once the application is running:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

### Create a task

```http
POST /tasks
```

Request body:

```json
{
  "title": "Learn FastAPI",
  "description": "Complete the Task Management API project"
}
```

Response:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Complete the Task Management API project",
  "is_completed": false,
  "created_at": "2026-08-26T18:00:00+03:30"
}
```

### List tasks

```http
GET /tasks
```

Supported query parameters:

| Parameter | Description | Example |
|---|---|---|
| `skip` | Number of records to skip | `skip=0` |
| `limit` | Maximum number of records | `limit=20` |
| `is_completed` | Filter by completion status | `is_completed=true` |
| `search` | Search by title | `search=FastAPI` |
| `sort` | Sort field | `sort=created_at` |
| `order` | Sort direction | `order=desc` |

Example:

```text
GET /tasks?search=FastAPI&is_completed=false&sort=created_at&order=desc&skip=0&limit=20
```

### Get a task

```http
GET /tasks/{task_id}
```

Example:

```bash
curl http://127.0.0.1:8000/tasks/1
```

### Update a task

```http
PUT /tasks/{task_id}
```

Example:

```bash
curl --location 'http://127.0.0.1:8000/tasks/1' --header 'Content-Type: application/json' --data '{
  "title": "Learn FastAPI and SQLAlchemy",
  "is_completed": true
}'
```

### Delete a task

```http
DELETE /tasks/{task_id}
```

Example:

```bash
curl --location --request DELETE 'http://127.0.0.1:8000/tasks/1'
```

## Example Requests

### Create a task

```bash
curl --location 'http://127.0.0.1:8000/tasks' --header 'Content-Type: application/json' --data '{
  "title": "Learn FastAPI",
  "description": "Complete Task Management API project"
}'
```

### List tasks with filtering, search, sorting, and pagination

```bash
curl --location 'http://127.0.0.1:8000/tasks?is_completed=false&search=FastAPI&sort=created_at&order=desc&skip=0&limit=20'
```

## Running Tests

The test suite uses a separate PostgreSQL database.

Set the test database URL:

```bash
export TEST_DATABASE_URL="postgresql+psycopg2://task_api_user:password@localhost:5432/tasks_test"
```

Create the test database:

```sql
CREATE DATABASE tasks_test OWNER task_api_user;
```

Run the tests:

```bash
python -m pytest -v
```

The test suite covers:

- Task creation
- Invalid input
- Task listing
- Pagination
- Completion filtering
- Task retrieval
- Non-existent tasks
- Task updates
- Task deletion
- Health check

## Production Deployment

The application can be deployed directly on a Linux server using Gunicorn, Uvicorn workers, and systemd.

### 1. Install the project on the server

```bash
git clone https://github.com/Mahdiwav/task-management-api.git
cd task-management-api
```

Create the virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure the production `.env` file with the PostgreSQL connection URL.

### 2. Test Gunicorn manually

From the project directory:

```bash
.venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

The API should then be available on the configured Gunicorn port.

### 3. Configure systemd

Create a service file:

```bash
sudo nano /etc/systemd/system/task-api.service
```

Example configuration:

```ini
[Unit]
Description=Task Management API
After=network.target postgresql.service

[Service]
User=YOUR_LINUX_USER
Group=YOUR_LINUX_USER
WorkingDirectory=/path/to/task-management-api
EnvironmentFile=/path/to/task-management-api/.env
ExecStart=/path/to/task-management-api/.venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000 app.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Replace `YOUR_LINUX_USER` and the project paths with the actual values on the server.

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable the service at boot:

```bash
sudo systemctl enable task-api
```

Start the service:

```bash
sudo systemctl start task-api
```

Check its status:

```bash
sudo systemctl status task-api
```

View application logs:

```bash
sudo journalctl -u task-api -f
```

Restart after deploying changes:

```bash
sudo systemctl restart task-api
```

## HTTP Status Codes

| Status Code | Meaning |
|---|---|
| `200` | Successful request |
| `201` | Task created successfully |
| `204` | Task deleted successfully |
| `404` | Task not found |
| `422` | Request validation failed |

## Repository

GitHub:

https://github.com/Mahdiwav/task-management-api

## License

This project is provided for demonstration and evaluation purposes.