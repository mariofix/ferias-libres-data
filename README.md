# ferias-libres-data

Data Files for Ferias Libres

## Origenes de Datos

[https://github.com/altazor-1967/Comunas-de-Chile](https://github.com/altazor-1967/Comunas-de-Chile)
[https://apimapaferias.sercotec.cl/API/Comuna/PorRegion?pRegionId=1](https://apimapaferias.sercotec.cl/API/Comuna/PorRegion?pRegionId=1)
[https://apimapaferias.sercotec.cl/API/Placemark/FeriasPorRegion?pRegionId=1](https://apimapaferias.sercotec.cl/API/Placemark/FeriasPorRegion?pRegionId=1)

## datos extra

buscar todas las direcciones de cada feria y calcular el rango de calles para obfuscar direcciones exactas
`https://geocode.maps.co/reverse?lat=-33.37864276006814&lon=-70.55694490947512`, pedirle a chatgpt que lo haga

los puntos
https://www.red.cl/restservice/rest/getpuntoparada/?lat=-33.37864276006814&lon=-70.55694490947512&bip=1


```python
import httpx, rich
while True:
    try:
        salida = httpx.get("https://www.red.cl/restservice/rest/getpuntoparada/?lat=-33.37864276006814&lon=-70.55694490947512&bip=1",verify=False, timeout=15.0)
    except Exception as e:
        rich.print(e)
    else:
        # Las estaciones de metro son son puntos bip que comienzan con "name" : "METRO*"
        # ni idea que significa la distancia, debe ser un calculo conocido
        rich.print_json(salida.text)
        break
```
