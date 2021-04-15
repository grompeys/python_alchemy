# pylint: disable=import-error
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, reqparse
# pylint: enable=import-error

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank.'
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Every item must belong to a store.'
    )

    # Only allow fresh JWTs to access this route 
    # with the `fresh=True` arguement.
    @jwt_required(fresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {
                'message': F"An item with the name: '{name}' already exists."
            }, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.upsert()
        except:
            return {
                'message': 'An error occurred saving the item.'
            }, 500

        return {
            'item': item.json(),
            'message': 'Item added successfully.'
        }, 201

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {
                'message': 'An error occurred while fetching the item.'
            }, 500

        if item:
            return item.json(), 200
        return {
            'message': 'No item found with that name.'
        }, 404

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        try:
            item.upsert()
        except:
            return {
                'message': 'An error occurred saving the item.'
            }, 500

        return {'message': 'Item saved', 'item': item.json()}, 200

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {
                'message': 'Admin privilege required.'
            }, 401

        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete()
            except:
                return {
                    'message': 'An error occurred deleting the item.'
                }, 500

            return {
                'message': 'Item deleted successfully.'
            }, 200
        return {
            'message': 'No item found with that name.'
        }, 400


class ItemList(Resource):

    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()

        items = [
            row.json() for row in ItemModel.find_all()
        ]

        if items:
            if user_id:
                return {'items': items}, 200
            return {
                # returns only the item's name
                'items': [item['name'] for item in items],
                'message': 'More data available if you log in.'
            }, 200
        return {
            'items': None,
            'message': 'No items found.'
        }, 404
