from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building

from model.titanics import TitanicRegression

titanic_api = Blueprint('titanic_api', __name__,
                   url_prefix='/api/titanic')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(titanic_api)

# Initialize the model
titanic_model = TitanicRegression()

class TitanicApi:        
    class _CRUD(Resource): 
        def post(self):
            data = request.get_json()
            # print(data)
            alive_prob = titanic_model.predictSurvival(data)
            return jsonify(alive_prob)

    api.add_resource(_CRUD, '/')