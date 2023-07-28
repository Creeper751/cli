import toml
from pprint import pprint

with open("default.toml", "r") as f:
	config = toml.load(f)
	pprint(config)
