from flask import Flask, request, jsonify
app = Flask(__name__)

tasks = []

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
    new_task = request.json.get('task')
    for task in tasks:
        if task["id"] == id:
            task["task"] = new_task
            return jsonify({"message": "Task updated"})
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t["id"] != id]
    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True)

'''
## API Endpoints
- `GET /tasks`
- `POST /tasks`
- `PUT /tasks/<id>`
- `DELETE /tasks/<id>`
'''