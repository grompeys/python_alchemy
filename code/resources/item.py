# pylint: disable=import-error
from flask_jwt import jwt_required
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

    @jwt_required()
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

    @jwt_required()
    def get(self):
        items = {
            'items': [
                row.json() for row in ItemModel.query.all()
            ]
        }

        if items:
            return items, 200
        return {
            'items': None,
            'message': 'No items found.'
        }, 404
