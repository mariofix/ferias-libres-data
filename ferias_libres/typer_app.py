from typer import Typer
from .configuracion import config
from .catastroferiaslibres import cli as cfl_cli
from .odepa import cli as odepa_cli

typer = Typer()
typer.add_typer(cfl_cli)
typer.add_typer(odepa_cli)