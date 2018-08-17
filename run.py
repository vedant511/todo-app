from flask import Flask, render_template, request
from app.database import Database
from models.user import User

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')  # Uncomment this in Production
app.config.from_pyfile('config.py')  # Uncomment this during development and staging


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/auth/login', methods=['POST'])
def login_user():
    identifier = request.form['email']
    password = request.form['password']

    if User.login(identifier, password):
        if User.get_by_mail(identifier) is not None:
            user = User.get_by_mail(identifier)

        else:
            user = User.get_by_unm(identifier)

        return render_template('profile.html', name=user.name)

    else:
        error = "Invalid credentials, please try again or register"
        return render_template('login.html', error=error)


@app.route('/auth/register', methods=['POST'])
def register_user():
    if request.form["submit"] == "login":
        return render_template("login.html")

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    username = request.form['username']

    user = User.register(name, email, password, username)

    if user == "Registered":
        return render_template("profile.html", name=name)

    else:
        error = user
        return render_template("register.html", error=error)


if __name__ == "__main__":
    app.run()
