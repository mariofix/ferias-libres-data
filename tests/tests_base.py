import pytest  # noqa: F401

from ferias_libres.typer_app import adivina_dias, obtiene_lista_ubicaciones


def test_adivina_dias():
    semana = adivina_dias("lunes martes miercoles jueves viernes sabado dom")
    assert semana.lunes is True
    assert semana.martes is True
    assert semana.miercoles is True
    assert semana.jueves is True
    assert semana.viernes is True
    assert semana.sabado is True
    assert semana.domingo is True
    assert semana.especial is False
    assert semana.motivo == ""


def test_adivina_dias_especial():
    semana = adivina_dias("Dia de Pago")
    assert semana.especial is True
    assert semana.motivo == "Dia de Pago"


def test_ubicaciones_lista_vacia():
    lista = obtiene_lista_ubicaciones([])
    assert len(lista) == 0
