from httpx import Limits
from pydantic import HttpUrl
from pydantic_settings import BaseSettings
from .version import __version__


class Configuracion(BaseSettings):
    debug: bool = False
    show_dots: bool = True
    odepa_comunas: HttpUrl = "https://apimapaferias.sercotec.cl/API/Comuna/PorRegion"  # type: ignore
    odepa_ferias: HttpUrl = "https://apimapaferias.sercotec.cl/API/Placemark/FeriasPorRegion"  # type: ignore
    tiempo_espera: float = 0.2

    httpx_ua: str = f"Ferias-Libres/{__version__} Ferias-Libres-Data-Fetcher/{__version__} python-httpx/latest"
    httpx_limits: Limits = Limits(max_connections=1)
    httpx_limits_api: Limits = Limits(max_connections=4)


config = Configuracion()
