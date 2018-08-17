from flask import Flask, render_template, request
from app.database import Database
from models.user import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')  # Uncomment this in Production
app.config.from_pyfile('config.py')  # Uncomment this during development and staging


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/auth/login', methods=['POST'])
def login_user():
    identifier = request.form['email']
    password = request.form['password']

    print(identifier, password)

    if User.login(identifier, password):
        print("A")
        if User.get_by_mail(identifier) is not None:
            print("A1")
            user = User.get_by_mail(identifier)
            print("A1pass")
        else:
            print("A2")
            user = User.get_by_unm(identifier)
            print("A2pass")

        return render_template('profile.html', name=user['name'])

    else:
        print("B")
        error = "Invalid credentials, please try again or register"
        return render_template('login.html', error=error)


if __name__ == "__main__":
    app.run()
