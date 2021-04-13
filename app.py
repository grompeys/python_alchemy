from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class Member(db.Model):
    # db.Model automatically creates the constructor
    # for the attributes defined bellow
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(60))
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return F'#{self.id} -- Member: {self.username}'


if __name__ == '__main__':
    app.run()