from flask import Flask, request
from flask_restx import Api, Resource, fields
from utils import (load_cakes, save_cakes, get_next_id)
from models import create_cake_model
import json

app = Flask(__name__)
api = Api(app, version='1.0', title='Cake API', description='A simple Cake API')
cake_model = create_cake_model(api)

@app.route('/')
def home():
    return "Welcome to the Cake API!"

@api.route('/cakes')
class CakeList(Resource):
    @api.doc('list_cakes')
    @api.marshal_list_with(cake_model)
    def get(self):
        return load_cakes()

    @api.doc('add_cake')
    @api.expect(cake_model)
    def post(self):
        cakes = load_cakes()
        new_cake = api.payload
        new_cake['id'] = get_next_id(cakes)
        cakes.append(new_cake)
        save_cakes(cakes)
        return {'result': 'Cake added'}, 201

@api.route('/cake/<int:id>')
@api.response(404, 'Cake not found')
@api.param('id', 'The cake identifier')
class Cake(Resource):
    @api.doc('delete_cake')
    def delete(self, id):
        cakes = load_cakes()
        cake = next((cake for cake in cakes if cake['id'] == id), None)
        if not cake:
            api.abort(404, f"Cake with id {id} not found")
        updated_cakes = [cake for cake in cakes if cake['id'] != id]
        save_cakes(updated_cakes)
        return {'result': 'Cake deleted'}, 200

if __name__ == '__main__':
    app.run(debug=True)