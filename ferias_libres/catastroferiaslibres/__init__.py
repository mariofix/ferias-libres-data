from typer import Typer

cli = Typer()

@cli.command()
def descarga_comunas_por_region():
    
    print("descarga_comunas_por_region")
    print("URL: https://apimapaferias.sercotec.cl/API/Comuna/PorRegion?pRegionId=[int]")

@cli.command()
def descarga_ferias_por_region():
    print("descarga_ferias_por_region")
    print("Param: xml/json")
    #usar async con httpx
    print("URL: https://apimapaferias.sercotec.cl/API/Placemark/FeriasPorRegion?pRegionId=[int]")

@cli.command()
def genera_archivos_por_comuna():
    print("Genera Archivos json separados por comuna.")
    print("Param: comuna/s")
    print("Param: destino")