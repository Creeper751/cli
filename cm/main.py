import logging
from typing import Any

import click
import os
import toml
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
from rich.prompt import Confirm
from errors import ConfigParseException


console = Console()
install()
FORMAT = "%(message)s"
logging.basicConfig(
	level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger("rich")
config = None
aliases = {}


@click.group()
@click.option('--log_level', default="NOTSET", type=str)
@click.version_option("v1.0", package_name="cm (Command Manager)")
def cli(log_level: Any | str):
	"""Welcome to cm, the ultimate script and alias manager for macOS!"""
	level = log_level.upper() if str(log_level).lower() in ["notset", "debug", "warning", "critical", "info",
	                                                        "error"] else "NOTSET"
	conf_file = os.environ.get("CM_CONF_NAME")
	if conf_file is None:
		conf_file = "default"
	log.setLevel(level)
	log.debug("Debug is now enabled.")
	log.info("Loading Config...")
	if os.path.isfile(f"~/.config/cm/{conf_file}.toml"):
		log.debug(f"File ~/.config/cm/{conf_file}.toml detected. Loading config...")
		with open(f"~/.config/cm/{conf_file}.toml", mode="rb") as file:
			if file:
				conf = toml.load(file)
				log.info("Config load successful")
				parse_config(conf)

			else:
				console.print("[bold red]File is empty!")
				console.print("[bold bright_black]Please run 'cm config use default' to use the default config")
				console.print("[bold yellow]:warning:No config loaded, proceed with caution!:warning:")
	else:
		log.debug(f"No config file {conf_file}.toml found!")
		console.print("[bold red]No config file found! Please run 'cm config use default' to use the default config")
		console.print("[bold yellow]:warning:No config loaded, proceed with caution!:warning:")


def parse_config(config: dict):
	log.debug("Parsing config...")
	if not isinstance(config, dict):
		raise ConfigParseException("Config is not of type dict!")
	keys = [x for x in config.keys()]
	for i in range(len(config.keys())):
		if keys[i] not in ["cm"]:
			raise ConfigParseException(f"Invalid configuration!, {keys[i]} not supposed to be where it is!")
		if isinstance(config.get(keys[i]), dict):
			aliases = {}
			parse_helper(keys[i], config.get(keys[i]))
		else:
			raise ConfigParseException("Invalid configuration! 'cm' is supposed to be a table, not a value!")

def parse_helper(key, value: dict):
	keys = [x for x in value.keys()]
	for new_key in keys:
		if new_key not in ["alias", "script", "misc"]:
			raise ConfigParseException(f"Invalid configuration!, {key} not valid table attribute")
		if new_key == "alias":










if __name__ == "__main__":
	cli()
