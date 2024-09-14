# app/models.py

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Route(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    finish_time = db.Column(db.Time, nullable=False)
    start_mileage = db.Column(db.Integer, nullable=False)
    end_mileage = db.Column(db.Integer, nullable=False)
    total_mileage = db.Column(db.Integer, nullable=False)
    container_number = db.Column(db.String(20), nullable=False)
    chassis_number = db.Column(db.String(20), nullable=False)
    route_from = db.Column(db.String(100), nullable=False)
    route_to = db.Column(db.String(100), nullable=False)
    load_status = db.Column(db.String(10), nullable=False)
    standby_time_in = db.Column(db.Time, nullable=True)
    standby_time_out = db.Column(db.Time, nullable=True)
    total_hours = db.Column(db.Float, nullable=False)
    inspection = db.relationship('Inspection', backref='route', uselist=False)

class Inspection(db.Model):
    __tablename__ = 'inspections'
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'))
    lights = db.Column(db.Boolean, default=False)
    tires = db.Column(db.Boolean, default=False)
    brakes = db.Column(db.Boolean, default=False)
    # Additional inspection fields
    remarks = db.Column(db.Text, nullable=True)
    signature = db.Column(db.Text, nullable=True)  # Base64-encoded image
