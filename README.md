# FastAPI Task Management System

An API built with FastAPI. Data is kept in a file in JSON Lines format. 
(Disclaimer: instructions written for UNIX based OS.)

## Features

- Create, read, update, and delete tasks
- Filter tasks by completion status
- View task statistics

## Requirements

- Python 3.10 or higher
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:

git clone https://github.com/krdszs/final-project.git
mkdir fastapi-tasks
cd fastapi-tasks

2. Install dependencies:

pip install fastapi uvicorn


3. Create an empty `tasks.txt` file:

touch tasks.txt


## Running the Application

Start the server with:

uvicorn main:app --reload

The API will be available at: `http://127.0.0.1:8000`

## API Documentation

Once the server is running, access SwaggerUI at:
`http://127.0.0.1:8000/docs`


## API Endpoints

### Root
- **GET /** - Check if API is running

### Tasks
- **GET /tasks** - Get all tasks (optional "completed" filter)
- **GET /tasks/stats** - Get statistics
- **GET /tasks/{task_id}** - Get a specific task by ID
- **POST /tasks** - Create a new task
- **PUT /tasks/{task_id}** - Update a specific task
- **DELETE /tasks/{task_id}** - Delete a specific task
- **DELETE /tasks** - Delete all tasks

## Example Usage

### Get All Tasks

curl "http://127.0.0.1:8000/tasks"

### Delete a Task
```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1"
```

## Data Model

### Task

{
  "id": 1,
  "title": "Task title",
  "description": "Task description (optional)",
  "completed": false
}

## Author

Zsombor Kardos
Zsombor.Kardos@Student.HTW-Berlin.de