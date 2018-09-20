from flask import Blueprint, render_template, request

__author__ = 'Vedant Sharma'

task_blueprint = Blueprint('tasks', __name__)


@task_blueprint.route('/new', methods=['POST'])
def create_task():
    pass


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
