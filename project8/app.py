from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple in-memory database to store tasks
todos = []

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    if request.is_json:
        data = request.get_json()
        if 'task' not in data:
            return jsonify({'error': 'Bad Request', 'message': 'Task is required'}), 400

        todo = {
            'id': len(todos) + 1,
            'task': data['task']
        }
        todos.append(todo)
        return jsonify(todo), 201
    return jsonify({'error': 'Unsupported Media Type', 'message': 'Content-Type must be application/json'}), 415

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo is None:
        return jsonify({'error': 'Not Found', 'message': 'Task not found'}), 404

    todos.remove(todo)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
