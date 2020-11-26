from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

users_roles = db.Table('users_roles',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

