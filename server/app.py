#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
      """
    Represents a resource for managing a list of plants.
    This resource supports HTTP GET and POST methods for retrieving and creating plant data.
    """
def get(self):
        """
        Retrieve a list of all plants.
        Returns:
            Response: A JSON response containing a list of plant data.
        """
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

def post(self):
        """
        Create a new plant.
        Returns:
            Response: A JSON response containing the newly created plant data.
        """

        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


api.add_resource(Plants, '/plants')
class PlantByID(Resource):
      """
    Represents a resource for managing an individual plant by ID.
    This resource supports HTTP GET method for retrieving a specific plant by its ID.
    """

def get(self, num):
        """
        Retrieve a specific plant by its ID.
        Args:
            num (int): The unique identifier of the plant.
        Returns:
            Response: A JSON response containing the plant data for the specified ID.
        """
        plant = Plant.query.filter_by(id=num).first().to_dict()
        return make_response(jsonify(plant), 200)


api.add_resource(PlantByID, '/plants/<int:num>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)