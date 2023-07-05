import json

from flask_restx import Namespace, Resource, fields
from slugify import slugify

from ..database import db
from ..models import Comuna

ns = Namespace("comunas")

comuna_schema = ns.model("Comuna", {"slug": fields.String, "nombre": fields.String, "region": fields.String})


@ns.route("/")
class lista_comunas(Resource):
    @ns.marshal_list_with(comuna_schema)
    def get(self):
        return Comuna.query.filter(Comuna.ferias.any()).all()
