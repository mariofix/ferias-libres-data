import json

from flask_restx import Namespace, Resource, fields
from rich import print as rich_print
from slugify import slugify

from ..database import db
from ..models import Comuna, Feria

ns = Namespace("ferias")

feria_schema = ns.model("Feria", {"slug": fields.String, "nombre": fields.String})


@ns.route("/")
class lista_todo(Resource):
    def get(self):
        return [{"nombre": "feria1"}, {"nombre": "feria2"}]


@ns.route("/<slug_comuna>")
class por_comuna(Resource):
    def get(self, slug_comuna):
        return {
            "comuna": slug_comuna,
            "ferias": [{"nombre": "feria1"}, {"nombre": "feria2"}],
        }


@ns.route("/carga-ferias")
class carga_ferias(Resource):
    @ns.marshal_list_with(feria_schema)
    def get(self):
        with open(
            "/home/mariofix/proyectos/ferias-libres-data/ferias_libres/archivo_destino.json",
            encoding="utf-8",
        ) as f:
            nuevas = []
            lista = json.load(f)
            for row in lista:
                comuna = Comuna.query.filter_by(slug=row["slug"]).first()
                if not comuna:
                    rich_print(f"[bold]{row['slug']}[/bold] no existe!!.")
                    continue
                print(f"{comuna=}")
                for f in row["ferias"]:
                    ferias_attrs = {
                        "nombre": f["nombre"],
                        "slug": slugify(f"{row['slug']} {f['nombre']}"),
                        **f["dias"],
                        "ubicacion": f["ubicacion"],
                        "comuna_id": comuna.id,
                    }

                    rich_print(f"{ferias_attrs=}")
                    nueva = Feria(**ferias_attrs)
                    db.session.add(nueva)
                    db.session.commit()
                    nuevas.append(nueva)

        return nuevas
