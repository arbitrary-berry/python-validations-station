from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Station(db.Model):
    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    city = db.Column(db.String(80))

    @validates("name")
    def validate_name(self,key,name):
        if len(name) >= 3:
            return name
        else:
            raise ValueError("Name must be at least 3 characters")

    def __repr__(self):
        return f"<Station {self.name}>"


class Platform(db.Model):
    __tablename__ = "platforms"

    id = db.Column(db.Integer, primary_key=True)
    platform_num = db.Column(db.Integer, nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey("stations.id"))

    @validates("platform_num")
    def validate_platform_num(self, key, platform_num):
        if 1 <= platform_num <= 20:
            return platform_num
        if not type(platform_num) == int:
            raise ValueError("Platform Num must be int")

    def __repr__(self):
        return f"<Platform {self.name}>"


class Train(db.Model):
    __tablename__ = "trains"

    id = db.Column(db.Integer, primary_key=True)
    train_num = db.Column(db.String)
    service_type = db.Column(db.String)
    origin = db.Column(db.String, nullable = False)
    destination = db.Column(db.String, nullable = False)

    @validates("origin")
    def validates_origin (self,key,origin):
        if 3 <= len(origin) <= 24:
            return origin
    
    @validates("destination")
    def validates_destination (self,key,destination):
        if 3 <= len(destination) <= 24:
            return destination

    @validates("service_type")
    def validates_service_type(self,key,service_type):
        if service_type in ("local", "express"):
        # if service_type == "express" or service_type == "local"
            return service_type

    def __repr__(self):
        return f"<Train {self.name}>"


class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    arrival_time = db.Column(db.DateTime, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey("trains.id"))
    platform_id = db.Column(db.Integer, db.ForeignKey("platforms.id"))

    def __repr__(self):
        return f"<Assignment Train No: {self.train.train_num} Platform: {self.platform.platform_num}>"
