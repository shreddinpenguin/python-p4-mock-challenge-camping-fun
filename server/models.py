from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    # Add relationship
    signup = db.relationship('Signup', back_populates='activity')
    # Add serialization rules
    serialize_rules = ('-signup.activity',)
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)

    # Add relationship
    signup = db.relationship('Signup', back_populates='camper')
    # Add serialization rules
    serialize_rules = ('-signup.camper',)
    # Add validation
    @validates('age')
    def validate_age(self, key, value):
        if value not in range(8, 19):
            raise ValueError("Not valid age")
        return value
    
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Not name")
        return value
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    # Add relationships
    activity = db.relationship("Activity", back_populates='signup')
    camper = db.relationship("Camper", back_populates='signup')
    # Add serialization rules
    serialize_rules = ('-activity.signup', '-camper.signup',)
    # Add validation
    @validates('time')
    def validates_time(self, key, value):
        if value not in range(0, 24):
            raise ValueError("Not valid time")
        return value
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
