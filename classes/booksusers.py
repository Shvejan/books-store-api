from flask_sqlalchemy import SQLAlchemy
import re
db=SQLAlchemy()

class books(db.Model):
    __tablename__='books'
    id = db.Column(db.Integer,primary_key='true')
    isbn=db.Column(db.String,nullable=False)
    title=db.Column(db.String,nullable=False)
    author=db.Column(db.String,nullable=False)
    year=db.Column(db.Integer,nullable=False)

    def display(self):
        print(self.isbn , self.title, self.author, self.year)
    def match(self,x):
        if re.search(x,self.isbn):
            return True
        if re.search(x,self.title) or re.search(x.capitalize(),self.title):
            return True
        if re.search(x,self.author) or re.search(x.capitalize(),self.author):
            return True
        return False


class users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key='true')
    username = db.Column(db.String,nullable=False,unique = True)
    password = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False,unique = True)

    def checkPass(self,a):
        if self.password==a:
            return True
        return False

class reviews(db.Model):
    __tablename__='reviews'
    id = db.Column(db.Integer,primary_key='true')
    msg = db.Column(db.String,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"),nullable=False)
