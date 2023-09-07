from flask import Flask, render_template, request, g, jsonify
from redis import Redis
import os
import socket
import random
import json
import logging
import uuid

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['POST', 'GET'])
def task_list():
    user_id = request.cookies.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())

    success_message = None  

    if request.method == 'POST':
        task_title = request.form['task_title']
        task_description = request.form['task_description']
        task = {
            'id': str(uuid.uuid4()),
            'title': task_title,
            'description': task_description,
            'completed': False
        }
        add_task(task)

        
        success_message = 'Tarefa adicionada com sucesso.'

    tasks = get_tasks()

    return render_template(
        'index.html',
        tasks=tasks,
        user_id=user_id,
        success_message=success_message
    )

def add_task(task):
    redis = get_redis()
    data = json.dumps(task)
    redis.rpush('tasks', data)

def get_tasks():
    redis = get_redis()
    task_json_list = redis.lrange('tasks', 0, -1)
    tasks = [json.loads(task_json) for task_json in task_json_list]
    return tasks

@app.route("/tasks", methods=['GET'])
def get_tasks_json():
    tasks = get_tasks()
    return jsonify(tasks)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
