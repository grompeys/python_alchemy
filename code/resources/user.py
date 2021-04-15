# pylint: disable=import-error
import psycopg2
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from werkzeug.security import safe_str_cmp
# pylint: enable=import-error

from models.user import UserModel
from blocklist import BLOCKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help='This field cannot be empty.'
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help='This field cannot be empty.'
)


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {
                'message': 'A user with that username already exists.'
            }, 400

        user = UserModel(**data)
        user.upsert()

        return {
            'message': 'User created successfully.'
        }, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if user:
            return user.json(), 200
        return {
            'message': 'User not found.'
        }, 404

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if user:
            try:
                user.delete()
                return {
                    'message': 'User deleted.'
                }, 200
            except:
                return {
                    'message': 'An error occurred while deleting the user'
                }, 500
        return {
            'message': 'User not found.'
        }, 404


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()
        # find user in db
        user = UserModel.find_by_username(data['username'])
        # check password
        if user and safe_str_cmp(user.password, data['password']):
            # create token
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(user.id)

            # return tokens
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {
            'message': 'Invalid credentials.'
        }, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti'] # jti: a unique id for JWT
        BLOCKLIST.add(jti)
        return {
            'message': 'Successfully logged out'
        }, 200


class TokenRefresh(Resource):
    # We are using the `refresh=True` options in jwt_required to only allow
    # refresh tokens to access this route.
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {
            'access_token': new_token
        }, 200
