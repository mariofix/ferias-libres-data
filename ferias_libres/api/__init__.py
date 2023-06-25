from flask import Blueprint
from flask_restx import Api

from .ns_comunas import ns as comunas_ns
from .ns_ferias import ns as ferias_ns

api_bp = Blueprint("api", __name__)

api = Api(
    api_bp,
    version="0.1.0",
    title="Ferias Libres API",
    description="API Endpoints para la App Ferias Libres",
    validate=True,
    ordered=True,
)

api.add_namespace(comunas_ns)
api.add_namespace(ferias_ns)
