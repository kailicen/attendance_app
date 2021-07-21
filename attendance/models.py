from sqlalchemy.orm import backref
from attendance import db, login_manager
from sqlalchemy.sql import func
from flask_login import UserMixin

import attendance


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    if_admin = db.Column(db.Boolean, nullable=False, default=False)
    if_member = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    mobile = db.Column(db.String(20))

    password = db.Column(db.String(60))

    attendance = db.relationship(
        'Attendance', cascade="all,delete", backref='member')

    def __repr__(self):
        return str(self.name)


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
