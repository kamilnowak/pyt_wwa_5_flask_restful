import http

from flask import Flask, request
from flask_jwt import JWT, jwt_required
from flask_restful import Api, Resource, reqparse
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'my-secret-key'
api = Api(app)
jwt = JWT(
    app,
    authentication_handler=authenticate,
    identity_handler=identity
)

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


class Student(Resource):
    def get(self, name):
        return {'student': name}

    def post(self, name):
        return {'student': name}


movies = []


class Movie(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "genre", type=str, required=True, help="This field cannot be blank!",
    )
    parser.add_argument(
        "year", type=int, required=True, help="This field cannot be blank!",
    )

    def get(self, name):
        for movie in movies:
            if movie["name"] == name:
                return movie
        return {
            "message": "movie not found"
        }, 404

    def delete(self, name):
        global movies
        movies = [movie for movie in movies if movie['name'] != name]
        return {"message": "movie deleted"}, 204

    def put(self, name):
        data = Movie.parser.parse_args()
        movie = None
        status = 200
        for _movie in movies:
            if _movie["name"] == name:
                movie = _movie
        if movie is None:  # if movie not found, create it
            movies.append({"name": name, "genre": data["genre"]})
        else:
            movie.update(data)
            status = 204
        return movie, status




class MovieList(Resource):
    @jwt_required()
    def get(self):
        return {"movies": movies}

    def post(self):
        data = request.get_json(silent=True)
        movie = {"name": data['name'], "genre": data['genre']}
        movies.append(movie)
        return movie, 201


# /movie
#           - listowanie filmow (GET)
#           - tworzenie nowego filmu (POST)
# /movie/<title>
#           - pobranie pojedynczego filmu (GET)
#           - update pojedynczego filmu (PATCH, PUT)
#           - usunięcie pojedynczego filmu (DELETE)


api.add_resource(Student, '/student/<string:name>')
api.add_resource(Movie, '/movie/<string:name>')
api.add_resource(MovieList, '/movie')

if __name__ == '__main__':
    app.run()
