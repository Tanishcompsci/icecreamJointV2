from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class FlavorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Flavor(name = {name}, price = {price}"


db.create_all()

flavor_put_args = reqparse.RequestParser()
flavor_put_args.add_argument("name", type=str, help="Ice cream flavor is required", required=True)
flavor_put_args.add_argument("price", type=float, help="Price of the flavor", required=True)

flavor_update_args = reqparse.RequestParser()
flavor_update_args.add_argument("name", type=str, help="Name of the ice cream is required")
flavor_update_args.add_argument("price", type=float, help="Price of the ice cream")

resource_field = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Float
}


class IceCream(Resource):
    @marshal_with(resource_field)
    def get(self, flavor_id):
        result = FlavorModel.query.filter_by(id=flavor_id).first()
        if not result:
            abort(404, message="Could not find ice cream with that ID")
        return result

    @marshal_with(resource_field)
    def put(self, flavor_id):
        args = flavor_put_args.parse_args()
        result = FlavorModel.query.filter_by(id=flavor_id).first()
        if result:
            abort(409, message="Flavor id taken...")
        type = FlavorModel(id=flavor_id, name=args['name'], price=args['price'])
        db.session.add(type)  # temporarily adds to database
        db.session.commit()  # permanently in database
        return type, 201

    @marshal_with(resource_field)
    def patch(self, flavor_id):
        args = flavor_update_args.parse_args()
        result = FlavorModel.query.filter_by(id=flavor_id).first()
        if not result:
            abort(404, message="Ice cream doesn't exist, cannot update")

        if args['name']:  # checks if name exists in specified id
            result.name = args['name']
        if args['price']:
            result.price = args['price']

        db.session.commit()
        return result


api.add_resource(IceCream, "/iceCream/<int:flavor_id>")

if __name__ == "__main__":
    app.run(debug=True)
