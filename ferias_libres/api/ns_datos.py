import datetime

from flask_restx import Namespace, Resource, fields

from ..database import db
from ..models import Comuna, Feria

ns = Namespace("datos")

schema_punto = ns.model(
    "PuntoInteres",
    {
        "tipo": fields.Integer,
        "titulo": fields.String,
        "link": fields.String,
    },
)
schema_semana = ns.model(
    "Semana",
    {
        "lunes": fields.Boolean,
        "martes": fields.Boolean,
        "miercoles": fields.Boolean,
        "jueves": fields.Boolean,
        "viernes": fields.Boolean,
        "sabado": fields.Boolean,
        "domingo": fields.Boolean,
        "especial": fields.Boolean,
        "motivo": fields.String,
    },
)
schema_feria = ns.model(
    "Feria",
    {
        "slug": fields.String,
        "nombre": fields.String,
        "dias": fields.Nested(schema_semana, skip_none=False),
        "dias_str": fields.String,
        "comuna_str": fields.String,
        "funcionando": fields.Boolean,
        "latlng": fields.List(fields.String),
        "puntos": fields.List(
            fields.Nested(schema_punto, skip_none=False),
        ),
    },
)
schema_comuna = ns.model("Comuna", {"slug": fields.String, "nombre": fields.String})
schema_pack_datos = ns.model(
    "PackDatos",
    {
        "fecha": fields.Date,
        "dia_semana": fields.String,
        "ferias_de_hoy": fields.Nested(schema_feria, skip_none=False),
        "todas_las_comunas": fields.Nested(schema_comuna, skip_none=False),
    },
)
schema_pack_feria = ns.model(
    "PackFeria",
    {
        "status": fields.String,
        "slug": fields.String,
        "info": fields.Nested(schema_feria, skip_none=False),
        "puntos": fields.String,
    },
)


def dia_de_la_semana(dia: int) -> str | None:
    semana = [
        "lunes",
        "martes",
        "miercoles",
        "jueves",
        "viernes",
        "sabado",
        "domingo",
    ]
    try:
        return semana[dia]
    except KeyError:
        return None


@ns.route("/app/index")
class pack_datos_index(Resource):
    @ns.marshal_list_with(schema_pack_datos)
    def get(self):
        dia_hoy = dia_de_la_semana(datetime.datetime.now().weekday())
        ferias_hoy = db.session.query(Feria).filter(Feria.dias[dia_hoy]).order_by(Feria.slug.asc()).all()

        comunas_con_feria = db.session.query(Comuna).filter(Comuna.ferias.any()).order_by(Comuna.slug.asc()).all()  # type: ignore
        pack_datos = {
            "fecha": datetime.datetime.now(),
            "dia_semana": dia_hoy,
            "ferias_de_hoy": ferias_hoy,
            "todas_las_comunas": comunas_con_feria,
        }
        return pack_datos


@ns.route("/app/info/<slug_feria>")
class pack_info_feria(Resource):
    @ns.marshal_list_with(schema_pack_feria)
    def get(self, slug_feria):
        datos = {"slug": slug_feria}
        feria = db.session.query(Feria).filter(Feria.slug == slug_feria).first()
        if feria:
            feria.puntos = [
                {"tipo": 0, "titulo": "XXYYY", "link": "https://www.red.cl/"},
                {"tipo": 0, "titulo": "XXYYY", "link": "https://www.red.cl/"},
            ]
            datos.update({"status": "encontrada"})
            datos.update({"info": feria})

        else:
            datos.update({"status": "no encontrada"})
        return datos
