from flask import Flask, request
from flask_restx import Api, Resource, fields
import json

app = Flask(__name__)
api = Api(app, version='1.0', title='Cake API', description='A simple Cake API')

cake_model = api.model('Cake', {
    'id': fields.Integer(required=True, description='The cake identifier'),
    'name': fields.String(required=True, description='The cake name', max_length=30),
    'comment': fields.String(required=True, description='A comment about the cake', max_length=200),
    'imageUrl': fields.String(required=True, description='Image URL of the cake'),
    'yumFactor': fields.Integer(required=True, description='Yum factor rating between 1 and 5', min=1, max=5)
})

def load_cakes():
    try:
        with open('cakes.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_cakes(cakes):
    with open('cakes.json', 'w') as file:
        json.dump(cakes, file, indent=4)

def get_next_id(cakes):
    return max(cake['id'] for cake in cakes) + 1 if cakes else 1

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
