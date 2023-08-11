import typer
from rich.console import Console
from rich import pretty

pretty.install()
console = Console()

main = typer.Typer(add_completion=False,
                   help="A simple cli application to convert things to and from binary and decimal")


def validator(b_or_d: str, test_input: str):
	global successful
	successful = True
	if b_or_d == "binary":
		for i in list(test_input):
			if int(i) not in [0, 1]:
				successful = False
				raise TypeError("Data specified is not binary")
	elif b_or_d == "decimal":
		try:
			int(test_input)
		except TypeError:
			successful = False
			try:
				raise TypeError("Data specified is not a number")
			except TypeError:
				console.print_exception()
	else:
		successful = False
		raise TypeError("Binary-Decimal input switch invalid")
	return successful


@main.command()
def to_binary(decimal: str = typer.Argument(..., help="Numbers to translate")):
	valid = validator("decimal", decimal)
	str_decimal = decimal
	decimal = int(decimal)
	if not valid:
		raise TypeError("Data not valid")
	binary = ""
	if decimal == 0:
		binary = "0"
	else:
		while decimal > 0:
			binary = str(decimal % 2) + binary
			decimal = decimal // 2
	console.print(f"The decimal {str_decimal} in binary is {binary}")


@main.command()
def to_decimal(binary: str = typer.Argument(..., help="Binary to translate")):
	valid = validator("binary", binary)
	str_bin = binary
	binary = list(binary)
	binary = binary[::-1]
	total = 0
	index = -1
	data = [2 ** i for i in range(len(binary))]
	if not valid:
		raise TypeError("Binary data not valid!")
	for i in binary:
		i = int(i)
		index += 1
		if i:
			total += data[index]
	console.print(f"The binary string {str_bin} results to {total} in decimal")
