from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = []
counter = 1

class Task(BaseModel):
    title: str
    status: str
    created_at: Optional[datetime] = None

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.post("/list")
def create_task(task: Task):
    global counter
    new_task = {
        "id": counter,
        "title": task.title,
        "status": task.status,
        "created_at": task.created_at or datetime.utcnow(),
    }
    tasks.append(new_task)
    counter += 1
    return new_task

@app.get("/list")
def get_tasks():
    return tasks

@app.put("/list/{id}")
def update_task(id: int, task: Task):
    for t in tasks:
        if t["id"] == id:
            t["title"] = task.title
            t["status"] = task.status
            t["created_at"] = task.created_at or datetime.utcnow()
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/list/{id}")
def delete_task(id: int):
    for i, t in enumerate(tasks):
        if t["id"] == id:
            tasks.pop(i)
            return {"message": "deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
