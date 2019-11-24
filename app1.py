import os
from flask import Flask,session,render_template,request,redirect,url_for
from classes.booksusers import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL2")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.secret_key = os.urandom(12)

@app.route('/')
def home():
    if session.get('logged_in'):
        return render_template('welcome.html')
    return render_template('home.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "GET":
        return redirect(url_for('home'))
    if session.get('logged_in'):
        return redirect(url_for('home'))
    else:
        n=request.form.get('lname')
        p=request.form.get('lpass')
        x = users.query.filter_by(username=n).first()
        if(x.checkPass):
            session['logged_in'] = True
        else:
            flash('wrong password!')
    return redirect(url_for('home'))



@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "GET":
        return redirect(url_for('home'))
    if session.get('logged_in'):
        return redirect(url_for('home'))
    else:

        n=request.form.get('sname')
        p=request.form.get('spass')
        e=request.form.get('semail')            
        x=users(username=n,password=p,email=e)
        db.session.add(x)
        db.session.commit()
        session['logged_in'] = True
    return redirect(url_for('home'))

@app.route('/logout',methods=['POST','GET'])
def logout():
    if request.method == "GET":
        return redirect(url_for('home'))
    session['logged_in']=False
    return render_template('home.html')
