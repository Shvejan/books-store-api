import os
from flask import Flask, session,render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

if not os.getenv('DATABASE_URL'):
    raise RuntimeError('db not set')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login')
def login():
    pass
@app.route('/signup')
def signup():
    pass
