from flask import Blueprint, render_template, request, session, url_for, redirect
from src.models.users.user import User
import src.models.users.errors as UserErrors

__author__ = 'Vedant Sharma'

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        identifier = request.form['email']
        password = request.form['password']

        try:

            if User.login(identifier, password):
                if User.get_by_mail(identifier) is not None:
                    user = User.get_by_mail(identifier)

                else:
                    user = User.get_by_unm(identifier)

                if user.isAdmin:
                    return render_template('users/admin.html', name=user.name)
                else:
                    tasks = user.get_tasks()
                    return render_template('users/home.html', name=user.name, tasks=tasks)

        except UserErrors.UserError as e:
            error = e
            return render_template('users/login.html', error=error)

    return render_template('users/login.html')


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        if request.form["submit"] == "login":
            return render_template("users/login.html")

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']

        try:
            if User.register(name, email, password, username):
                session['email'] = email
                return render_template('users/home.html', name=name)

        except UserErrors.UserError as e:
            error = e
            return render_template('users/register.html', error=error)

    return render_template('users/register.html')


@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return redirect(url_for('home'))


# @user_blueprint.route('/tasks')
# def get_tasks():
#     user = User.get_by_mail(email=session['email'])
#     tasks = User.get_tasks()
#
#     return redirect(url_for('users.get_tasks'))


@user_blueprint.route('/home')
def home():
    email = session['email']
    user = User.get_by_mail(email)
    tasks = user.get_tasks()
    print(tasks)
    return render_template('users/home.html', name=user.name, tasks=tasks)
