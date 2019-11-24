from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class books(db.Model):
    __tablename__='books'
    id = db.Column(db.Integer,primary_key='true')
    isbn=db.Column(db.String,nullable=False)
    title=db.Column(db.String,nullable=False)
    author=db.Column(db.String,nullable=False)
    year=db.Column(db.Integer,nullable=False)

class users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key='true')
    username = db.Column(db.String,nullable=False,unique = True)
    password = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False,unique = True)

    def checkPass(a):
        if password==a:
            return True
        return False
