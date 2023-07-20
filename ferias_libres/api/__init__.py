from flask import Blueprint
from flask_restx import Api

from ..version import __version__

# from .ns_admin import ns as admin_ns
from .ns_comunas import ns as comunas_ns
from .ns_datos import ns as datos_ns
from .ns_ferias import ns as ferias_ns

api_bp = Blueprint("api", __name__)

api = Api(
    api_bp,
    version=__version__,
    title="Ferias Libres API",
    description="API Endpoints para la App Ferias Libres",
    validate=True,
    ordered=True,
    doc="/doc/",
)

api.add_namespace(comunas_ns)
api.add_namespace(ferias_ns)
# api.add_namespace(admin_ns)
api.add_namespace(datos_ns)
