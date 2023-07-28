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
conf = None
aliases = {}
misc = {}
scripts = {}


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
				global aliases
				global misc
				global scripts
				(aliases, misc, scripts) = parse_config(conf)

			else:
				console.print("[bold red]File is empty!")
				console.print("[bold bright_black]Please run 'cm default_config' to use the default config")
				console.print("[bold yellow]:warning:No config loaded, proceed with caution!:warning:")
	else:
		log.debug(f"No config file {conf_file}.toml found!")
		console.print("[bold red]No config file found! Please run 'cm default_config' to use the default config")
		console.print("[bold yellow]:warning:No config loaded, proceed with caution!:warning:")


def parse_config(conf: dict):
	log.debug("Parsing config...")
	if not isinstance(conf, dict):
		raise ConfigParseException("Config is not of type dict!")
	keys = [x for x in conf.keys()]
	for i in range(len(conf.keys())):
		if keys[i] not in ["cm"]:
			raise ConfigParseException(f"Invalid configuration!, {keys[i]} not supposed to be where it is!")
		if isinstance(conf.get(keys[i]), dict):
			data = parse_helper(keys[i], conf.get(keys[i]))
			return data
		else:
			raise ConfigParseException("Invalid configuration! 'cm' is supposed to be a table, not a value!")


def parse_helper(key, value: dict) -> tuple[dict, dict, dict]:
	global aliases, scripts, misc
	keys = [x for x in value.keys()]
	for new_key in keys:
		if new_key not in ["alias", "script", "misc"]:
			raise ConfigParseException(f"Invalid configuration!, {key} not valid table attribute")
		data = validate_data(({"alias": value.get("alias")}, {"script": value.get("script")}, {"misc": value.get("misc")}))
		return data


def validate_data(tuple_data: tuple[dict, dict, dict]):
	global aliases
	global misc
	global scripts
	(alias_dict, script_dict, misc_dict) = tuple_data
	for data in tuple_data:
		for key, value in data:
			if key == "alias":
				ref_aliases = value.get("aliases")
				for i in ref_aliases:
					if value.get(i) is None:
						raise ConfigParseException(f"The alias mentioned, {i}, is not specified!")
					else:
						aliases[i] = value.get(i)
			if key == "misc":
				for i in value.keys():
					if i in ["default"] and value.get(i) is not None:
						misc[i] = value.get(i)
			if key == "script":
				ref_script = value.get(scripts)
				for i in ref_script:
					if value.get(i) is None:
						raise ConfigParseException(f"The script mentioned, {i}, is not specified")
					elif ("label" or "runner") not in (current_script := value.get(i)).keys():
						raise ConfigParseException(f"'runner' or 'label' not specified in script {i}!")
					scripts[i] = value.get(i)
			else:
				raise ConfigParseException(f"{key} is not valid table attribute!")
	data = (aliases, misc, scripts)
	return data






if __name__ == "__main__":
	cli()
