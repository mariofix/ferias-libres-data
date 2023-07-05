from flask import abort
from flask_restx import Namespace, Resource

from ..models import Comuna, Feria

ns = Namespace("ferias")


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
