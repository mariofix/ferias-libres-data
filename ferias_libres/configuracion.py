from pydantic_settings import BaseSettings


class Configuracion(BaseSettings):
    debug: bool = True

    # origenes: list[str] = list(["catastroferias", "odepa"])
    # Mas adelante de deberia poder elegir que cargar


config = Configuracion()