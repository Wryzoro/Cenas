import json
import os

class Task:
    def __init__(self, title, description=''):
        self.title = title
        self.description = description
        self.completed = False

    def complete(self):
        self.completed = True

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, task_dict):
        task = cls(task_dict['title'], task_dict['description'])
        task.completed = task_dict['completed']
        return task

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].complete()
            self.save_tasks()

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                tasks = json.load(file)
                return [Task.from_dict(task) for task in tasks]
        return []
