import os

# pylint: disable=import-error
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
# pylint: enable=import-error

import config

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ['SECRET_KEY']
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# JWT creates the '/auth' endpoint
# when reached, username and password are sent to our authenticate
# if matched, it return a JWT
jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
