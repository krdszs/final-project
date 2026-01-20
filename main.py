from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool = False

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False                 # Added to be able to update completion status

tasks_file = "tasks.txt"                    # Variable for easier file reading

def load_tasks():                           # Load and handle file
    if not os.path.exists(tasks_file):      
        return []                           # Empty list if file doesn't exist
    
    tasks = []
    with open(tasks_file, "r") as f:
        for line in f:
            line = line.strip()
            tasks.append(json.loads(line))
    return tasks

def save_tasks(tasks):                      # Save list of tasks into file
    with open(tasks_file, "w") as f:
        for task in tasks:
            json_str = json.dumps(task)
            f.write(json_str + "\n")

def find_task_by_id(task_id: int):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def get_next_id():                          # Find the next id for a new task
    tasks = load_tasks()
    if not tasks:
        return 1
    else:
        max_id = max(task["id"] for task in tasks)
    return (max_id+1)

@app.get("/")
def root():
    return {"message": "Task Management API is running"}

@app.get("/tasks")
def get_all_tasks(completed: bool | None = None):
    tasks = load_tasks()

    if completed is None:                   # If no filter, list all tasks
        return tasks
    
    filtered_tasks = []
    for task in tasks:
        if task["completed"] == completed:              # Filtering by "complete" status
            filtered_tasks.append(task)

    return filtered_tasks

@app.get("/tasks/stats")
def summarise():
    tasks = load_tasks()

    completed_count = 0                     # Number of completed tasks
    for task in tasks:
        if task["completed"] is True:
            completed_count += 1

    pending_count = len(tasks) - completed_count        # Number of not completed tasks

    if len(tasks) > 0:
        completion_percentage = (completed_count/len(tasks))*100
    else:
        completion_percentage = 0.0
    
    summary = {
        "total_tasks": len(tasks),
        "completed_count": completed_count,
        "pending_count": pending_count,
        "completion_percentage": f"{completion_percentage:.2f}%"
    }
    return summary

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks")
def create_task(task_create: TaskCreate):
    tasks = load_tasks()
    task = {
        "id": get_next_id(),                # Auto-generated id
        "title": task_create.title,             
        "description": task_create.description,
        "completed": False                  # Defaults to false (not logical to add completed task)    
    }
    
    tasks.append(task)
    save_tasks(tasks)
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskCreate):
    tasks = load_tasks()
    
    task_index = None
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            task_index = i
            break
    
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks[task_index]["title"] = task_update.title
    tasks[task_index]["description"] = task_update.description              # Complete modification of task except id
    tasks[task_index]["completed"] = task_update.completed
    save_tasks(tasks)
    return tasks[task_index]

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()

    task_index = None
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            task_index = i
            break
    
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    deleted_task = tasks.pop(task_index)
    save_tasks(tasks)
    return {"message": "Task deleted successfully", "Deleted task": deleted_task}

@app.delete("/tasks")
def delete_all_tasks():
    tasks = load_tasks()
    tasks.clear()

    save_tasks(tasks)
    return {"message": "All tasks deleted successfully"}
