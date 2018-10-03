from flask import Blueprint, render_template, request, redirect, url_for, session
from src.models.tasks.task import Task
import src.models.tasks.errors as TaskErrors

__author__ = 'Vedant Sharma'

task_blueprint = Blueprint('tasks', __name__)


@task_blueprint.route('/new', methods=['POST', 'GET'])
def create_task():
    if request.method == 'POST':
        if request.form['action'] == 'create':
            title = request.form['title']
            description = request.form['description']
            group = request.form['cat']
            timeDue = request.form['due-date']
            timeRemind = request.form['remind-at']
            priority = request.form['priority']

            freq_num = request.form['freq']
            freq_timeframe = request.form['freq-time']
            reminderFreq = freq_num + freq_timeframe

            user_id = session['email']

            try:
                if Task.create_task(user_id, title, description, timeDue, priority, timeRemind, reminderFreq, group):
                    return redirect(url_for('users.home'))
            except TaskErrors.TaskError as e:
                error = e
                return render_template('tasks/create_task.html', error=error)

        elif request.form['action'] == 'cancel':
            return redirect(url_for('users.home'))

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
