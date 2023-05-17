from pydantic import HttpUrl
from pydantic_settings import BaseSettings
from httpx import Limits


class Configuracion(BaseSettings):
    debug: bool = True
    show_dots: bool = True
    odepa_comunas: HttpUrl = "https://apimapaferias.sercotec.cl/API/Comuna/PorRegion"  # type: ignore
    odepa_ferias: HttpUrl = (
        "https://apimapaferias.sercotec.cl/API/Placemark/FeriasPorRegion"
    )  # type: ignore
    tiempo_espera: int = 1

    httpx_ua: str = (
        "Ferias-Libres/1.0.3 Ferias-Libres-Data-Fetcher/0.1.0 python-httpx/latest"
    )
    httpx_limits: Limits = Limits(max_connections=2)


config = Configuracion()
