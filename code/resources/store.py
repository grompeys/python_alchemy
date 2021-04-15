# pylint: disable=import-error
import psycopg2
from flask_jwt_extended import jwt_required
from flask_restful import Resource
# pylint: enable=import-error

from models.store import StoreModel

class Store(Resource):
    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {
                'message': F"A store with the name: '{name}' already exists."
            }, 400
        store = StoreModel(name)

        try:
            store.upsert()
        except:
            return {
                'message': 'An error occurred saving the store.'
            }, 500

        return {
            'store': store.json(),
            'message': 'Store created successfully.'
        }, 201


    @jwt_required()
    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
        except:
            return {
                'message': 'An error occurred while fetching the store.'
            }, 500
        
        if store:
            return store.json(), 200
        return {
            'message': 'No item found with that name.'
        }, 404

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            try:
                store.delete()
                return {
                    'message': 'Item deleted successfully.'
                }, 200
            except:
                return {
                    'message': 'An error occurred while deleting the store.'
                }, 500
        return {
            'message': 'No item found with that name.'
        }, 400


class StoreList(Resource):
    
    @jwt_required()
    def get(self):
        return {
            'stores': [
                store.json() for store in StoreModel.find_all()
            ]
        }, 200