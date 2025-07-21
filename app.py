from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Setup app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
db = SQLAlchemy(app)

tasks = []

# ✅ Define Task Model Here
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "task": self.task}
#new setup with database
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task_name = data.get("task")
    if not task_name:
        return jsonify({"error": "Task name required"}), 400

    new_task = Task(task=task_name)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task added!", "task": new_task.to_dict()}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.task = data.get("task")
    db.session.commit()
    return jsonify({"message": "Task updated", "task": task.to_dict()})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})

''' old setup no database
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task_name = data.get("task")

    # Simple validation
    if not task_name:
        return jsonify({"error": "Task name is required"}), 400

    # Create a new task with ID
    new_task = {
        "id": len(tasks) + 1,
        "task": task_name
    }

    tasks.append(new_task)
    return jsonify({"message": "Task added!", "task": new_task}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    new_task_name = data.get("task")

    for task in tasks:
        if task["id"] == id:
            task["task"] = new_task_name
            return jsonify({"message": "Task updated!", "task": task})

    return jsonify({"error": "Task not found"}), 404


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    updated_tasks = [t for t in tasks if t["id"] != id]
    
    if len(updated_tasks) == len(tasks):
        return jsonify({"error": "Task not found"}), 404

    tasks = updated_tasks
    return jsonify({"message": "Task deleted!"})
'''

if __name__ == '__main__':
    app.run(debug=True)

'''
## API Endpoints
- `GET /tasks`
- `POST /tasks`
- `PUT /tasks/<id>`
- `DELETE /tasks/<id>`
'''