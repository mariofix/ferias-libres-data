import typer
from rich import print as rich_print
from .configuracion import config
from typing_extensions import Annotated
from typing import Optional
import time
import httpx
from pydantic import HttpUrl
from slugify import slugify
import json

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
            else:
                rich_print(f"Archivo [bold]{archivo}[/bold] Guardado!")


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
            else:
                rich_print(f"Archivo [bold]{archivo}[/bold] Guardado!")


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
    with open(archivo_comunas, "r", encoding="utf-8") as comunas:
        lista_comunas = json.load(comunas)

    rich_print(f"{lista_comunas=}")

    with open(archivo_ferias, "r", encoding="utf-8") as ferias:
        lista_ferias = json.load(ferias)

    rich_print(f"{lista_ferias=}")


@app.callback()
def main(debug: bool = False):
    global app_debug
    if debug:
        app_debug = True

    if app_debug:
        rich_print("[bold]Debug Enabled[/bold]")
