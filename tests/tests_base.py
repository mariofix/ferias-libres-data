from ferias_libres.typer_app import descarga_url, adivina_dias, obtiene_lista_ubicaciones
import pytest

def test_descarga_sin_url():
    with pytest.raises(Exception):
        descarga_url(None)

def test_adivina_dias():
    semana = adivina_dias("lunes")
    assert semana.lunes is True

def test_ubicaciones_lista_vacia():
    lista = obtiene_lista_ubicaciones([])
    assert len(lista) == 0
