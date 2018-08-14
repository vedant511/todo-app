from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')
app.config.from_pyfile('config.py')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
