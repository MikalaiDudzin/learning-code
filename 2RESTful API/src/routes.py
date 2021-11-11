from flask import request
from flask_restful import Resource, Api

from src import api


class Smoke(Resource):
    def get(self):
        return {'hello': 'world'}


def get_all_films():
    return [
        {
            'id': '1',
            'title': 'film 1',
            'release_date': 'date1'
        },
        {
            'id': '2',
            'title': 'film 2',
            'release_date': 'date2'
        },
        {
            'id': '3',
            'title': 'film 3',
            'release_date': 'date3'
        },
        {
            'id': '4',
            'title': 'film 4',
            'release_date': 'date4'
        }
    ]


def get_film_by_uuid(uuid: str) ->dict:
    films = get_all_films()
    film = list(filter(lambda f: f['id'] == uuid, films))
    return film[0] if film else {}


def create_film(film_json: dict) -> list[dict]:
    films = get_all_films()
    films.append(film_json)
    return films
    pass


class FilmListApi(Resource):
    def get(self, uuid=None):
        if not uuid:
            films = get_all_films()
            return films, 200
        film = get_film_by_uuid(uuid)
        if not film:
            return '', 404
        return film, 200

    def post(self):
        film_json = request.json
        return create_film(film_json), 201

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass


api.add_resource(Smoke, '/',strict_slasehs=False)
api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slasehs=False)
