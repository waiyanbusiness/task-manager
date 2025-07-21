from flask import Flask, request, jsonify
app = Flask(__name__)

tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json.get('task')
    tasks.append({"id": len(tasks)+1, "task": task})
    return jsonify({"message": "Task added!"}), 201

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
