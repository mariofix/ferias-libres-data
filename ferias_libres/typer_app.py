import json
import re
import time
from typing import Optional

import httpx
import typer
from pydantic import HttpUrl
from rich import print as rich_print
from slugify import slugify
from typing_extensions import Annotated

from .configuracion import config
from .schemas import Comuna, Feria, LatLng, Payload, Semana

app = typer.Typer(help="CLI App para procesamiento de datos de Ferias Libres")
app_debug = config.debug


def descarga_url(url_list: Optional[list] = None) -> list:
    if not url_list:
        raise Exception("La lista de URLs no puede estar vacia")

    data: list = []
    primer_request = True
    headers = {"user-agent": config.httpx_ua}
    with httpx.Client(limits=config.httpx_limits, headers=headers) as cliente:
        for url in url_list:
            if not primer_request:
                if config.debug:
                    rich_print(
                        f"Esperando {config.tiempo_espera}s para no sobrecargar la API"
                    )
                time.sleep(config.tiempo_espera)

            if config.debug:
                rich_print(f"Iniciando descarga: {url}")
            datos = cliente.get(str(url))
            dict_key = slugify(url.query)
            if config.debug:
                rich_print(f"Se seteó en indice {dict_key=}")
            nueva_region = {f"{dict_key}": datos.json()}
            if config.debug:
                rich_print(f"{nueva_region=}")
            data.append(nueva_region)
            primer_request = False

    return data


@app.command("obtiene-comunas")
def descarga_comunas_por_region(
    region: Annotated[
        Optional[int],
        typer.Option(help="Define region a descargar. Todas si no se define."),
    ] = None,
    guardar: Annotated[
        bool,
        typer.Option(
            help="Guarda automaticamente el archivo en vez de mostrarlo en pantalla."
        ),
    ] = False,
    archivo: Annotated[
        str,
        typer.Option(help="nombre del archivo a guardar."),
    ] = "./comunas.json",
):
    """
    Descarga Listado de comunas
    """
    urls: list[HttpUrl] = []
    if not region:
        if config.debug:
            rich_print("Vamos a descargar las comunas de 15 regiones...")
        for region in range(1, 16):
            urls.append(HttpUrl(f"{config.odepa_comunas}?pRegionId={region}"))

    else:
        urls.append(HttpUrl(f"{config.odepa_comunas}?pRegionId={region}"))

    datos = descarga_url(urls)
    if not guardar:
        rich_print(datos)
    else:
        with open(archivo, "w", encoding="utf-8") as f:
            try:
                json.dump(datos, f, ensure_ascii=False, indent=4, sort_keys=True)
            except Exception as e:
                rich_print(f"Error: {e}")
                raise typer.Abort()
            else:
                rich_print(f"Archivo [bold]{archivo}[/bold] Guardado!")
                raise typer.Exit()


@app.command("obtiene-ferias")
def descarga_ferias_por_region(
    region: Annotated[
        Optional[int],
        typer.Option(help="Define region a descargar. Todas si no se define."),
    ] = None,
    guardar: Annotated[
        bool,
        typer.Option(
            help="Guarda automaticamente el archivo en vez de mostrarlo en pantalla."
        ),
    ] = False,
    archivo: Annotated[
        str,
        typer.Option(help="nombre del archivo a guardar."),
    ] = "./ferias.json",
):
    """
    Descarga Listado de ferias libres
    """
    urls: list[HttpUrl] = []
    if not region:
        if config.debug:
            rich_print("Vamos a descargar las ferias de 15 regiones...")
        for region in range(1, 16):
            urls.append(HttpUrl(f"{config.odepa_ferias}?pRegionId={region}"))

    else:
        urls.append(HttpUrl(f"{config.odepa_ferias}?pRegionId={region}"))

    datos = descarga_url(urls)
    if not guardar:
        rich_print(datos)
    else:
        with open(archivo, "w", encoding="utf-8") as f:
            try:
                json.dump(datos, f, ensure_ascii=False, indent=4, sort_keys=True)
            except Exception as e:
                rich_print(f"Error: {e}")
                raise typer.Abort()
            else:
                rich_print(f"Archivo [bold]{archivo}[/bold] Guardado!")
                raise typer.Exit()


