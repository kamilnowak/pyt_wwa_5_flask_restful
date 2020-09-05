import sqlite3

from flask_restful import Resource, reqparse

from models import user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="Cannot be blank"
    )
    parser.add_argument(
        "password", type=str, required=True, help="Cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        connection = sqlite3.connect("../data.db")
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        try:
            cursor.execute(
                query,
                (data["username"], data["password"])
            )
        except sqlite3.IntegrityError:
            return {"message": "user already exists"}, 400
        connection.commit()
        connection.close()
        return {"message": "user created"}, 201
