import os
from booksusers import *
from flask import Flask,session
import csv
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL2")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    per = open("csv/books.csv")
    reader = csv.reader(per)
    for i,t,a,y in reader:
        x = books(isbn = i,title=t,author=a,year=y)
        db.session.add(x)
        db.session.commit()
if __name__ == '__main__':
    with app.app_context():
        main()
