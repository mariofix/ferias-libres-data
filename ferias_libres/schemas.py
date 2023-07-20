from pydantic import BaseModel


class LatLng(BaseModel):
    latitude: float = 0.0
    longitude: float = 0.0
    latitudeDelta: float = 0.0
    longitudeDelta: float = 0.0

    @property
    def lat(self) -> float:
        return self.latitude

    @property
    def lng(self) -> float:
        return self.longitude


class Semana(BaseModel):
    lunes: bool = False
    martes: bool = False
    miercoles: bool = False
    jueves: bool = False
    viernes: bool = False
    sabado: bool = False
    domingo: bool = False
    especial: bool = False
    motivo: str = ""


class Feria(BaseModel):
    nombre: str
    dias: Semana
    ubicacion: list[LatLng] = []


class Comuna(BaseModel):
    nombre: str
    slug: str
    region: int
    ubicacion: LatLng
    ferias: list[Feria] = []


class Payload(BaseModel):
    comunas: list[Comuna] = []