@app.command("genera-archivos")
def genera_archivos_por_comuna(
    archivo_comunas: Annotated[
        str, typer.Option(help="archivo de comunas")
    ] = "./comunas.json",
    archivo_ferias: Annotated[
        str, typer.Option(help="archivo de ferias")
    ] = "./ferias.json",
    guardar: Annotated[
        bool,
        typer.Option(
            help="Guarda automaticamente el archivo en vez de mostrarlo en pantalla."
        ),
    ] = False,
    archivo: Annotated[
        str,
        typer.Option(help="nombre del archivo a guardar."),
    ] = "./ferias-libres-data.json",
):
    """
    Genera archivos para Ferias Libres
    """
    global app_debug
    with open(archivo_ferias, "r", encoding="utf-8") as ferias:
        lista_ferias = json.load(ferias)

    comunas: dict = {}
    if app_debug:
        rich_print(f"Procesando {len(lista_ferias)} regiones.")
    for fila_feria in lista_ferias:
        for region, fila in fila_feria.items():
            num_region = int(region.split("-").pop())
            if app_debug:
                rich_print(f"{region=}")
                rich_print(f"{num_region=}")
                rich_print(f"Procesando {len(fila)} ferias.")
            for feria in fila:
                comuna_slug = slugify(feria.get("nombre_comuna"))
                if app_debug:
                    rich_print(f"{feria.get('nombre_comuna')=}")
                    rich_print(f"{comuna_slug=}")
                comuna = Comuna(
                    nombre=feria.get("nombre_comuna"),
                    slug=comuna_slug,
                    region=num_region,
                    ubicacion=LatLng(),
                )
                if comuna.slug not in comunas.keys():
                    comunas.update({comuna.slug: comuna.dict()})

                feriaModel = Feria(
                    nombre=feria.get("nombre_feria"),
                    dias=adivina_dias(feria.get("postura_feria")),
                    ubicacion=obtiene_lista_ubicaciones(feria.get("coordenadas")),
                )
                if app_debug:
                    rich_print(f"{feria=}")

                comunas[comuna_slug]["ferias"].append(feriaModel.dict())

    with open(archivo, "w", encoding="utf-8") as f:
        try:
            json.dump(comunas, f, ensure_ascii=False, indent=4, sort_keys=True)
        except Exception as e:
            rich_print(f"Error: {e}")
            raise typer.Abort()
        else:
            rich_print(f"Archivo [bold]{archivo}[/bold] Guardado!")
            raise typer.Exit()
    raise typer.Exit()


def obtiene_lista_ubicaciones(lista: list) -> list:
    global app_debug
    if app_debug:
        rich_print(f"Procesando {len(lista)} elementos")
    ubicaciones = []
    for row in lista:
        ubicacion = LatLng(
            latitude=row.get("lat").strip(), longitude=row.get("lng").strip()
        )
        if app_debug:
            rich_print(f"{ubicacion=}")
        ubicaciones.append(ubicacion)

    if app_debug:
        rich_print(f"{ubicaciones=}")
    return ubicaciones


def adivina_dias(texto: str) -> Semana:
    global app_debug
    semana = Semana()
    encontrado = False
    lunes = re.compile("Lunes|lunes|lun")
    martes = re.compile("Martes|martes|arte")
    miercoles = re.compile("Miercoles|miercoles|mie|iércol")
    jueves = re.compile("Jueves|jueves|jue")
    viernes = re.compile("Viernes|viernes|vie")
    sabado = re.compile("sab|ábado")
    domingo = re.compile("Domingo|domingo|dom")
    if re.search(lunes, texto):
        semana.lunes = True
        encontrado = True
    if re.search(martes, texto):
        semana.martes = True
        encontrado = True
    if re.search(miercoles, texto):
        semana.miercoles = True
        encontrado = True
    if re.search(jueves, texto):
        semana.jueves = True
        encontrado = True
    if re.search(viernes, texto):
        semana.viernes = True
        encontrado = True
    if re.search(sabado, texto):
        semana.sabado = True
        encontrado = True
    if re.search(domingo, texto):
        semana.domingo = True
        encontrado = True
    if not encontrado:
        semana.especial = True
        semana.motivo = texto
    if app_debug:
        rich_print(f"{texto=}")
        rich_print(f"{semana}")

    return semana


@app.callback()
def main(debug: bool = False):
    global app_debug
    if debug:
        app_debug = True

    if app_debug:
        rich_print("[bold]Debug Enabled[/bold]")
