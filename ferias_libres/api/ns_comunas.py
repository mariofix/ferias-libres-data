import json

from flask_restx import Namespace, Resource, fields
from slugify import slugify

from ..database import db
from ..models import Comuna

ns = Namespace("comunas")

comuna_schema = ns.model("Comuna", {"slug": fields.String, "nombre": fields.String})


@ns.route("/carga-comunas/")
class carga_comunas(Resource):
    @ns.marshal_list_with(comuna_schema)
    def get(self):
        with open(
            "/home/mariofix/proyectos/ferias-libres-data/ferias_libres/comunas_geoloc.json",
            encoding="utf-8",
        ) as f:
            nuevas = []
            lista = json.load(f)
            for comuna in lista:
                row = {
                    "slug": slugify(comuna["Comuna"].strip()),
                    "nombre": comuna["Comuna"].strip(),
                    "cut": comuna["CUT (Código Único Territorial)"],
                    "provincia": slugify(comuna["Provincia"].strip()),
                    "region": slugify(comuna["Región"].strip()),
                    "ubicacion": {
                        "latitude": comuna["Latitud (Decimal)"],
                        "longitude": comuna["Longitud (decimal)"],
                    },
                }
                nueva = Comuna(**row)
                db.session.add(nueva)
                db.session.commit()
                nuevas.append(nueva)
        return nuevas


@ns.route("/")
class lista_comunas(Resource):
    @ns.marshal_list_with(comuna_schema)
    def get(self):
        return Comuna.query.filter(Comuna.ferias.any()).all()
