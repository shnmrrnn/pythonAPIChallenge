from flask_restx import fields, Model

def create_cake_model(api):
    cake_model = api.model('Cake', {
        'id': fields.Integer(required=True, description='The cake identifier'),
        'name': fields.String(required=True, description='The cake name', max_length=30),
        'comment': fields.String(required=True, description='A comment about the cake', max_length=200),
        'imageUrl': fields.String(required=True, description='Image URL of the cake'),
        'yumFactor': fields.Integer(required=True, description='Yum factor rating between 1 and 5', min=1, max=5)
    })
    return cake_model
