from flask_restx import Namespace, Resource, fields
from ..models import Comuna, Feria
from ..database import db
import datetime

ns = Namespace("datos")

schema_feria = ns.model(
    "Feria",
    {
        "slug": fields.String,
        "nombre": fields.String,
        "dias_str": fields.String,
        "comuna_str": fields.String,
        "funcionando": fields.Boolean,
        "latlng": fields.List(fields.String),
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


def dia_de_la_semana(dia: int) -> str | None:
    semana = ["domingo", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado"]
    try:
        return semana[dia]
    except KeyError:
        return None


@ns.route("/app/index")
class pack_datos_index(Resource):
    @ns.marshal_list_with(schema_pack_datos)
    def get(self):
        dia_hoy = dia_de_la_semana(datetime.datetime.now().weekday())
        ferias_hoy = db.session.query(Feria).filter(Feria.dias[dia_hoy] == True).all()
        comunas_con_feria = db.session.query(Comuna).filter(Comuna.ferias.any()).all()
        pack_datos = {
            "fecha": datetime.datetime.now(),
            "dia_semana": dia_hoy,
            "ferias_de_hoy": ferias_hoy,
            "todas_las_comunas": comunas_con_feria,
        }
        return pack_datos
