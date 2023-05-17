from ferias_libres.typer_app import descarga_url
import pytest

def test_descarga_sin_url():
    with pytest.raises(Exception):
        descarga_url(None)