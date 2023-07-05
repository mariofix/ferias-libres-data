import json
import time

from flask import abort
from flask_restx import Namespace, Resource, fields
from rich import print as rich_print
from slugify import slugify

from ..database import db
from ..models import Comuna, Feria

ns = Namespace("admin")


feria_schema = ns.model("Ferias", {"slug": fields.String, "nombre": fields.String})


@ns.route("/carga-ferias")
class carga_ferias(Resource):
    @ns.marshal_list_with(feria_schema)
    def get(self):
        with open(
            "/home/mariofix/proyectos/ferias-libres-data/ferias-libres-data.json",
            encoding="utf-8",
        ) as f:
            nuevas = []
            lista = json.load(f)
            # print(f"{lista=}")
            for key, row in lista.items():
                # rich_print(f"{key=} {row=}")
                comuna = Comuna.query.filter_by(slug=row["slug"]).first()
                if not comuna:
                    rich_print(f"[bold]{row['slug']}[/bold] no existe!!.")
                    continue
                rich_print(f"{comuna=}")
                for f in row["ferias"]:
                    ferias_attrs = {
                        "nombre": f["nombre"].strip(),
                        "slug": slugify(f"{row['slug'].strip()} {f['nombre'].strip()}"),
                        "dias": f["dias"],
                        "ubicacion": f["ubicacion"],
                        "comuna_id": comuna.id,
                    }

                    rich_print(f"{ferias_attrs=}")
                    feria = Feria.query.filter_by(slug=ferias_attrs["slug"]).first()
                    if not feria:
                        nueva = Feria(**ferias_attrs)
                        db.session.add(nueva)
                        db.session.commit()
                        nuevas.append(nueva)

        return nuevas
