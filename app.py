from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'



config = {
    'apiKey': "AIzaSyDjLN-RtkPkgWL8FNb0wsKPYf9TseG1P7k",
    'authDomain': "ukko-project-6645b.firebaseapp.com",
    'projectId': "ukko-project-6645b",
    'storageBucket': "ukko-project-6645b.appspot.com",
    'messagingSenderId': "797815642342",
    'appId': "1:797815642342:web:67f2b736a8da68c6858327",
    "databaseURL": "https://ukko-project-6645b-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase =pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html")


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        account_info = {
            'name': request.form['name'],
            'email':request.form['email'],
            'sex':request.form['sex'],
            'question1':request.form['question1'],
            'question2':request.form['question2'],
            'question3':request.form['question3'],
            'alg':request.form.getlist('alg'),
            'fufu':request.form.getlist('fufu')
        }
        db.child("candidates").push(account_info)
    return render_template("join.html")


@app.route('/process', methods=['GET', 'POST'])
def process():
    return render_template("timeline.html")


@app.route('/aboutus')
def aboutus():
    return render_template('abtUs.html')

if __name__ == '__main__':
    app.run(debug=True)