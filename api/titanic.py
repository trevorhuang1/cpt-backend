import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource
from datetime import datetime
from model.titanics import TitanicRegression, predictSurvival
import pandas as pd
import seaborn as sns
import numpy as np

# Define the Titanic API blueprint
titanic_api = Blueprint("titanic_api", __name__, url_prefix="/api/titanic")
api = Api(titanic_api)

class TitanicAPI:
    class Passenger(Resource):
        def get(self):
            passenger = pd.DataFrame({
                'name': ['John Mortensen'],
                'pclass': [2],  # 2nd class picked as it was median, bargains are my preference, but I don't want to have poor accomodations
                'sex': ['male'],
                'age': [64],
                'sibsp': [1],  # I usually travel with my wife
                'parch': [1],  # currently I have 1 child at home
                'fare': [16.00],  # median fare picked assuming it is 2nd class
                'embarked': ['S'],  # majority of passengers embarked in Southampton
                'alone': [False]  # travelling with family (spouse and child)
            })

            response = predictSurvival(self=self, passenger=passenger)  # Assuming predictSurvival is defined elsewhere
            return response

    api.add_resource(Passenger, "/")  # Register Passenger resource