import os
from flask import Flask,session,render_template,request,redirect,url_for,flash
from classes.booksusers import *
import requests

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
        cur_user = users.query.filter_by(username=n).first()
        if(cur_user.checkPass(p)):
            session['logged_in'] = True
            session['user']=n

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
        cur_user=users(username=n,password=p,email=e)
        db.session.add(cur_user)
        db.session.commit()
        session['logged_in'] = True
        session['user']=n
    return redirect(url_for('home'))

@app.route('/logout',methods=['POST','GET'])
def logout():
    if request.method == "GET":
        return redirect(url_for('home'))
    session['logged_in']=False
    return render_template('home.html')

@app.route('/results',methods=['POST'])
def results():
    exp = request.form.get('exp')
    p = books.query.all()
    x=[]
    for a in p:
        if a.match(exp):
            x.append(a)

    return render_template('results.html',x=x)

@app.route('/open/<string:var>',methods=['POST','GET'])
def open(var):
    b=books.query.filter_by(isbn=var).first()

    u = users.query.filter_by(username=session.get('user')).first()
    if request.method=='POST':
        r=reviews(msg = request.form.get('rev'), user_id=u.id, book_id=b.id)
        db.session.add(r)
        db.session.commit()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "j9nL5Qi4UvfI66ErTe0cHw", "isbns": var})
    all_rev = reviews.query.filter_by(book_id=b.id).all()
    d={}
    for x in all_rev:
        tu=users.query.filter_by(id=x.user_id).first()
        d[tu.username]=x.msg
    return render_template('open.html',  x=res.json(),b=b,all_rev = d )

@app.route('/api/<string:id>')
def api(id):
    x=books.query.filter_by(isbn=id).first()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "j9nL5Qi4UvfI66ErTe0cHw", "isbns": id})
    res=res.json()
    return {
    "title": x.title,
    "author": x.author,
    "year": x.year,
    "isbn": x.isbn,
    "review_count": res['books'][0]["reviews_count"],
    "average_score": res['books'][0]["average_rating"]
    }
