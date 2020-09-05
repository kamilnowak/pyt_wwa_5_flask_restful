import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by(cls, query, value):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        result = cursor.execute(query, value)
        row = result.fetchone()

        user = None
        if row:
            user = UserModel(row[0], row[1], row[2])

        connection.commit()
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        return UserModel.query.filter_by(id=id).first()

    @classmethod
    def find_by_username(cls, username):
        return UserModel.query.filter_by(username=username).first()
        # query = "SELECT * FROM users where username=?"
        # return cls.find_by(query, (username,))

