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
            'email': request.form['email'],
            'type': request.form['tp'],
            'illness': request.form['illness'],
            'age': request.form['age'],
            'number': request.form['number'],
            'call': request.form.get('call', 'false') 
        }
        db.child("candidates").push(account_info)
        return redirect(url_for('home'))
    return render_template("join.html")



@app.route('/process', methods=['GET', 'POST'])
def process():
    return render_template("timeline.html")


@app.route('/aboutus')
def aboutus():
    return render_template('abtUs.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Check if the user is logged in
    if 'logged_in' in login_session and login_session['logged_in']:
        candidates_data = db.child("candidates").get()

        if candidates_data.each():
            candidates_list = [{"candidate_id": candidate.key(), "candidate_data": candidate.val()} for candidate in candidates_data.each()]
        else:
            candidates_list = []

        return render_template('admin.html', candidates=candidates_list)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        if (email == 'ukko@gmail.com') and (password == "12345678"):
            login_session['logged_in'] = True
            return redirect(url_for("admin"))
        else:
            flash("Invalid email or password", "error")
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    login_session.clear()
    return redirect(url_for('home'))

@app.route('/remove_candidate/<candidate_id>', methods=['POST'])
def remove_candidate(candidate_id):
    db.child("candidates").child(candidate_id).remove()
    flash("Candidate removed successfully!", "success")
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True)