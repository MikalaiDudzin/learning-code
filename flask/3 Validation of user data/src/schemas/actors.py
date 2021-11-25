from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.database.models import Actor


class ActorSchema(SQLAlchemyAutoSchema):
    class Mata:
        model = Actor
        load_instance = True