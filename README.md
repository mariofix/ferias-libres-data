# ferias-libres-data

Data Files for Ferias Libres

[![Tests & Coverage](https://github.com/mariofix/ferias-libres-data/actions/workflows/Tests.yml/badge.svg?branch=main)](https://github.com/mariofix/ferias-libres-data/actions/workflows/Tests.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/c744545bcd4e419abbbf931781b64346)](https://app.codacy.com/gh/mariofix/ferias-libres-data/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/c744545bcd4e419abbbf931781b64346)](https://app.codacy.com/gh/mariofix/ferias-libres-data/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mariofix/ferias-libres-data/main.svg)](https://results.pre-commit.ci/latest/github/mariofix/ferias-libres-data/main)
![GitHub](https://img.shields.io/github/license/mariofix/ferias-libres-data)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/mariofix/ferias-libres-data/main)
![GitHub top language](https://img.shields.io/github/languages/top/mariofix/ferias-libres-data)

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
