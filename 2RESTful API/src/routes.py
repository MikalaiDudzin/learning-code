import datetime
from flask import request
from flask_restful import Resource
from src import api, db
from src.models import Film

class Smoke(Resource):
    def get(self):
        return {'hello': 'world'}

#
# def get_all_films():
#     return [
#         {
#             'id': '1',
#             'title': 'Harry Potter and the Philosopher\'s Stone',
#             'release_date': date(2001, 11, 4)
#         },
#         {
#             'id': '2',
#             'title': 'Harry Potter and Chamber of Secrets',
#             'release_date': date(2002, 11, 3)
#         },
#         {
#             'id': '3',
#             'title': 'Harry Potter and the Prizoner of Azkaban',
#             'release_date': date(2004, 6, 4)
#         },
#         {
#             'id': '4',
#             'title': 'Harry Potter and the Goblet of Fire',
#             'release_date': date(2005, 11, 6)
#         }
#     ]
#
#
# def get_film_by_uuid(uuid: str) ->dict:
#     films = get_all_films()
#     film = list(filter(lambda f: f['id'] == uuid, films))
#     return film[0] if film else {}
#
#
# def create_film(film_json: dict) -> list[dict]:
#     films = get_all_films()
#     films.append(film_json)
#     return films
#     pass
from src.models import Film


class FilmListApi(Resource):

    def get(self, uuid=None):
        if not uuid:
            films = db.session.query(Film).all()
            return [f.to_dict() for f in films], 200
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return "", 404
        return film.to_dict(), 200

    def post(self):
        film_json = request.json
        if not film_json:
            return {'message': 'Wrong data'}, 400
        try:
            film = Film(
                title=film_json['title'],
                release_date=datetime.datetime.strptime(film_json['release_date'], '%B %d, %Y'),
                distributed_by=film_json['distributed_by'],
                rating=film_json.get('rating'),
                length=film_json.get('length'),
                description=film_json.get('description')
            )
            db.session.add(film)
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Created successfully', 'uuid': film.uuid}, 201

    def put(self, uuid):
        film_json = request.json
        if not film_json:
            return {'message': 'Wrong data'}, 400
        try:
            db.session.query(Film).filter_by(uuid=uuid).update(
                dict(
                    title=film_json['title'],
                    release_date=datetime.datetime.strptime(film_json['release_date'], '%B %d, %Y'),
                    distributed_by=film_json['distributed_by'],
                    rating=film_json.get('rating'),
                    length=film_json.get('length'),
                    description=film_json.get('description')
                )
            )
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Updated successfully'}, 200

    def patch(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return "", 404
        film_json = request.json
        title = film_json.get('title')
        release_date = datetime.datetime.strptime(film_json.get('release_date'), '%B %d, %Y') if film_json.get(
            'release_date') else None
        distributed_by = film_json.get('distributed_by'),
        rating = film_json.get('rating'),
        length = film_json.get('length'),
        description = film_json.get('description')

        if title:
            film.title = title
        elif release_date:
            film.release_date = release_date
        elif distributed_by:
            film.distributed_by = distributed_by
        elif rating:
            film.rating = rating
        elif length:
            film.length = length
        elif description:
            film.description = description

        db.session.add(film)
        db.session.commit()
        return {'message': 'Updated successfully'}, 200

    def delete(self, uuid):
        film = db.session.query(Film).filter_by(uuid=uuid).first()
        if not film:
            return "", 404
        db.session.delete(film)
        db.session.commit()
        return '', 204


class ActorListApi(Resource):
    def get(self, uuid=None):
        pass

    def post(self):
        pass

    def put(self, uuid):
        pass

    def delete(self, uuid):
        pass


api.add_resource(Smoke, '/smoke', strict_slashes=False)
api.add_resource(FilmListApi, '/films', '/films/<uuid>', strict_slashes=False)
api.add_resource(ActorListApi, '/actors', '/actors/<uuid>', strict_slashes=False)