from flask import Flask, abort, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import *
from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Stations(Resource):
    def get(self):
        stations = [stations.to_dict() for stations in Station.query.all()]
        return make_response(
            stations,
            200
        )
    def post(self):
        data = request.get_json()
        new_station = Station(
            name=data["name"],
            city=data["city"]
        )
        db.session.add(new_station)
        db.session.commit()

        return make_response(
            new_station.to_dict(),
            200
        )
api.add_resource(Stations, "/stations")

class StationsByID(Resource):
    def get(self,id):
        station = Station.query.filter(Station.id == id).first().to_dict()
        return make_response(
            station,
            200
        )
api.add_resource(StationsByID, "/station/<int:id>")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
