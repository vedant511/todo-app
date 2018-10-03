from flask import Blueprint, render_template, request
from src.models.tasks.task import Task
import src.models.tasks.errors as TaskErrors

__author__ = 'Vedant Sharma'

task_blueprint = Blueprint('tasks', __name__)


@task_blueprint.route('/new', methods=['POST', 'GET'])
def create_task():
    if request.method == 'POST':
        pass

    # What happens if it's a GET request
    return render_template('tasks/create_task.html')


@task_blueprint.route('/delete/<string:task_id>')
def delete_task():
    pass


@task_blueprint.route('/update/<string:task_id>', methods=['POST'])
def update_task(task_id):
    pass


@task_blueprint.route('/task/<string:task_id>')
def load_task(task_id):
    pass


@task_blueprint.route('/for_user/<string:user_id>')
def load_tasks_for_user(user_id):
    pass
