#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/campers', methods=['GET', 'POST'])
def get_campers():
    campers = Camper.query.all()
    if request.method == 'GET':
        all_campers = []
        for camper in campers:
            all_campers.append(camper.to_dict(only=('id', 'name', 'age')))
        return make_response(all_campers, 200)
        # return make_response([camper.to_dict() for camper in Camper.query.all()], 200)
    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_camper = Camper(
                name = data['name'],
                age = data['age']
            )
            db.session.add(new_camper)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({"errors": ["validation errors"] }), 400)
        return make_response(new_camper.to_dict(), 201)

@app.route('/campers/<int:id>', methods=['GET', 'PATCH'])
def campers_by_id(id):
    camper = Camper.query.filter(Camper.id == id).first()
    if request.method == 'GET':
        if not camper:
            return make_response({"error": "Camper not found"}, 404)
        else:
            return make_response(camper.to_dict(), 200)
    elif request.method == 'PATCH':
        data = request.get_json()
        if not camper:
            return make_response(jsonify({"error": "Camper not found"}), 404)
        try:
            for attr in data:
                setattr(camper, attr, data[attr])
            db.session.add(camper)
            db.session.commit()
        except Exception as e:
            return make_response({'errors': ['validation errors']}, 400)
        return make_response(camper.to_dict(), 202)

    
@app.route('/activities')
def get_activities():
    return make_response([activity.to_dict() for activity in Activity.query.all()], 200)

@app.route('/activities/<int:id>', methods=['GET', 'DELETE'])
def activity_by_id(id):
    activity = Activity.query.filter(Activity.id == id).first()
    if request.method == 'GET':
        return make_response(activity.to_dict(), 200)
    elif request.method == 'DELETE':
        if activity:
            db.session.delete(activity)
            db.session.commit()
            return make_response(activity.to_dict(), 204)
        else:
            return make_response({"error": "Activity not found"}, 404)
        
@app.route('/signups', methods = ['GET', 'POST'])
def sign_up():
    signups = Signup.query.all()
    if not signups:
        return make_response({ "errors": ["validation errors"] }, 400)
    else:
        if request.method == 'GET':
            return make_response([signup.to_dict() for signup in Signup.query.all()], 200)
        elif request.method == 'POST':
            try:
                data = request.get_json()
                new_signup = Signup(
                    camper_id = data['camper_id'],
                    activity_id = data['activity_id'],
                    time = int(data['time'])
                )
                db.session.add(new_signup)
                db.session.commit()
                return make_response(new_signup.to_dict(), 201)
            except Exception as e:
                return make_response({ "errors": ["validation errors"] }, 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
