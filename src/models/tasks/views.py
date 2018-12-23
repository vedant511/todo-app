from flask import Blueprint, render_template, request, redirect, url_for, session
from src.models.tasks.task import Task
import src.models.tasks.errors as TaskErrors
import datetime

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
            reminderFreq = freq_num + ' ' + freq_timeframe

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
def delete_task(task_id):
    Task.delete_single(task_id)
    return redirect(url_for('users.home'))


@task_blueprint.route('/update/<string:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    old_task = Task.get_by_task_id(task_id)
    freq, timeframe = old_task['reminderFreq'].split(' ')
    old_task['freq'] = freq
    old_task['timeframe'] = timeframe

    if request.method == 'POST':
        if request.form['action'] == 'update':
            update_query = dict()

            if request.form['description'] != old_task['description']:
                update_query['description'] = request.form['description']
            if datetime.datetime.strptime(request.form['due-date'], '%Y-%m-%dT%H:%M') != old_task['timeDue']:
                update_query['timeDue'] = datetime.datetime.strptime(request.form['due-date'], '%Y-%m-%dT%H:%M')
            if datetime.datetime.strptime(request.form['remind-at'], '%Y-%m-%dT%H:%M') != old_task['timeRemind']:
                update_query['timeRemind'] = datetime.datetime.strptime(request.form['remind-at'], '%Y-%m-%dT%H:%M')
            if request.form['cat'] != old_task['group']:
                update_query['group'] = request.form['cat']
            if request.form['priority'] != old_task['priority']:
                update_query['priority'] = request.form['priority']
            if request.form['freq'] + ' ' + request.form['freq-time'] != old_task['reminderFreq']:
                update_query['reminderFreq'] = request.form['freq'] + ' ' + request.form['freq-time']

            full_update_query = {'$set': update_query}
            Task.edit_task(task_id=task_id, edit_query=full_update_query)

            return redirect(url_for('users.home'))

        elif request.form['action'] == 'cancel':
            return redirect(url_for('users.home'))

    return render_template('tasks/edit_task.html', task=old_task)


@task_blueprint.route('/<string:task_id>')
def load_task(task_id):
    task = Task.get_by_task_id(task_id=task_id)
    return render_template('tasks/task.html', task=task)


@task_blueprint.route('/for_user/<string:user_id>')
def load_tasks_for_user(user_id):
    pass
