from flask import Flask, render_template
from src.common.database import Database

__author__ = 'Vedant Sharma'

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')  # Uncomment this in Production
# app.config.from_pyfile('config.py')  # Uncomment this during development and staging


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.html')


from src.models.users.views import user_blueprint
from src.models.tasks.views import task_blueprint
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(task_blueprint, url_prefix='/tasks')
