import json

from flask import abort
from flask_restx import Namespace, Resource, fields
from rich import print as rich_print
from slugify import slugify

from ..database import db
from ..models import Comuna, Feria

ns = Namespace("ferias")


feria_schema = ns.model("Ferias", {"slug": fields.String, "nombre": fields.String})


@ns.route("/")
class lista_todo(Resource):
    def get(self):
        ferias = Feria.query.all()
        lista_ferias: list = list()
        for feria in ferias:
            lista_ferias.append(
                {
                    "nombre": feria.nombre,
                    "slug": feria.slug,
                    "ubicacion": feria.ubicacion,
                    "comuna_slug": feria.comuna.slug,
                    "comuna_nombre": feria.comuna.nombre,
                    "comuna_region_slug": feria.comuna.region,
                    "dias": {
                        "lunes": feria.lunes,
                        "martes": feria.martes,
                        "miercoles": feria.miercoles,
                        "jueves": feria.jueves,
                        "viernes": feria.viernes,
                        "sabado": feria.sabado,
                        "domingo": feria.domingo,
                    },
                }
            )

        return lista_ferias


@ns.route("/<slug_comuna>")
class por_comuna(Resource):
    def get(self, slug_comuna):
        return_payload: dict = dict()
        comuna = Comuna.query.filter(Comuna.slug == slug_comuna).first()
        if not comuna:
            abort(404, f"{slug_comuna} is not found.")

        ferias = Feria.query.filter(Feria.comuna_id == comuna.id).all()

        return_payload.update({"comuna_slug": comuna.slug})
        return_payload.update({"comuna_nombre": comuna.nombre})
        return_payload.update({"comuna_region_slug": comuna.region})
        lista_ferias: list = list()
        for feria in ferias:
            lista_ferias.append(
                {
                    "nombre": feria.nombre,
                    "slug": feria.slug,
                    "ubicacion": feria.ubicacion,
                    "dias": {
                        "lunes": feria.lunes,
                        "martes": feria.martes,
                        "miercoles": feria.miercoles,
                        "jueves": feria.jueves,
                        "viernes": feria.viernes,
                        "sabado": feria.sabado,
                        "domingo": feria.domingo,
                    },
                }
            )
        return_payload.update({"ferias": lista_ferias})
        return return_payload


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
